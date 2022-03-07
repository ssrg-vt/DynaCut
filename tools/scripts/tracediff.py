#!/usr/bin/python

## Utility to calculate basic blocks of unwanted features from the wanted ones.
## Usage:  ./tracediff.py -u <unwanted feature log> -b <base log>

import sys,getopt
from enum import Enum

class LOG_TYPE(Enum):
   FEAT = 1
   INIT = 2

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

# Read two logs, print lines that only belong to init log
def init_diff(initlog, baselog):
   blog = open(baselog, "r")
   baseloglist = blog.readlines()
   blog.close()

   ilog = open(initlog, "r")
   line = ilog.readline()
   print()
   cnt = 0
   while line:
      if line not in baseloglist:
         print("[{:3}] {}".format(cnt, line), end = '')
         cnt = cnt + 1
      line = ilog.readline()
   ilog.close()

def main(argv):
   unwanted_feature_log = ''
   base_log = ''
   type = 0
   try:
      opts, args = getopt.getopt(argv,"hu:b:",["unwanted-log","base-log="])
   except getopt.GetoptError:
      print('tracediff.py -u <unwanted feature log> -b <base log>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('tracediff.py -u <unwanted feature log> -b <base log>')
         sys.exit()
      elif opt in ("-u", "--unwanted-log"):
         unwanted_feature_log = arg
         type = LOG_TYPE.FEAT
      elif opt in ("-i", "--init-log"):
         unwanted_feature_log = arg
         type = LOG_TYPE.INIT
      elif opt in ("-b", "--base-log"):
         base_log = arg
   
   print('The feature log file: {}'.format(unwanted_feature_log))
   print('The base log file: {}'.format(base_log))

   if (type == LOG_TYPE.FEAT):
      feature_diff(unwanted_feature_log, base_log)
   elif (type == LOG_TYPE.INIT):
      init_diff(unwanted_feature_log, base_log)


if __name__ == "__main__":
   main(sys.argv[1:])
