### Author: Abhijit Mahurkar
### Description: A tool to add VMA regions to a CRIU snapshot image


import pycriu
import fnmatch
import os
import sys
import struct
from operator import itemgetter

class Addvmas:
    def __init__(self):
		pass

    # Get files from dump folder
    def open_files(self, filepath):
        
        pgmap_file = fnmatch.filter(os.listdir(filepath), 'pagemap-*.img')
        mm_file = fnmatch.filter(os.listdir(filepath), 'mm-*.img')
        pages_file = fnmatch.filter(os.listdir(filepath), 'pages-*.img')
    
        return pgmap_file, mm_file, pages_file

    # Function to create a MM payload with start and end address of VMA region
    def create_mm_payload(self, vaddr1, vaddr2):
        payload = {\
                "start": int(vaddr1, 16),\
                "end":int(vaddr2, 16),\
                "pgoff":0,\
                "shmid":1,\
                "prot":"PROT_READ",\
                "flags": "MAP_PRIVATE",\
                "status":"VMA_AREA_REGULAR | VMA_FILE_PRIVATE",\
                "fd": -1,\
                "fdflags":"0x0"\
                }
        return payload

    # Function to create a PAGEMAP payload with start address and number of pages
    def create_pgmap_payload(self, vaddr1, nr_pages):
        payload = {\
                "vaddr":int(vaddr1, 16),\
                "nr_pages": nr_pages,\
                "flags": "PE_PRESENT"\
                }
        return payload

    def dump_new_images(self, mm_img, pgmap_img, mm_file, pgmap_file, filepath):

        with open(filepath + mm_file[0], mode='rb+') as mm_file_write:
            pycriu.images.dump(mm_img, mm_file_write)

        with open(filepath + pgmap_file[0], mode='rb+') as pgmap_file_write:
            pycriu.images.dump(pgmap_img, pgmap_file_write)

    # Modify binary
    def modify_binary(self, filepath, pages_file, nr_pages):
        
        with open(filepath + "zeros", mode='wb+') as f_zeros:
            f_zeros.seek(0)
            f_zeros.write(bytearray(int(nr_pages) * 4096))
        
        # Append zeros to the file
        with open(filepath + "zeros", "ab+") as myfile, open(filepath + pages_file[0], "rb") as file2:
            myfile.write(file2.read())

        # Delete original pages img without zeros
        os.remove(filepath + pages_file[0])

        # Rename zeros file to original file
        os.rename(filepath + "zeros", filepath + pages_file[0])


# Function to add VMA regions to MM image and Pagemap Image
def add_vma_regions(vaddr1, vaddr2, nr_pages, filepath):
    
    addvma = Addvmas()
    # Open files for reading
    pgmap_file, mm_file, pages_file = addvma.open_files(filepath)

    # Open PAGEMAP image
    with open(str(filepath + pgmap_file[0]), mode='rb') as f:
        pgmap_img = pycriu.images.load(f)

    # Open MM image
    with open(str(filepath + mm_file[0]), mode='rb') as f:
        mm_img = pycriu.images.load(f)

    pgmap_list = pgmap_img['entries']
    mm_list = mm_img['entries']

    # Copy first entry in pgmap_list to append later
    copy_payload = pgmap_list[0]

    # Create MM and pgmap payloads

    mm_payload = addvma.create_mm_payload(vaddr1, vaddr2)
    pgmap_payload = addvma.create_pgmap_payload(vaddr1, nr_pages)

    # Iterate over mm_list
    for index in range(len(mm_list)):
        for key in mm_list[index]:
            if(key == "vmas"):
                vma_list = mm_list[index][key]
                break

    # Insert payload and sort the mm list
    # (CRIU needs the list to be sorted)
    vma_list.insert(0, mm_payload)
    new_vma_list = sorted(vma_list, key=itemgetter('start'))

    # Insert the modfied list into mm_img
    for index in range(len(mm_list)):
        for key in mm_list[index]:
            if(key == "vmas"):
                mm_list[index][key] = new_vma_list
                break

    mm_img['entries'] = mm_list

    # Insert payload and sort the pgmap list
    pgmap_list.insert(1, pgmap_payload)
    new_pgmap_list = sorted(pgmap_list[1:], key=itemgetter('vaddr'))

    # Insert the first payload into the list
    new_pgmap_list.insert(0,copy_payload)

    # Append entries
    pgmap_img['entries'] = new_pgmap_list

    # Modify pages-1.img to add VMAs
    addvma.modify_binary(filepath, pages_file, nr_pages)
    
    # Dump images
    addvma.dump_new_images(mm_img, pgmap_img, mm_file, pgmap_file, filepath)
    print('Done')
