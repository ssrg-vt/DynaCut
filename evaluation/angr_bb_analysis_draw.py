#!/usr/bin/env python3
# A script to dump function and basic block locations, size, etc.
# Install angr (https://docs.angr.io/introductory-errata/install) and matplotlib
# before use it.
import angr
import sys
import matplotlib.pyplot as plt

DEF_LOAD_BASE = 0x400000
GRAPH_WIDTH = 64  # width for data drawing

# mcf_s: line_width = 4, base = 0x1000
# lighttpd: line_width = 0.2, base = 0xc000
# x264: line_width = 0.2, base = 0x4000
line_width = 3
base = 0x1000

# Dump basic blocks [start, end]
def dump_functions_bbs(cfg):
  bb_list = {}
  # Functions are stored in a key-value dict (cfg.kb.functions)
  for key in cfg.kb.functions:
    # Iterate through all BBs in a function, print:
    # BB start addr | BB end addr
    for bb in cfg.kb.functions[key].blocks:
      bb_start_addr = int(bb.addr) - DEF_LOAD_BASE
      bb_end_addr = bb_start_addr + bb.size
      bb_list[bb_start_addr] = bb_end_addr
  return bb_list

# Draw all BBs
def draw(lines, width = 1, line_color='gray'):
  for line in lines:
    x = line[0]
    y = line[1]
    plt.plot(x, y, linestyle='-', color=line_color, linewidth=width)
  return

# Convert an address to a line
def addr2line(start, end, lines):
    width = 256  # width for data drawing
    x1 = start // width
    y1 = start % width
    x2 = end // width
    y2 = end % width
    if (x1 == x2 and y1 == y2):
        return
    if (x1 < x2):
        delta = x2 - x1
        #print(x1, y1, x1, width, start, end)
        lines.append([[x1, x1], [y1, width]])
        for i in range(1, delta):
            #print(x1+i, 0, x1+i, width)
            lines.append([[x1+i, x1+i], [0, width]])
        #print(x1+delta, 0, x1+delta, y2)
        lines.append([[x1+delta, x1+delta], [0, y2]])
    else:
        #print(x1, y1, x2, y2, start, end)
        lines.append([[x1, x1], [y1, y2]])
    return

# ./bb_draw <BIN> <Executed_BBs.log> (optional <Removed_BBs.log>)
# *.log files are a list of <BB offset, size>
# Executed_BBs.log: Executed BBs, from DrCOV   (in blue)
# Removed_BBs.log: init Removed BBs removed    (in red)
def main(argv):
  # 1. passing binary through argv[1] and load the binary to Angr
  if (len(argv) < 3):
    print("Usage %s <BIN> <Executed_BBs.log> (optional <Removed_BBs.log>)" % argv[0])
    return 1
  path_to_binary = argv[1]
  p = angr.Project(path_to_binary, load_options={'auto_load_libs': False})

  cfg = p.analyses.CFGFast()
  entry_func = cfg.kb.functions[p.entry]
  print(entry_func)

  # 2. Retrieve functions and basic blocks from the binary
  bb_list = dump_functions_bbs(cfg)

  base = sorted(bb_list)[0]
  print("Binary base address (1st address in the binary): ", hex(base))
  
  # 3. Convert addresses to lines and draw lines
  lines = []
  for start_addr in sorted(bb_list):
    addr2line(start_addr-base, bb_list[start_addr]-base, lines)
  draw(lines, line_width)

  # 4. Open the executed BB log and draw BLUE lines
  executed_trace_file = open(argv[2], "r")
  lines_exec = []
  for bb in executed_trace_file:
    start, size = bb.split()
    addr2line(int(start, 16)-base, int(start, 16)+int(size)-base, lines_exec)
    #print(int(start, 16), int(size), int(start, 16)+int(size))
  draw(lines_exec, line_width, "#0045A5")

  # 5. (optional) Open the removed BB log and draw RED lines
  if (len(argv) == 4):
    init_trace_file = open(argv[3], "r")
    lines_init = []
    for bb in init_trace_file:
      start, size = bb.split()
      addr2line(int(start, 16)-base, int(start, 16)+int(size)-base, lines_init)
      #print(int(start, 16), int(size), int(start, 16)+int(size))
    draw(lines_init, line_width, "#E24A33")

  # 6. Finish drawing, show it.
  print("Ready to show...")
  plt.axis('off')
  plt.show()

  return 0

if __name__ == '__main__':
  main(sys.argv)