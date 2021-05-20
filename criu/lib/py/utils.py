### File with utility functions for added features

import pycriu
import os
import fnmatch 

# Get files from dump folder
def open_files(filepath, pid):
    """
    This function returns a list of the filenames to match pagemap, mm 
    and pages image file 
    """
    pgmap_file = fnmatch.filter(os.listdir(filepath), 'pagemap-%s.img' % pid)
    mm_file = fnmatch.filter(os.listdir(filepath), 'mm-%s.img' % pid)

    return pgmap_file, mm_file

def readImages(pid, filepath):
    """
    This function reads and returns the pgmap_img and mm_img 
    """

    # Open PAGEMAP image
    with open(os.path.join(filepath, 'pagemap-%s.img' % pid), mode='r+b') as f:
        pgmap_img = pycriu.images.load(f)

    # Open MM image
    with open(os.path.join(filepath, 'mm-%s.img' % pid), mode='r+b') as f:
        mm_img = pycriu.images.load(f)
    
    return pgmap_img, mm_img