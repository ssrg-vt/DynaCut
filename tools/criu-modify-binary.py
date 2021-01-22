"""
A Python script to modify a CRIU binary image using data from
pagemap dump and mm dump

Author: Abhijit Mahurkar
"""
import sys
import json

pg_offset = 0
address = sys.argv[1]
print('The address to be modifed is:', address)

# open a CRIT decoded MM image (JSON file) for parsing
with open("./dump10/mm-dump", mode='r') as mm_f:
    mm_data = json.load(mm_f)

mm_list = mm_data['entries']

# open a CRIT decoded PAGEMAP image (JSON file) for parsing
with open("./dump10/pagemap-dump", mode='r') as pgmap_f:
    pgmap_data = json.load(pgmap_f)

pgmap_list = pgmap_data['entries']

for i in range(1, len(pgmap_list)):
    pages = pgmap_list[i]["nr_pages"]
    for key in pgmap_list[i]:
        if(key == "vaddr"):
            map_address = int(pgmap_list[i][key], 16)
            if(map_address < int(address, 16) < (map_address + pages * 4096)):
                binary_offset = pg_offset + (int(address, 16) - map_address)
    pg_offset = pg_offset + (4096 * pages)

print(binary_offset)

# Modify binary
with open("./dump10/pages-1.img", mode='r+b') as f:
    f.seek(binary_offset,0)
    data_bytes = f.read(1)
    f.seek(-1, 1)
    f.write(b'\x10')
    data_bytes_write = f.read(4)

print('The data before modifying is', data_bytes.hex())
print('The data after modifying is', data_bytes_write.hex())


