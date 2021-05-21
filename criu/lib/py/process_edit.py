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
    
    print("The int3 at binary offset: 0x{:08x}".format(binary_offset))
    # Modify binary
    with open(os.path.join(filepath, 'pages-%s.img' % pages_id), mode='r+b') as f:
        f.seek((binary_offset),0)
        bytes_data = f.read(1)
        print(bytes_data.encode('hex'))
        f.seek(-1,1)
        f.write(b'\xCC')

# Adds traps into the CRIU process image (for dynamically linked binary)
def modify_binary_dynamic(filepath, address, library_offset, pid):
    pgmap_img, _= pycriu.utils.readImages(pid, filepath)
    pgmap_list = pgmap_img['entries']
    pages_id = pgmap_list[0]['pages_id']
    trap_address = address + library_offset
    pg_offset = 0
    binary_offset = 0
    for i in range(1, len(pgmap_list)):
        nr_pages = pgmap_list[i]["nr_pages"]
        for key in pgmap_list[i]:
            if(key == "vaddr"):
                map_address = pgmap_list[i][key]
                if(map_address <= trap_address < (map_address + nr_pages*4096)):
                    binary_offset = pg_offset + (trap_address - map_address)
                    print("The int3 @ 0x{:04x}, offset in pages-1.img: 0x{:04x}".
                        format(trap_address, binary_offset))
                    break
        pg_offset = pg_offset + 4096*nr_pages
    
    # Modify binary
    with open(os.path.join(filepath, 'pages-%s.img' % pages_id), mode='r+b') as f:
        f.seek(binary_offset,0)
        bytes_data = f.read(1)
        print("The data @ 0x{:04x} is 0x{}".format(binary_offset, bytes_data.encode('hex')))
        f.seek(-1,1)
        f.write(b'\xCC')
