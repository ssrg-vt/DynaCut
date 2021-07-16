from __future__ import print_function
import pycriu 
import pycriu.utils
import os
import re
import sys
import json
import struct

from elftools.elf.elffile import ELFFile

#Change to true to print

DEBUG = False

def config_remove_init(filepath, pid, library_offset, bb_trace, binary_path, init_point):
    config_list_data = ''
    config_list_address = ''
    config_list_both = ''
    # Write offset address to header file
    with open(os.path.join(filepath, 'config_base.h'), 'wb+') as config_base_file:
        config_base_file.write(hex(library_offset))

    pgmap_img, mm_img = pycriu.utils.readImages(pid, filepath)
    pgmap_list = pgmap_img['entries']
    mm_list = mm_img['entries'][0]
    pages_id = pgmap_list[0]['pages_id']
    binary_offset = 0
    pg_offset = 0
    i = 0
    new_bb_list = []
    end = 0

    binary_size = os.path.getsize(binary_path.strip())
    with open(binary_path.strip(), 'rb') as f:
        elffile = ELFFile(f)
        for section in elffile.iter_sections():
            if section.name.startswith('.text'):
                text_section_start_address = section.header['sh_offset']
                text_section_end_address = section.header['sh_offset'] + section.header['sh_size']

    # To add PROT_WRITE permission to executable segment of binary
    for vma in mm_list['vmas']:
        if (library_offset <= vma['start'] <= library_offset + binary_size):
            if(vma['prot'] == 5):
                vma['prot'] = 7
                break
    
    # Dump modified mm image
    mm_img['entries'][0] = mm_list
    _, mm_file = pycriu.utils.open_files(filepath, pid)
    with open(os.path.join(filepath, mm_file[0]), mode='rb+') as mm_f:
        pycriu.images.dump(mm_img, mm_f)
    
    bb_trace_int = [int(x[0],16) for x in bb_trace]
    init_index = bb_trace_int.index(int(init_point, 16))
    for list_elem in bb_trace:
        if(bb_trace_int.index(int(list_elem[0], 16)) < init_index and not (int(list_elem[0], 16) == int("0x43511", 16)) \
            and not (int(list_elem[0], 16) == int("0x434c0", 16)) and not (int(list_elem[0], 16) == int("0x16fd30", 16))\
                 and not (int(list_elem[0], 16) == int("0x167d19", 16))):
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

                # Modify binary
                with open(os.path.join(filepath, 'pages-%s.img' % pages_id), mode='r+b') as f:
                    f.seek(binary_offset,0)
                    bytes_data = f.read(1)
                    if((bytes_data.encode('hex') == (b'\x90').encode('hex'))):
                        if DEBUG:
                            print('Basic block starts with NOP instruction at address and not removed:', list_elem[0])
                            print(bytes_data.encode('hex'))
                        config_list_data+=''
                        config_list_address+=''
                        binary_offset = 0
                        pg_offset = 0
                        i+=1
                    else:
                        new_bb_list.append(list_elem)
                        if DEBUG:
                            print("The offset in the pages-1.img is:", binary_offset, "(decimal)", "address", \
                                list_elem[0], "size", list_elem[1])
                        f.seek(-1,1)
                        f.write(b'\xCC')
                        binary_offset = 0
                        pg_offset = 0
                        if i:
                            config_list_data+= ','
                            config_list_address+= ','
                            config_list_both+= ','
                        config_list_data += '0x{0}'.format(bytes_data.encode('hex'))
                        config_list_address += '{0}'.format(int(list_elem[0], 16))
                        config_list_both += '{{ {0} , 0x{1} }}'.format(int(list_elem[0], 16),bytes_data.encode('hex'))
                        i+=1
    
    if DEBUG:
        print("The number of BBs where traps are added is:", len(new_bb_list))

    with open(os.path.join(filepath, 'config_init_data.h'), 'wb+') as config_file:
        config_file.write("%s" % config_list_data)
    
    with open(os.path.join(filepath, 'config_init_address.h'), 'wb+') as config_file:
        config_file.write("%s" % config_list_address)

    with open ("bb_list_original",'w+') as bb_file_original:
        json.dump(bb_trace, bb_file_original)
    
    with open("bb_list_file", 'w+') as bb_file:
        json.dump(new_bb_list, bb_file)

# Parses the DynamoRIO log and removes init functions from the master image given the init point
def remove_init_drio(filepath, library_offset, pid, init_trap_file):

    pgmap_img, _= pycriu.utils.readImages(pid, filepath)
    bb_trace = []
    pgmap_list = pgmap_img['entries']
    pages_id = pgmap_list[0]['pages_id']
    binary_offset = 0
    pg_offset = 0
    bb_counter = 0
    removed_size = 0

    with open("bb_list_file", 'r') as bb_file:
        bb_trace = json.load(bb_file)
    
    with open("bb_list_original", 'r') as bb_file_original:
        bb_trace_original = json.load(bb_file_original)

    data_list = []
    f = open(init_trap_file, 'rb')
    f.seek(0,0)
    while True:
        try:
            data_list.append(struct.unpack_from("<Q", f.read(8))[0])
        except struct.error:
            break
    f.close()

    #print(data_list)
    data_list = [(x - library_offset) for x in data_list]
    bb_trace_int = [int(x[0], 16) for x in bb_trace_original]

    for list_elem in bb_trace:
        address_range = range((int(list_elem[0], 16) + 1),(int(list_elem[0], 16) + int(list_elem[1])))
        address_list = list(address_range)
        if(int(list_elem[0], 16) not in data_list and not(any(x in address_list for x in bb_trace_int))):
            trap_address = int(list_elem[0], 16) + library_offset
            for j in range(1, len(pgmap_list)):
                pages = pgmap_list[j]["nr_pages"]
                for key in pgmap_list[j]:
                    if(key == "vaddr"):
                        map_address = pgmap_list[j][key]
                        if(map_address <= trap_address < (map_address + pages * 4096)):
                            binary_offset = pg_offset + (trap_address - map_address)
                pg_offset = pg_offset + (4096 * pages)
            
            #Increment BB counter to count number of basic blocks removed
            bb_counter+=1
            removed_size += int(list_elem[1])
            if DEBUG:
                print("This offset has been permanently removed at offset", binary_offset, "(decimal)", "file offset:",\
                    list_elem[0], "size:", list_elem[1])
            # Modify binary
            with open(os.path.join(filepath, 'pages-%s.img' % pages_id), mode='r+b') as f:
                f.seek(binary_offset,0)
                f.write(b'\xCC'* int(list_elem[1]))
                binary_offset = 0
                pg_offset = 0
        else:
            if DEBUG:
                print('Data not removed at file offset:', list_elem[0],"of size", list_elem[1])

    if DEBUG:   
        print("The total number of basic blocks permanently removed is:", bb_counter)
        print("The total number of bytes of data removed is:", removed_size)

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
                    if DEBUG:
                        print("The trap address is", trap_address)
        pg_offset = pg_offset + (4096 * pages)
    
    if DEBUG:
        print("The offset in the pages-1.img is:", binary_offset, "(decimal)")
    # Modify binary
    with open(os.path.join(filepath, 'pages-%s.img' % pages_id), mode='r+b') as f:
        f.seek(binary_offset,0)
        bytes_data = f.read(1)
        if DEBUG:
            print("The data at the location is:", bytes_data.encode('hex'))
        f.seek(-1,1)
        f.write(b'\xCC' * size)