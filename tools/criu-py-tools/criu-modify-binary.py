#!/usr/bin/env python3

# A Python script to modify a CRIU binary image using data from
# pagemap dump and mm dump
# Author: Abhijit Mahurkar

import sys
import json
import fnmatch
from package import images
import os

filepath = sys.argv[1]
address = sys.argv[2]
pg_offset = 0

print('The address to be modifed is:', address)

# Get files from dump folder
pgmap_file = fnmatch.filter(os.listdir(filepath), 'pagemap-*.img')
mm_file = fnmatch.filter(os.listdir(filepath), 'mm-*.img')

# open a MM image protobuf file for parsing
with open(filepath+mm_file[0], mode='rb') as mm_f:
    mm_img = images.load(mm_f, pretty=True)
    mm_list = mm_img['entries']

# open a PAGEMAP image protobuf file for parsing
with open(filepath+pgmap_file[0], mode='rb') as pgmap_f:
    pgmap_img = images.load(pgmap_f, pretty=True)
    pgmap_list = pgmap_img['entries']

for i in range(1, len(pgmap_list)):
    pages = pgmap_list[i]["nr_pages"]
    for key in pgmap_list[i]:
        if(key == "vaddr"):
            map_address = int(pgmap_list[i][key], 16)
            if(map_address < int(address, 16) < (map_address + pages * 4096)):
                binary_offset = pg_offset + (int(address, 16) - map_address)
    pg_offset = pg_offset + (4096 * pages)

print('The offset from the start of the pages-1.img binary is:', binary_offset, '(decimal)')

# Modify binary
with open(filepath+"pages-1.img", mode='r+b') as f:
    f.seek(binary_offset,0)
    data_bytes = f.read(1)
    f.seek(-1, 1)
    f.write(b'\x30')
    f.seek(binary_offset, 0)
    data_bytes_write = f.read(1)

print('The data before modifying is', data_bytes.hex())
print('The data after modifying is', data_bytes_write.hex())


