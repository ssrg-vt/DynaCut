#!/usr/bin/python

## Utility to calculate unique basic blocks in unwanted feature logs but not in 
## wanted feature logs.
## Usage:  ./tracediff.py -u <unwanted feature log> -b <base log>

import sys,getopt

USAGE = """
USAGE: tracediff.py -u <unwanted feature log> -b <base log: wanted feature>
   or: tracediff.py -u <init log> -b <base log: exec log after init>
"""

# Read two logs, print lines that only belong to (unwanted) feature log
def feature_diff(featurelog, baselog):
    blog = open(baselog, "r")
    baseloglist = blog.readlines()
    blog.close()

    flog = open(featurelog, "r")
    line = flog.readline()
    print()
    cnt = 0
    while line:
        if line not in baseloglist:
            print("[{:3}] {}".format(cnt, line), end = '')
            cnt = cnt + 1
        line = flog.readline()
    flog.close()

def main(argv):
   unwanted_feature_log = ''
   base_log = ''
   type = 0
   try:
      opts, args = getopt.getopt(argv,"hu:b:",["unwanted-log","base-log="])
   except getopt.GetoptError:
      print(USAGE)
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print(USAGE)
         sys.exit()
      elif opt in ("-u", "--unwanted-log"):
         unwanted_feature_log = arg
      elif opt in ("-b", "--base-log"):
         base_log = arg
   
   print('The feature log file: {}'.format(unwanted_feature_log))
   print('The base log file: {}'.format(base_log))

   feature_diff(unwanted_feature_log, base_log)

if __name__ == "__main__":
   main(sys.argv[1:])
