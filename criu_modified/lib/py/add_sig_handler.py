#-------------------------------------------------------------------------------
# Created by Abhijit Mahurkar
# 03/17/2021
# This module adds library pages into the CRIU Image
#-------------------------------------------------------------------------------
from __future__ import print_function

import fnmatch
import os
from operator import itemgetter
import pycriu
from elftools.elf.elffile import ELFFile
import struct
import json

def page_start(x):
    page_mask = (~(4096 - 1))
    return (x & page_mask)

def page_end(x):
    return page_start(x + (4096 - 1))

def get_build_id(libpath, libname):
    # N: Number of characters in HEX string to split
    n = 8
    build_id_list = []
    with open(os.path.join(libpath, libname), 'rb') as f:
        elffile= ELFFile(f)
        for section in elffile.iter_sections():
             if(section.name == '.note.gnu.build-id'):
                 for notes in section.iter_notes():
                     build_id = notes['n_desc']
        build_id_str = [build_id[i:i+n] for i in range(0, len(build_id), n)]
        for b in build_id_str:
             little_hex = bytearray.fromhex(b)
             little_hex.reverse()
             str_little = ''.join(format(x, '02x')for x in little_hex)
             build_id_list.append(int(str_little, 16))
        
    return build_id_list

def create_new_file_object(libpath, build_id, id, size):
    payload = {
                "type": "REG",
                "id": id,
                "reg": {
                    "id": id,
                    "flags": "",
                    "pos": 0,
                    "fown": {
                        "uid": 0,
                        "euid": 0,
                        "signum": 0,
                        "pid_type": 0,
                        "pid": 0
                    },
                    "name": str(libpath),
                    "size": size,
                    #TODO: Calculate on the fly
                    "mode": 33277, #Octal: 100775 
                    "build_id": build_id
               }
           }
    return payload

def modify_files_img(filepath, libpath, libname):
    build_id = get_build_id(libpath, libname)
    size = os.stat(os.path.join(libpath, libname)).st_size
    id = 1
    with open(os.path.join(filepath, 'files.img'), mode = 'rb') as f:
        files_img = pycriu.images.load(f)
    file_list = files_img['entries']
    for files in file_list[0:]:
        id +=1
    file_item = create_new_file_object(os.path.join(libpath, libname), build_id, id, size)
    file_list.append(file_item)
    files_img['entries'] = file_list

    with open(os.path.join(filepath, 'files.img'), mode = 'rb+') as f:
        pycriu.images.dump(files_img, f)
    
    return id

def modify_core_img(filepath, handler_address, restorer_address):
    # Signal Number 5: SIGTRAP
    sig_id  = 5

    core_file = fnmatch.filter(os.listdir(filepath), 'core-*.img')
    
    # Open core file
    with open(os.path.join(filepath,core_file[0]), mode='rb') as f:
        core_img = pycriu.images.load(f)
    
    sigaction_list = core_img['entries'][0]['tc']['sigactions']

    sig_item = sigaction_list[sig_id - 1]

    sig_item['sigaction'] = str(handler_address)
    sig_item['flags'] = "0x14000000"
    sig_item['restorer'] = str(restorer_address)
    #TODO: cALCULATE ON THE FLY
    sig_item['mask'] = "0x10"
    sig_item['compat_sigaction'] = False

    sigaction_list[sig_id - 1] = sig_item
    core_img['entries'][0]['tc']['sigactions'] = sigaction_list

    with open(os.path.join(filepath,core_file[0]), mode='rb+') as f:
        pycriu.images.dump(core_img, f)

def calculate_num_pages(lib_path, libname):
    min_vaddr = 65535 #UINTPTR_MAX
    max_vaddr = 0
    with open(os.path.join(lib_path, libname), 'rb') as f:
        elffile = ELFFile(f)
        for segment in elffile.iter_segments():
            if(segment.header.p_type == 'PT_LOAD'):
                if(segment.header['p_vaddr'] < min_vaddr):
                    min_vaddr = segment.header['p_vaddr']
                if(segment.header['p_vaddr'] + segment.header['p_memsz'] > max_vaddr):
                    max_vaddr = segment.header['p_vaddr'] + segment.header['p_memsz']
    
    min_vaddr = page_start(min_vaddr)
    max_vaddr = page_end(max_vaddr)

    return ((max_vaddr - min_vaddr) / 4096)

def create_vma_item(offset, start_address, end_address, prot_list, file_id):
        item =  {
                          "start": start_address,
                          "end": end_address,
                          "pgoff": offset,
                          "shmid": file_id,
                          "prot": prot_list,
                          "flags": "MAP_PRIVATE",
                          "status": "VMA_AREA_REGULAR | VMA_FILE_PRIVATE",
                          "fd": -1,
                          "fdflags": 0
                }
        return item

def create_vma_item_pagemap(start_address, nr_pages):
    item =  {
                "vaddr": start_address,
                "nr_pages": nr_pages,
                "flags": "PE_PRESENT"
            }
    return item

def create_prot_list(flags):
    prot_list = ""
    if(flags >= 4):
        prot_list = "PROT_READ"
        if((flags -4 ) == 1):
            prot_list += " | PROT_EXEC"
        if((flags - 4) == 2):
            prot_list += " | PROT_WRITE"
        elif((flags - 4) == 3):
            prot_list += " | PROT_EXEC | PROT_WRITE"
    
    if((flags) == 1):
        prot_list += "PROT_EXEC"
    elif((flags) == 2):
            prot_list += "PROT_WRITE"
    elif((flags) == 3):
            prot_list += "PROT_EXEC | PROT_WRITE"

    return prot_list

