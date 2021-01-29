#!/usr/bin/python3

# A script to modify CRIU binary images
# Author: Abhijit Mahurkar

import json
import sys
import fnmatch
from package import images
import os

filepath = sys.argv[1]

# Get files from dump folder
pgmap_file = fnmatch.filter(os.listdir(filepath), 'pagemap-*.img')
mm_file = fnmatch.filter(os.listdir(filepath), 'mm-*.img')

# open a MM image protobuf file for parsing
with open(filepath+mm_file[0], mode='rb') as mm_f:
    mm_img = images.load(mm_f, pretty=True)
    mm_list = mm_img['entries']

print('The MM list is', str(mm_list))

# open a PAGEMAP image protobuf file for parsing
with open(filepath+pgmap_file[0], mode='rb') as pgmap_f:
    pgmap_img = images.load(pgmap_f, pretty=True)
    pgmap_list = pgmap_img['entries']

# JSON file is a list of dictionaries, convert to lists and
# iterate over the list

for index in range(len(mm_list)):
    for key in mm_list[index]:
        if(key == "vmas"):
            vma_list = mm_list[index][key]
        if(key == "mm_start_brk"):
            heap_vma_start = mm_list[index][key]
        if(key == "mm_brk"):
            heap_vma_end = mm_list[index][key]
        if(key == "mm_start_code"):
            code_vma_start = mm_list[index][key]
        if(key == "mm_end_code"):
            code_vma_end = mm_list[index][key]

for i in range(len(vma_list)):
    for key2 in vma_list[i]:
        if(key2 == "flags"):
            if(vma_list[i][key2] == "MAP_PRIVATE | MAP_ANON | MAP_GROWSDOWN"):
                # Get the stack start address and end address from MM image JSON
                stack_vma_start = vma_list[i]["start"]
                stack_vma_end = vma_list[i]["end"]

# Print VMA list
for i in range(len(vma_list)):
    print('VMA start:', vma_list[i]["start"], '- VMA end:', vma_list[i]["end"])

print('\n')

# Print Mapped pages list
for i in range (1, len(pgmap_list)):
    print('Mapped page address:', pgmap_list[i]["vaddr"], 'Number of pages:', pgmap_list[i]["nr_pages"])


# Iterate over pagemap list and find mapped stack pages
for i in range(len(pgmap_list)):
    for key in pgmap_list[i]:
        if(key == "vaddr"):
            if(int(stack_vma_start, 16) < int(pgmap_list[i][key], 16) < int(stack_vma_end, 16)):
                print('\nThe stack page mapped address is:', pgmap_list[i][key])
                print('The number of stack pages mapped is:', pgmap_list[i]["nr_pages"])

# Print stack VMAs
print(' \nThe stack VMA start address is', stack_vma_start)
print('The stack VMA end address is', stack_vma_end)
print('The total number of stack pages is', (int(stack_vma_end, 16) - int(stack_vma_start, 16)) / 4096)

# Print heap VMAs
print('\nThe heap start address is:', heap_vma_start)
print('The heap end address is:', heap_vma_end)

# Print code VMAs
print('\nThe code start address is:', code_vma_start)
print('The code end address is:', code_vma_end)
