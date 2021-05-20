from __future__ import print_function
import pycriu 
import pycriu.utils
import os
import re

# Parses the DynamoRIO log and stores nginx entries into a dictionary
def remove_init_drio(filepath, library_offset, pid, trace_filepath_master, trace_filepath_worker):
    pgmap_img, _= pycriu.utils.readImages(pid, filepath)
    whitelist = []
    pgmap_list = pgmap_img['entries']
    pages_id = pgmap_list[0]['pages_id']
    flag = False
    address_dict = {}
    binary_offset = 0
    pg_offset = 0
    f = open(trace_filepath_master, 'r')
    f_worker = open(trace_filepath_worker, 'r')
    content = f.readlines()
    content_worker = f_worker.readlines()
    content = [x.strip() for x in content]
    content_worker = [x.strip() for x in content_worker]

    with open(os.path.join(filepath, "whitelist"), mode='r+b') as f_whitelist:
        whitelist = f_whitelist.readlines()
        whitelist = [int(x, 16) for x in whitelist]

    for i in range(len(content)):
        if "nginx" in content[i]:
            if("18000" in content[i].split(',')[5]):
                module_id = content[i].split(',')[0]
        if "BB Table" in content[i]:
            flag = True
            i+=2
        if flag == True:
            m = re.findall(r"\[\s*\+?(-?\d+)\s*\]", content[i])
            if str(module_id) in m:
                split_line = re.split('\]: |,   |,  | |\[  |, ',content[i])
                bb_address = split_line[2]
                bb_size = split_line[3]
                #address_dict.setdefault(bb_address, [0, 0])
                #address_dict[bb_address][0] = bb_size
                #address_dict[bb_address][1] += 1
                if(int(bb_address, 16) == int("0x5baeb", 16)):
                    flag = False
                    break
                address_dict[bb_address] = bb_size
    
    # for i in range(len(content_worker)):
    #     if "nginx" in content_worker[i]:
    #         if("18000" in content_worker[i].split(',')[5]):
    #             module_id = content_worker[i].split(',')[0]
    #     if "BB Table" in content_worker[i]:
    #         flag = True
    #         i+=2
    #     if flag == True:
    #         m = re.findall(r"\[\s*\+?(-?\d+)\s*\]", content_worker[i])
    #         if str(module_id) in m:
    #             split_line = re.split('\]: |,   |,  | |\[  |, ',content_worker[i])
    #             bb_address = split_line[2]
    #             bb_size = split_line[3]
    #             #if str(bb_address) in address_dict.keys():
    #             #    address_dict[bb_address][1] += 1
                
    f.close()
    f_worker.close()

    for d_key in address_dict:
        #if(address_dict[d_key][1] == 1 and not(377358 <= int(d_key,16) <= 378315) and \
            #not(382740 <= int(d_key,16) <= 385232)):
            #print(d_key, address_dict[d_key][0])
        if(int("0x19280", 16) <= int(d_key,16) <= int("0xea000", 16) and (int(d_key,16) not in whitelist) \
            and not(int("0x23212", 16) <= int(d_key,16) <= int("0x24645",16)) \
                and not(int("0x33fb3", 16) <= int(d_key,16) <= int("0x346a4",16))):
            trap_address = int(d_key, 16) + library_offset
            for j in range(1, len(pgmap_list)):
                pages = pgmap_list[j]["nr_pages"]
                for key in pgmap_list[j]:
                    if(key == "vaddr"):
                        map_address = pgmap_list[j][key]
                        if(map_address <= trap_address < (map_address + pages * 4096)):
                            binary_offset = pg_offset + (trap_address - map_address)
                pg_offset = pg_offset + (4096 * pages)
            
            print("The offset in the pages-1.img is:", binary_offset, "(decimal)")
            # Modify binary
            with open(os.path.join(filepath, 'pages-%s.img' % pages_id), mode='r+b') as f:
                f.seek(binary_offset,0)
                bytes_data = f.read(1)
                print("The data at the location is:", bytes_data.encode('hex'), d_key)
                f.seek(-1,1)
                f.write(b'\xCC' *  int(address_dict[d_key][0], 10))
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