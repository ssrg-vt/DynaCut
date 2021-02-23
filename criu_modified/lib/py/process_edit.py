### A python module to edit a process image
### Author: Abhijit Mahurkar

import pycriu 
import pycriu.utils
import os

def dinf(opts, name):
    return open(os.path.join(opts['dir'], name))

def modify_binary(filepath, address):
    pgmap_file, mm_file, pages_file = pycriu.utils.open_files(filepath)
    pgmap_img, mm_img = pycriu.utils.readImages(pgmap_file, mm_file, filepath)
    pgmap_list = pgmap_img['entries']
    #mm_list = mm_img['entries']
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
    
    print(binary_offset)
    # Modify binary
    with open(os.path.join(filepath, pages_file[0]), mode='r+b') as f:
        f.seek((binary_offset),0)
        bytes_data = f.read(1)
        print(bytes_data.encode('hex'))
        f.seek(-1,1)
        f.write(b'\xCC')

def modify_binary_dynamic(filepath, address, library_offset):
    pgmap_file, mm_file, pages_file = pycriu.utils.open_files(filepath)
    pgmap_img, mm_img = pycriu.utils.readImages(pgmap_file, mm_file, filepath)
    pgmap_list = pgmap_img['entries']
    mm_list = mm_img['entries']
    mm_list_vmas = mm_list[0]['vmas']
    vmi = 0
    while mm_list_vmas[vmi]["start"] < int(address, 16):
        vmi+=1
    pg_offset = 0
    binary_offset = 0
    for i in range(1, len(pgmap_list)):
        pages = pgmap_list[i]["nr_pages"]
        for key in pgmap_list[i]:
            if(key == "vaddr"):
                map_address = pgmap_list[i][key]
                if(map_address <= int(address, 16) < (map_address + pages * 4096)):
                    print(mm_list_vmas[vmi]['pgoff'])
                    binary_offset = pg_offset + (int(address, 16) - map_address)\
                         + (int(library_offset, 16) - mm_list_vmas[vmi]['pgoff'])
                    print(pg_offset)
        pg_offset = pg_offset + (4096 * pages)
    
    print(binary_offset)
    # Modify binary
    with open(os.path.join(filepath, pages_file[0]), mode='r+b') as f:
        f.seek(binary_offset,0)
        bytes_data = f.read(1)
        print(bytes_data.encode('hex'))
        f.seek(-1,1)
        f.write(b'\xCC')

def shared_library_info(pgmap_list, mm_list, files_list):

        print("%d" % pid)
        vmi = 0
        pvmi = -1
        for pm in pms[1:]:
            pstr = '\t%lx / %-8d' % (pm['vaddr'], pm['nr_pages'])
            while vmas[vmi]['end'] <= pm['vaddr']:
                vmi += 1

            pme = pm['vaddr'] + (pm['nr_pages'] << 12)
            vstr = ''
            while vmas[vmi]['start'] < pme:
                vma = vmas[vmi]
                if vmi == pvmi:
                    vstr += ' ~'
                else:
                    vstr += ' %08lx / %-8d' % (
                        vma['start'], (vma['end'] - vma['start']) >> 12)
                    if vma['status'] & ((1 << 6) | (1 << 7)):
                        vstr += ' ' + get_file_str(opts, {
                            'type': 'REG',
                            'id': vma['shmid']
                        })
                    pvmi = vmi
                vstr += '\n\t%23s' % ''
                vmi += 1

            vmi -= 1

            print('%-24s%s' % (pstr, vstr))

