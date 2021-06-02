from __future__ import print_function
import pycriu 
import pycriu.utils
import os
import re
import sys

from elftools.elf.elffile import ELFFile
# Parses the DynamoRIO log and removes init functions from the master image given the init point
def remove_init_drio(filepath, library_offset, pid, trace_filepath_master, name, init_point, trace_filepath_worker = None):
    pgmap_img, _= pycriu.utils.readImages(pid, filepath)
    pgmap_list = pgmap_img['entries']
    pages_id = pgmap_list[0]['pages_id']
    flag = False
    binary_offset = 0
    pg_offset = 0
    bb_list = []

    f = open(trace_filepath_master, 'r')
    content = f.readlines()
    content = [x.strip() for x in content]
    f.close()
    if(trace_filepath_worker != None):
        f_worker = open(trace_filepath_worker, 'r')
        content_worker = f_worker.readlines()
        content_worker = [x.strip() for x in content_worker]
        f_worker.close()

    for i in range(len(content)):
        if name in content[i]:
            i+=1
            module_id = content[i].split(',')[0]
            binary_path = content[i].split(', ')[6]
            break
    
    with open(binary_path.strip(), 'rb') as f:
        elffile = ELFFile(f)
        for section in elffile.iter_sections():
            if section.name.startswith('.text'):
                text_section_start_address = section.header['sh_offset']
                text_section_end_address = section.header['sh_offset'] + section.header['sh_size']
    
    for i in range(len(content)):
        if "BB Table" in content[i]:
            flag = True
            i+=1
        if flag == True:
            m = re.findall(r"\[\s*\+?(-?\d+)\s*\]", content[i])
            if str(module_id) in m:
                split_line = re.split('\[\s*|:\s*|\]\s*|\s*',content[i])
                #print(split_line)
                bb_address = split_line[2]
                bb_size = split_line[3]
                first_timestamp = split_line[5]
                latest_timestamp = split_line[7]
                if(int(latest_timestamp) == 0):
                    latest_timestamp = first_timestamp
                list_elem = [bb_address, bb_size, int(latest_timestamp)]
                bb_list.append(list_elem)
    bb_list.sort(key = lambda x:x[2])
    #print(bb_list)

    for list_elem in bb_list:
        if(list_elem[2] < int(init_point)):
            if(text_section_start_address <= int(list_elem[0], 16) <= text_section_end_address):
                trap_address = int(list_elem[0], 16) + library_offset
                for j in range(1, len(pgmap_list)):
                    pages = pgmap_list[j]["nr_pages"]
                    for key in pgmap_list[j]:
                        if(key == "vaddr"):
                            map_address = pgmap_list[j][key]
                            if(map_address <= trap_address < (map_address + pages * 4096)):
                                binary_offset = pg_offset + (trap_address - map_address)
                    pg_offset = pg_offset + (4096 * pages)
                
                print("The offset in the pages-1.img is:", binary_offset, "(decimal)", list_elem[0], list_elem[2])
                # Modify binary
                with open(os.path.join(filepath, 'pages-%s.img' % pages_id), mode='r+b') as f:
                    f.seek(binary_offset,0)
                    f.seek(-1,1)
                    f.write(b'\xCC' * int(list_elem[1]))
                    binary_offset = 0
                    pg_offset = 0

# Adds traps into the CRIU binary image
def remove_init(filepath, address, library_offset, pid, size):
    pgmap_img, _= pycriu.utils.readImages(pid, filepath)
    pgmap_list = pgmap_img['entries']
    pages_id = pgmap_list[0]['pages_id']
    trap_address = address + library_offset
    pg_offset = 0
    binary_offset = 0
    for i in range(1, len(pgmap_list)):
        pages = pgmap_list[i]["nr_pages"]
        for key in pgmap_list[i]:
            if(key == "vaddr"):
                map_address = pgmap_list[i][key]
                if(map_address <= trap_address < (map_address + pages * 4096)):
                    binary_offset = pg_offset + (trap_address - map_address)
                    print("The trap address is", trap_address)
        pg_offset = pg_offset + (4096 * pages)
    
    print("The offset in the pages-1.img is:", binary_offset, "(decimal)")
    # Modify binary
    with open(os.path.join(filepath, 'pages-%s.img' % pages_id), mode='r+b') as f:
        f.seek(binary_offset,0)
        bytes_data = f.read(1)
        print("The data at the location is:", bytes_data.encode('hex'))
        f.seek(-1,1)
        f.write(b'\xCC' * size)