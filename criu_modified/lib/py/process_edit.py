### A python module to edit a process image
### Author: Abhijit Mahurkar

import pycriu 
import pycriu.utils
import sys
import json
import fnmatch
import os

def modify_binary(filepath, address):
    pgmap_file, mm_file, pages_file = pycriu.utils.open_files(filepath)
    pgmap_img, mm_img = pycriu.utils.readImages(pgmap_file, mm_file, filepath)
    pgmap_list = pgmap_img['entries']
    #mm_list = mm_img['entries']
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
    with open(os.path.join(filepath, pages_file[0]), mode='r+b') as f:
        f.seek((binary_offset),0)
        bytes_data = f.read(1)
        print(bytes_data.encode('hex'))
        f.seek(-1,1)
        f.write(b'\xCC')

def modify_binary_dynamic(filepath, address, library_offset):
    pgmap_file, mm_file, pages_file = pycriu.utils.open_files(filepath)
    pgmap_img, mm_img = pycriu.utils.readImages(pgmap_file, mm_file, filepath)
    pgmap_list = pgmap_img['entries']
    mm_list = mm_img['entries']
    mm_list_vmas = mm_list[0]['vmas']
    vmi = 0
    while mm_list_vmas[vmi]["start"] < int(address, 16):
        vmi+=1
    pg_offset = 0
    binary_offset = 0
    for i in range(1, len(pgmap_list)):
        pages = pgmap_list[i]["nr_pages"]
        for key in pgmap_list[i]:
            if(key == "vaddr"):
                map_address = pgmap_list[i][key]
                if(map_address <= int(address, 16) < (map_address + pages * 4096)):
                    print(mm_list_vmas[vmi]['pgoff'])
                    binary_offset = pg_offset + (int(address, 16) - map_address) + (int(library_offset, 16) - mm_list_vmas[vmi]['pgoff'])
                    print(pg_offset)
        pg_offset = pg_offset + (4096 * pages)
    
    print(binary_offset)
    # Modify binary
    with open(os.path.join(filepath, pages_file[0]), mode='r+b') as f:
        f.seek(binary_offset,0)
        bytes_data = f.read(1)
        print(bytes_data.encode('hex'))
        f.seek(-1,1)
        f.write(b'\xCC')

