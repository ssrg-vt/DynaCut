from __future__ import print_function
import re
from elftools.elf.elffile import ELFFile
from collections import OrderedDict
import sys

DEBUG = True

def merge_log(file_list, name):
    bb_list = []
    bb_list_no_duplicates = []
    files_list = []
    i = 0
    flag = False
    module_id = 0
    for file in file_list:
        f = open(file, 'r')
        content = f.readlines()
        content = [x.strip() for x in content]
        for i in range(len(content)):
            if name in content[i]:
                #print('Inside if')
                i+=1
                module_id = content[i].split(',')[0]
                binary_path = content[i].split(', ')[6]
                #print(module_id)
                break

        for j in range(len(content)):
            if "BB Table" in content[j]:
                flag = True
                i+=2
            if flag == True:
                m = re.findall(r"\[\s*\+?(-?\d+)\s*\]", content[j])
                if str(module_id) in m:
                    #split_line = re.split('\[\s*|:\s*|\]\s*|\s*',content[j])
                    split_line = re.split('\[\s*|\]:\s*|,\s*',content[j])
                    bb_address = split_line[2]
                    bb_size = split_line[3]
                    #first_timestamp = split_line[5]
                    #latest_timestamp = split_line[7]
                    #if(int(latest_timestamp) == 0):
                    #    latest_timestamp = first_timestamp
                    list_elem = [bb_address, bb_size]
                    bb_list.append(list_elem)
                    f.close()
    #bb_list.sort(key = lambda x: intx[2])
    if DEBUG:
        print("The total number of executed BBs is:", len(bb_list))
    # To remove duplicates
    for list_elem in bb_list:
        if list_elem not in bb_list_no_duplicates:
            bb_list_no_duplicates.append(list_elem)
    
    if DEBUG:
        print("The total number of deduplicated executed BBs is:", len(bb_list_no_duplicates))
    # Display BB list
    #for i in range(len(bb_list)):
    #    print(bb_list[i])
    
    #Write BB list to file
    with open('bb_list_executed', 'wb+') as f_write:
         for item in bb_list_no_duplicates:
             f_write.write("%s\n" % item)
    
    return bb_list_no_duplicates, binary_path