def create_vmas(libpath, libname, start_address, file_id):
    vma_list_mm = []
    vma_list_pgmap = []
    vma_start = start_address
    with open(os.path.join(libpath, libname), 'rb') as f:
        elffile = ELFFile(f)
        for segment in elffile.iter_segments():
            if(segment.header.p_type == 'PT_LOAD'):
                offset = page_start(segment.header.p_offset)
                prot_list = create_prot_list(segment.header['p_flags'])
                end_address = page_end(vma_start + segment.header['p_vaddr'] + segment.header['p_memsz'])
                nr_pages = (end_address - start_address) >> 12
                vma_list_mm.append(create_vma_item(offset, start_address,\
                    end_address, prot_list, file_id))
                vma_list_pgmap.append(create_vma_item_pagemap(start_address, nr_pages))
                start_address = end_address
    return vma_list_mm, vma_list_pgmap

def add_pages(filepath, libpath, libname,  num_pages, library_address):

    f_zeros = open(os.path.join(filepath, 'zeros'), 'wb+')
    f_zeros.write(b'\x00' * num_pages * 4096)
    with open(os.path.join(libpath, libname), 'rb') as f:
        elffile = ELFFile(f)
        for segment in elffile.iter_segments():
            address = segment.header['p_vaddr']
            if(segment.header.p_type == 'PT_LOAD'):
                f_zeros.seek(address, 0)
                f_zeros.write(segment.data())
    
    with open(os.path.join(filepath, "plt-file.json")) as plt_file:
        plt_data = json.load(plt_file)
        plt_file_entries = plt_data['entries']
    
    for i in range(0, len(plt_file_entries)):
        # IF condition checks whether entries in plt-file.json are valid
        if(int(plt_file_entries[i]['libc_offset'], 16) != 0):
            lib_address = int(plt_file_entries[i]['libc_offset'], 16) + library_address
            if(int(plt_file_entries[i]['plt_address'], 16)!= 0):
                plt_address = int(plt_file_entries[i]['plt_address'], 16)
                f_zeros.seek(plt_address, 0)
                f_zeros.write(struct.pack('<Q', lib_address))

    f_zeros.close()

def modify_binary_image(filepath, libpath, libname, library_address):
    num_pages = calculate_num_pages(libpath, libname)
    add_pages(filepath, libpath, libname, num_pages, library_address)
    return num_pages

def dump_new_images(mm_img, pgmap_img, mm_file, pgmap_file, filepath):
    
    with open(os.path.join(filepath, mm_file[0]), mode='rb+') as mm_file_write:
            pycriu.images.dump(mm_img, mm_file_write)
    
    with open(os.path.join(filepath, pgmap_file[0]), mode='rb+') as pgmap_file_write:
            pycriu.images.dump(pgmap_img, pgmap_file_write)

def append_at_location(pgmap_list, start_address):
    pg_offset = 0
    binary_offset = 0
    for i in range(1, len(pgmap_list)):
        pages = pgmap_list[i]["nr_pages"]
        for key in pgmap_list[i]:
            if(key == "vaddr"):
                map_address = pgmap_list[i][key]
                if(int(start_address, 16) <= map_address < (map_address + pages * 4096)):
                    binary_offset = pg_offset
                    return binary_offset
        pg_offset = pg_offset + (4096 * pages) 

def add_signal_handler(filepath, libpath, libname, handler_address, restorer_address,\
                                            vma_start_address, library_address):

    pgmap_file, mm_file, pages_file = pycriu.utils.open_files(filepath)
    pgmap_img, mm_img = pycriu.utils.readImages(pgmap_file, mm_file, filepath)

    pgmap_list = pgmap_img['entries']
    mm_list = mm_img['entries']

    file_id = modify_files_img(filepath, libpath, libname)
    modify_core_img(filepath, int(handler_address, 16), int(restorer_address, 16))
    vma_list_mm, vma_list_pgmap = create_vmas(libpath, libname, int(vma_start_address, 16), file_id)
    num_pages = modify_binary_image(filepath, libpath, libname, int(library_address))

    vma_list = mm_list[0]['vmas']

    copy_payload = pgmap_list[0]
    
    # Insert payload and sort the mm list
    # (CRIU needs the list to be sorted)
    
    vma_list.extend(vma_list_mm)
    new_vma_list = sorted(vma_list, key=itemgetter("start"))

    mm_img['entries'][0]['vmas'] = new_vma_list

    pgmap_list_extend = pgmap_list[1:]
    pgmap_list_extend.extend(vma_list_pgmap)
    new_pgmap_list = sorted(pgmap_list_extend, key=itemgetter("vaddr"))

    new_pgmap_list.insert(0,copy_payload)
    pgmap_img['entries'] = new_pgmap_list

    dump_new_images(mm_img, pgmap_img, mm_file, pgmap_file, filepath)

    binary_offset = append_at_location(pgmap_img['entries'], vma_start_address)

    # Copy data from offset to temp file
    with open(os.path.join(filepath, pages_file[0]), "rb") as pg_file,\
         open(os.path.join(filepath, "temp"), "wb+") as temp:
            pg_file.seek(binary_offset, 0)
            temp.write(pg_file.read())

    # Write pages to pages-img 
    with open(os.path.join(filepath, "zeros"), "rb") as myfile,\
         open(os.path.join(filepath, pages_file[0]), "rb+") as file2:
            file2.seek(binary_offset)
            file2.write(myfile.read())
    
    # Append zeros to the file
    with open(os.path.join(filepath, pages_file[0]), "rb+") as myfile, open(os.path.join(filepath, "temp"), "rb") as file2:
        myfile.seek(binary_offset + (num_pages * 4096), 0)
        myfile.write(file2.read())

    # Delete zeros and temp file
    os.remove(os.path.join(filepath, 'zeros'))
    os.remove(os.path.join(filepath, 'temp'))

    print('Done')

