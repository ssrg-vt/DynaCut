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
import pycriu.process_edit
from elftools.elf.elffile import ELFFile
from elftools.elf.elffile import DynamicSegment, GNUHashSection
import struct

# Aligns the address given to the page start
def page_start(x):
    page_mask = (~(4096 - 1))
    return (x & page_mask)

# Aligns the address given to the page end
def page_end(x):
    return page_start(x + (4096 - 1))

# Creates the build ID for the file (library) that is to be loaded into the 
# Address space
 
def get_build_id(libpath):
    # N: Number of characters in HEX string to split
    n = 8
    build_id_list = []
    with open(libpath, 'rb') as f:
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

# Creates a new file object to insert into files.img

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

# Modify the files.img and insert the file object

def modify_files_img(filepath, libpath):
    build_id = get_build_id(libpath)
    size = os.stat(libpath).st_size
    id = 1
    with open(os.path.join(filepath, 'files.img'), mode = 'rb') as f:
        files_img = pycriu.images.load(f)
    file_list = files_img['entries']
    for files in file_list[0:]:
        id +=1
    file_item = create_new_file_object(libpath, build_id, id, size)
    file_list.append(file_item)
    files_img['entries'] = file_list

    with open(os.path.join(filepath, 'files.img'), mode = 'rb+') as f:
        pycriu.images.dump(files_img, f)
    
    return id

# Add the SIGNAL info into core.img, including the restorer address and the 
# handler address from the sighandler library

def modify_core_img(filepath, handler_address, restorer_address, pid):
    # Signal Number 5: SIGTRAP
    sig_id  = 5

    # Open core file
    with open(os.path.join(filepath,'core-%s.img' % pid), mode='rb') as f:
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

    with open(os.path.join(filepath,'core-%s.img' % pid), mode='rb+') as f:
        pycriu.images.dump(core_img, f)

# Calculate the number of pages required for the sighandler library

def calculate_num_pages(lib_path):
    min_vaddr = 65535 #UINTPTR_MAX
    max_vaddr = 0
    with open(lib_path, 'rb') as f:
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

# Create the VMA item to be inserted into the MM image

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

# Create the pagemap item to be inserted into the PAGEMAP image

def create_vma_item_pagemap(start_address, nr_pages):
    item =  {
                "vaddr": start_address,
                "nr_pages": nr_pages,
                "flags": "PE_PRESENT"
            }
    return item

# Utility function to create the protection flag list for a page

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

# Add the VMAs into the MM mage and the PAGEMAP image

def create_vmas(libpath, start_address, file_id):
    vma_list_mm = []
    vma_list_pgmap = []
    vma_start = start_address
    with open(libpath, 'rb') as f:
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

# Create the pages for the virtual region

def add_pages(filepath, libpath,  num_pages):

    f_zeros = open(os.path.join(filepath, 'zeros'), 'wb+')
    f_zeros.write(b'\x00' * num_pages * 4096)
    write_flag = 0
    zeros_buf = b'\x00' * 9
    with open(libpath, 'rb') as f:
        elffile = ELFFile(f)
        for segment in elffile.iter_segments():
            address = segment.header['p_vaddr']
            if(segment.header.p_type == 'PT_LOAD'):
                f_zeros.seek(address, 0)
                f_zeros.write(segment.data())
                f_zeros.seek(0)

                # To write the restorer code in the pages-1.img
                if(segment.header['p_flags'] == 5 and (write_flag == 0)):
                    data_size = segment.header['p_memsz']
                    sigreturn_offset = address + data_size + 1
                    #TODO: Add condition to check to page overflow
                    f_zeros.seek(sigreturn_offset, 0)
                    buf = f_zeros.read(9)
                    if(buf == zeros_buf):
                        # Check for page overflow
                        if(page_end(sigreturn_offset + 9) == page_end(sigreturn_offset)):
                            f_zeros.seek(sigreturn_offset, 0)
                            f_zeros.write(b'\x48\xc7\xc0\x0f\x00\x00\x00\x0f\x05')
                            write_flag = 1
    
    f_zeros.close()
    return sigreturn_offset

# To perform global data and PLT relocations

def perform_relocations(libpath, filepath, vma_start_address, library_address, libc_path):
    
    f_zeros = open(os.path.join(filepath, 'zeros'), 'rb+')
    with open(libpath, 'rb') as f:
        elffile = ELFFile(f) 
        # Get the dynamic segment from the elf (to read DT_SYMTAB)
        for segment in elffile.iter_segments():
                if isinstance(segment, DynamicSegment):
                    dynamic_segment = segment
        reladyn_name = '.rela.dyn'
        reladyn = elffile.get_section_by_name(reladyn_name)
        # Get all relocations to be performed from the .rela.dyn section
        for reloc in reladyn.iter_relocations():
            # Get symbol index from relocation information
            index = reloc['r_info_sym']
            # Get type of relocation from relocation information
            reloc_type = reloc['r_info_type']
            # Get offset at which relocation has to be performed
            symbol_offset = reloc['r_offset']
            # Get symbol object from DT_SYMTAB section
            symbol = dynamic_segment.get_symbol(index)
            if(reloc_type == 6): #R_X86_64_GLOB_DAT
                # Perform the relocation
                address_to_write = symbol.entry['st_value'] + int(vma_start_address, 16)
                f_zeros.seek(symbol_offset, 0)
                f_zeros.write(struct.pack('<Q', address_to_write))
    
        # Get the GNUHash section from libc
        with open(libc_path, 'rb') as lib_f:
            libelffile = ELFFile(lib_f)
            for section in libelffile.iter_sections():
                if isinstance(section, GNUHashSection):
                    hash_section = section
            # Get all relocations to be performed from the .rela.plt section
            relaplt_name = '.rela.plt'
            relaplt = elffile.get_section_by_name(relaplt_name)
            for reloc in relaplt.iter_relocations():
                index = reloc['r_info_sym']
                # Get type of relocation from relocation information
                reloc_type = reloc['r_info_type']
                # Get offset at which relocation has to be performed
                symbol_offset = reloc['r_offset']
                # Get symbol object from DT_SYMTAB section
                symbol = dynamic_segment.get_symbol(index)
                if(reloc_type == 7): #R_X86_64_JUMP_SLO
                    # Perform the relocation
                    # Address to write calculation: Find the offset of the PLT function from the 
                    # GNUHash section and add it to the base address of libc
                    address_to_write = hash_section.get_symbol(symbol.name).entry['st_value'] + library_address
                    f_zeros.seek(symbol_offset, 0)
                    f_zeros.write(struct.pack('<Q', address_to_write))
    
    f_zeros.close()

