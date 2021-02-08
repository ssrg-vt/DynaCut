### File with utility functions for added features

import pycriu
import os
import fnmatch 

# Get files from dump folder
def open_files(filepath):
    """
    This function returns a list of the filenames to match pagemap, mm 
    and pages image file 
    """
    pgmap_file = fnmatch.filter(os.listdir(filepath), 'pagemap-*.img')
    mm_file = fnmatch.filter(os.listdir(filepath), 'mm-*.img')
    pages_file = fnmatch.filter(os.listdir(filepath), 'pages-*.img')

    return pgmap_file, mm_file, pages_file

def readImages(pgmap_file, mm_file, filepath):
    """
    This function reads and returns the pgmap_img and mm_img 
    """
    if not pgmap_file:
        raise Exception("crit: addvma: no pagemap file found (empty dump folder?) \n")
    if not mm_file:
        raise Exception("crit: addvma: no mm image file found (empty dump folder?) \n")

    # Open PAGEMAP image
    with open(os.path.join(filepath,pgmap_file[0]), mode='rb') as f:
        pgmap_img = pycriu.images.load(f)

    # Open MM image
    with open(os.path.join(filepath,mm_file[0]), mode='rb') as f:
        mm_img = pycriu.images.load(f)
    
    return pgmap_img, mm_img