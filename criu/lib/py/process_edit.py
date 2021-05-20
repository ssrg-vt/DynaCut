### A python module to edit a process image
### Author: Abhijit Mahurkar

from __future__ import print_function
import pycriu 
import pycriu.utils
import os

def modify_binary(filepath, address, pid):
    pgmap_file, mm_file = pycriu.utils.open_files(filepath, pid)
    pgmap_img, _= pycriu.utils.readImages(pid, filepath)
    pgmap_list = pgmap_img['entries']
    pages_id = pgmap_list[0]['pages_id']
    pg_offset = 0
    binary_offset = 0
    for i in range(1, len(pgmap_list)):
        pages = pgmap_list[i]["nr_pages"]
        for key in pgmap_list[i]:
            if(key == "vaddr"):
                map_address = pgmap_list[i][key]
                if(map_address < int(address, 16) < (map_address + pages * 4096)):
                    binary_offset = pg_offset + (int(address, 16) - map_address)
        pg_offset = pg_offset + (4096 * pages)
    
    print(binary_offset)
    # Modify binary
    with open(os.path.join(filepath, 'pages-%s.img' % pages_id), mode='r+b') as f:
        f.seek((binary_offset),0)
        bytes_data = f.read(1)
        print(bytes_data.encode('hex'))
        f.seek(-1,1)
        f.write(b'\xCC')

# Adds traps into the CRIU binary image
def modify_binary_dynamic(filepath, address, library_offset, pid):
    pgmap_file, mm_file = pycriu.utils.open_files(filepath, pid)
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
        f.write(b'\xCC')

