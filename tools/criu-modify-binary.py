"""
A Python script to modify a CRIU binary image using data from
pagemap dump and mm dump

Author: Abhijit Mahurkar
"""
import sys
import json

filepath = sys.argv[1]
address = sys.argv[2]
pg_offset = 0

print('The address to be modifed is:', address)

# open a CRIT decoded MM image (JSON file) for parsing
with open(filepath+"/mm_dump.json", mode='r') as mm_f:
    mm_data = json.load(mm_f)

mm_list = mm_data['entries']

# open a CRIT decoded PAGEMAP image (JSON file) for parsing
with open(filepath+"/pagemap_dump.json", mode='r') as pgmap_f:
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

print('The offset from the start of the pages-1.img binary is:', binary_offset, '(decimal)')

# Modify binary
with open(filepath+"/pages-1.img", mode='r+b') as f:
    f.seek(binary_offset,0)
    data_bytes = f.read(1)
    f.seek(-1, 1)
    f.write(b'\x30')
    f.seek(binary_offset, 0)
    data_bytes_write = f.read(1)

print('The data before modifying is', data_bytes.hex())
print('The data after modifying is', data_bytes_write.hex())


