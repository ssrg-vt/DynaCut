#-------------------------------------------------------------------------------
# Created by Abhijit Mahurkar
# Module to unmap VMAs from a process image
# abhijitm@vt.edu
#-------------------------------------------------------------------------------
from __future__ import print_function

import os
import pycriu
import pycriu.add_sig_handler
from operator import itemgetter

def find_offset(pgmap_list, vma_address):
    pg_offset = 0
    binary_offset = 0
    for i in range(1, len(pgmap_list)):
        pages = pgmap_list[i]["nr_pages"]
        for key in pgmap_list[i]:
            if(key == "vaddr"):
                map_address = pgmap_list[i][key]
                if(map_address <= vma_address < (map_address + pages * 4096)):
                  print('Inside if')
                  binary_offset = pg_offset + (vma_address - map_address)
                  print(binary_offset)
                  return binary_offset
        pg_offset = pg_offset + (4096 * pages) 

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
   print(item)
   return item

def create_vma_item_pagemap(start_address, nr_pages):
    item =  {
                "vaddr": start_address,
                "nr_pages": nr_pages,
                "flags": "PE_PRESENT"
            }
    print(item)
    return item


def modify_vma(mm_list, vma_address, num_pages):
   
   # Initial iteration to remove mm entry
   new_vma_list = [i for i in mm_list if not (i['start'] <= vma_address < i['end'])]
   
   for entry in mm_list:
      start_address = entry['start']
      end_address = entry['end']
      offset = entry['pgoff']
      if(start_address == vma_address):
         offset_vma1 = offset + num_pages * 4096
         start_address_vma1 = start_address + num_pages * 4096
         print(start_address_vma1)
         end_address_vma1 = end_address
         new_vma_list.append(create_vma_item(offset_vma1,start_address_vma1, end_address_vma1,\
            entry['prot'], entry['shmid']))
      elif(start_address < vma_address < end_address):
         start_address_vma1 = start_address
         print(start_address_vma1)
         offset_vma1 = offset
         offset_vma2 = offset + (vma_address - start_address) + num_pages * 4096
         end_address_vma1 = vma_address
         start_address_vma2 = vma_address + num_pages * 4096
         end_address_vma2 = end_address 
         new_vma_list.append(create_vma_item(offset_vma1,start_address_vma1, end_address_vma1,\
            entry['prot'], entry['shmid']))
         new_vma_list.append(create_vma_item(offset_vma2,start_address_vma2, end_address_vma2,\
            entry['prot'], entry['shmid']))
   
   return sorted(new_vma_list, key=itemgetter("start"))

def modify_pagemap(pgmap_list, vma_address, num_pages):

   #print('vanilla',pgmap_list)
   # Check if page is mapped 
   flag = 0
   for i in range(1, len(pgmap_list)):
      vaddr = pgmap_list[i]['vaddr']
      nr_pages = pgmap_list[i]['nr_pages']
      if ((vaddr == vma_address) or (vaddr < vma_address < (vaddr + nr_pages * 4096))):
         flag = 1
   if not flag:
      raise Exception ("Page is not mapped")
      
   copy_payload = pgmap_list[0]
   new_pgmap_list = [i for i in pgmap_list[1:] if not (i['vaddr'] <= vma_address\
       < (i['vaddr'] + 4096 * i['nr_pages']))]
   #print('delete',pgmap_list)
   for i in range(1,len(pgmap_list)):
      vaddr = pgmap_list[i]['vaddr']
      nr_pages = pgmap_list[i]['nr_pages']
      if(vaddr == vma_address):
         if(num_pages > nr_pages):
            raise Exception("num pages exceeds nr_pages for the pagemap entry")
         vaddr_vma1 = vma_address + 4096 * num_pages
         nr_pages_vma1 = nr_pages - num_pages
         new_pgmap_list.append(create_vma_item_pagemap(vaddr_vma1, nr_pages_vma1))
      elif(vaddr < vma_address < (vaddr + nr_pages * 4096)):
         if(num_pages > nr_pages):
            raise Exception("num pages exceeds nr_pages for the pagemap entry")
         vaddr_vma1 = vaddr
         nr_pages_vma1 = ((vma_address - vaddr) / 4096)
         vaddr_vma2 = vma_address + num_pages * 4096
         #if((vma_address - vaddr) / 4096) 
         nr_pages_vma2 = nr_pages - num_pages - ((vma_address - vaddr) / 4096)
         if(nr_pages_vma2 < 0):
            print('Cannot remove %d pages from specified VMA address' % (num_pages))
            print('Pagemap image from chosen VMA address has only '\
               '%d pages mapped -> reduce the number of pages to be removed'%\
                (nr_pages - ((vma_address - vaddr) / 4096)))
            raise Exception("reduce the number of pages to be removed")
         new_pgmap_list.append(create_vma_item_pagemap(vaddr_vma1, nr_pages_vma1))
         new_pgmap_list.append(create_vma_item_pagemap(vaddr_vma2, nr_pages_vma2))
   
   new_pgmap_list = sorted(new_pgmap_list, key=itemgetter("vaddr"))
   new_pgmap_list.insert(0,copy_payload)
   return new_pgmap_list

def unmap_vmas(filepath, pid, vma_address, num_pages):
   pgmap_img, mm_img = pycriu.utils.readImages(pid, filepath)

   pgmap_list = pgmap_img['entries']
   mm_list = mm_img['entries'][0]['vmas']

   pages_id = pgmap_list[0]['pages_id']

   binary_offset = find_offset(pgmap_img['entries'], int(vma_address, 16))
   print('the binary offset is:', binary_offset)
   new_pgmap_list = modify_pagemap(pgmap_list, int(vma_address, 16), int(num_pages))
   new_vma_list = modify_vma(mm_list, int(vma_address, 16), int(num_pages))

   #print(new_pgmap_list)
   #print(new_vma_list)
   pgmap_img['entries'] = new_pgmap_list
   mm_img['entries'][0]['vmas'] = new_vma_list

   with open(os.path.join(filepath, 'pagemap-%s.img' % pid), mode='r+b') as pgmap_file_write:
         pycriu.images.dump(pgmap_img, pgmap_file_write)

   with open(os.path.join(filepath, 'mm-%s.img' % pid), mode='r+b') as mm_file_write:
         pycriu.images.dump(mm_img, mm_file_write)

   with open(os.path.join(filepath, 'pages-%s.img' % pages_id), mode='r+b') as pg_file,\
      open(os.path.join(filepath, "temp1"), "wb+") as temp:
         pg_file.seek(0, 0)
         temp.write(pg_file.read(binary_offset))

   with open(os.path.join(filepath, 'pages-%s.img' % pages_id), mode='r+b') as pg_file,\
      open(os.path.join(filepath, "temp2"), "wb+") as temp:
         pg_file.seek(binary_offset + (int(num_pages) * 4096), 0)
         temp.write(pg_file.read())
   
   os.remove(os.path.join(filepath, 'pages-%s.img' % pages_id))

   # Append zeros to the file
   with open(os.path.join(filepath, 'pages-%s.img' % pages_id), mode='wb+') as myfile,\
      open(os.path.join(filepath, "temp1"), "rb") as file1,\
         open(os.path.join(filepath, "temp2"), "rb") as file2:
      myfile.seek(0,0)
      myfile.write(file1.read())
      myfile.seek(binary_offset, 0)
      myfile.write(file2.read())

   # Delete zeros and temp file
   #os.remove(os.path.join(filepath, 'temp1'))
   #os.remove(os.path.join(filepath, 'temp2'))
