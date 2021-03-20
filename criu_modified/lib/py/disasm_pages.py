### A Python script to modify a CRIU binary image using data from
### pagemap dump and mm dump

### Author: Abhijit Mahurkar

import sys
import json
import os

#from capstone import *
import pycriu

class Disasmpages:

    def findOffset(self, mm_list, pgmap_list):
        pg_offset = 0
        for index in range(len(mm_list)):
            for key in mm_list[index]:
                if(key == "mm_start_code"):
                    code_vma_start = mm_list[index][key]
                if(key == "mm_end_code"):
                    code_vma_end = mm_list[index][key]

        for i in range(1, len(pgmap_list)):
            pages = pgmap_list[i]["nr_pages"]
            for key in pgmap_list[i]:
                if(key == "vaddr"):
                    map_address = pgmap_list[i][key]
                    if(code_vma_start <= map_address < code_vma_end):
                        code_offset = pg_offset
                    break
            pg_offset = pg_offset + (4096 * pages)
        
        return code_offset, code_vma_start, code_vma_end

    # Disassemble binary
    def disasm_binary(self, filepath, pages_file, code_offset, code_vma_start, code_vma_end):
        with open(os.path.join(filepath, pages_file[0]), mode='rb') as f:
            no_bytes_to_read = (code_vma_end - code_vma_start) + 1
            f.seek((code_offset),0)
            data_bytes = f.read(no_bytes_to_read)

        md = Cs(CS_ARCH_X86, CS_MODE_64)
        for i in md.disasm(data_bytes, 0x0):
            print("0x%x:\t%s\t%s" %(i.address, i.mnemonic, i.op_str))


def disassemblePages(filepath):
    """
    Input: filepath to the directory \n
    Output: Disassemble code pages from CRIU image
    """
    disasm = Disasmpages()

    pgmap_file, mm_file, pages_file = pycriu.utils.open_files(filepath)
    pgmap_img, mm_img = pycriu.utils.readImages(pgmap_file, mm_file, filepath)

    pgmap_list = pgmap_img['entries']
    mm_list = mm_img['entries']

    code_offset, code_vma_start, code_vma_end = disasm.findOffset(mm_list, pgmap_list)

    # Disassemble binary
    disasm.disasm_binary(filepath, pages_file, code_offset, code_vma_start, code_vma_end)

