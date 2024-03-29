#!/usr/bin/python2

import re
from elftools.elf.elffile import ELFFile
import sys

def merge_log(file_list, name):
    bb_list = []
    i = 0
    flag = False
    module_id = 0
    iter_file = 0
    for file in file_list:
        f = open(file, 'r')
        content = f.readlines()
        content = [x.strip() for x in content]
        for i in range(len(content)):
            if name in content[i]:
                print('Inside if')
                i+=1
                module_id = content[i].split(',')[0]
                binary_path = content[i].split(', ')[6]
                print(module_id)
                break

        for j in range(len(content)):
            if "BB Table" in content[j]:
                flag = True
                i+=1
            if flag == True:
                m = re.findall(r"\[\s*\+?(-?\d+)\s*\]", content[j])
                if str(module_id) in m:
                    split_line = re.split('\[\s*|:\s*|\]\s*|\s*',content[j])
                    bb_address = split_line[2]
                    bb_size = split_line[3]
                    first_timestamp = split_line[5]
                    latest_timestamp = split_line[7]
                    if(int(latest_timestamp) == 0):
                        latest_timestamp = first_timestamp
                    list_elem = [bb_address, bb_size, int(latest_timestamp)]
                    bb_list.append(list_elem)
                    f.close()
    bb_list.sort(key = lambda x:x[2])

    # Display BB list
    #for i in range(len(bb_list)):
    #    print(bb_list[i])
    
    # Write BB list to file
    with open('bb_list', 'wb+') as f_write:
        for item in bb_list:
            f_write.write("%s\n" % item)
    return bb_list, binary_path

name = sys.argv[1]
samples = sys.argv[2:]
print(name, samples)
merge_log(samples, str(name))