# Utility function that calls other functions to modify the binary image of dump

def modify_binary_image(filepath, libpath, library_address, vma_start_address, libc_path):
    num_pages = calculate_num_pages(libpath)
    sigreturn_offset = add_pages(filepath, libpath, num_pages)
    perform_relocations(libpath, filepath, vma_start_address, library_address, libc_path)
    return num_pages, sigreturn_offset

# Dump the modfied images back to the dump files

def dump_new_images(mm_img, pgmap_img, mm_file, pgmap_file, filepath):
    
    with open(os.path.join(filepath, mm_file[0]), mode='rb+') as mm_file_write:
            pycriu.images.dump(mm_img, mm_file_write)
    
    with open(os.path.join(filepath, pgmap_file[0]), mode='rb+') as pgmap_file_write:
            pycriu.images.dump(pgmap_img, pgmap_file_write)

# Find the offset at which to add the pages of sighandler into the original dump

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

# Config handler adds trap in the target library and creates the config.h and config_base.h files

def config_add_sig_handler(filepath, library_address_trap, jump_address, pid):
    config_list = ''
    # Write offset address to header file
    with open(os.path.join(filepath, 'config_base.h'), 'wb+') as config_base_file:
        config_base_file.write(hex(library_address_trap))

    with open(os.path.join(filepath, 'trap_locations')) as trap_locations_file:
        trap_contents = trap_locations_file.read()
        contents_list = trap_contents.splitlines()
    
    for i in range(len(contents_list)):
        trap_address = library_address_trap + int(contents_list[i], 16)
        offset_to_write = (jump_address - trap_address) - 1
        if i:
            config_list+= ','
        config_list += '{{ {0},{1} }}'.format(contents_list[i], offset_to_write)
        #Add traps in the binary
        pycriu.process_edit.pedit_update_a_byte(filepath, library_address_trap, int(contents_list[i], 16), pid, 0xCC)
    
    with open(os.path.join(filepath, 'config.h'), 'wb+') as config_file:
        config_file.write("%s" % config_list)

# Main function to add signal handler into the original image
def add_signal_handler(filepath, libpath, handler_address,\
                    vma_start_address, library_address, libc_path, pid):

    pgmap_file, mm_file = pycriu.utils.open_files(filepath, pid)
    pgmap_img, mm_img = pycriu.utils.readImages(pid, filepath)

    pgmap_list = pgmap_img['entries']
    mm_list = mm_img['entries']

    pages_id = pgmap_list[0]['pages_id']

    file_id = modify_files_img(filepath, libpath)
    vma_list_mm, vma_list_pgmap = create_vmas(libpath, int(vma_start_address, 16), file_id)
    num_pages, sigreturn_offset = modify_binary_image(filepath, libpath, int(library_address), vma_start_address, libc_path)
    sigreturn_address = sigreturn_offset + int(vma_start_address, 16)
    modify_core_img(filepath, handler_address, sigreturn_address, pid)

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

    # Dump modified images
    dump_new_images(mm_img, pgmap_img, mm_file, pgmap_file, filepath)

    # Calculate the position at which the signal handler pages need to be added
    binary_offset = append_at_location(pgmap_img['entries'], vma_start_address)

    # Copy data from offset to temp file
    with open(os.path.join(filepath, 'pages-%s.img' % pages_id), mode='r+b') as pg_file,\
         open(os.path.join(filepath, "temp"), "wb+") as temp:
            pg_file.seek(binary_offset, 0)
            temp.write(pg_file.read())

    # Write pages to pages-img 
    with open(os.path.join(filepath, "zeros"), "rb") as myfile,\
         open(os.path.join(filepath, 'pages-%s.img' % pages_id), mode='r+b') as file2:
            file2.seek(binary_offset)
            file2.write(myfile.read())
    
    # Append zeros to the file
    with open(os.path.join(filepath, 'pages-%s.img' % pages_id), mode='r+b') as myfile,\
         open(os.path.join(filepath, "temp"), "rb") as file2:
        myfile.seek(binary_offset + (num_pages * 4096), 0)
        myfile.write(file2.read())

    # Delete zeros and temp file
    os.remove(os.path.join(filepath, 'zeros'))
    os.remove(os.path.join(filepath, 'temp'))

    print('Done')

