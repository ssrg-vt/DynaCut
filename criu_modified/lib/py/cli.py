from __future__ import print_function
from __future__ import unicode_literals

import argparse
import json
import os
import re
import sys

import pycriu
import pycriu.add_sig_handler
import pycriu.disasm_pages
import pycriu.process_edit


def inf(opts):
    if opts['in']:
        return open(opts['in'], 'rb')
    else:
        return sys.stdin


def outf(opts):
    if opts['out']:
        return open(opts['out'], 'w+')
    else:
        return sys.stdout


def dinf(opts, name):
    return open(os.path.join(opts['dir'], name))


def decode(opts):
    indent = None

    try:
        img = pycriu.images.load(inf(opts), opts['pretty'], opts['nopl'])
    except pycriu.images.MagicException as exc:
        print("Unknown magic %#x.\n"\
          "Maybe you are feeding me an image with "\
          "raw data(i.e. pages.img)?" % exc.magic, file=sys.stderr)
        sys.exit(1)

    if opts['pretty']:
        indent = 4

    f = outf(opts)
    json.dump(img, f, indent=indent)
    if f == sys.stdout:
        f.write("\n")

def get_default_arg(opts, arg, default=""):
	if opts[arg]:
		return opts[arg]
	return default
def addvma(opts):
    start_address=get_default_arg(opts, 'startaddress', "0x1000")
    directory=get_default_arg(opts, 'directory', "./")
    end_address=get_default_arg(opts, 'endaddress', "0x5000")
    if(((int(end_address, 16) - int(start_address, 16)) % 4096) != 0):
         raise Exception("VMA region is not a multiple of 4k")
    nr_pages= (int(end_address, 16) - int(start_address, 16))/4096
    pycriu.add_vmas.add_vma_regions(start_address, end_address, nr_pages, directory)

def mb(opts):
    start_address=opts['address']
    if not start_address:
        raise Exception("Address cannot be empty!")
    directory=get_default_arg(opts, 'directory', "./")
    pycriu.process_edit.modify_binary(directory, start_address)

def mbd(opts):
    start_address=opts['startaddress']
    if not start_address:
        raise Exception("Start address cannot be empty!")
    directory=get_default_arg(opts, 'directory', "./")
    offset=opts['offset']
    if not offset:
        raise Exception("Offset address cannot be empty!")
    pycriu.process_edit.modify_binary_dynamic(directory, int(start_address, 16), int(offset, 16))

def disasm(opts):
    directory=get_default_arg(opts, 'directory', "./")
    pycriu.disasm_pages.disassemblePages(directory)

def encode(opts):
    img = json.load(inf(opts))
    pycriu.images.dump(img, outf(opts))


def info(opts):
    infs = pycriu.images.info(inf(opts))
    json.dump(infs, sys.stdout, indent=4)
    print()


def get_task_id(p, val):
    return p[val] if val in p else p['ns_' + val][0]


#
# Explorers
#


class ps_item:
    def __init__(self, p, core):
        self.pid = get_task_id(p, 'pid')
        self.ppid = p['ppid']
        self.p = p
        self.core = core
        self.kids = []


def show_ps(p, opts, depth=0):
    print("%7d%7d%7d   %s%s" %
          (p.pid, get_task_id(p.p, 'pgid'), get_task_id(p.p, 'sid'), ' ' *
           (4 * depth), p.core['tc']['comm']))
    for kid in p.kids:
        show_ps(kid, opts, depth + 1)


def explore_ps(opts):
    pss = {}
    ps_img = pycriu.images.load(dinf(opts, 'pstree.img'))
    for p in ps_img['entries']:
        core = pycriu.images.load(
            dinf(opts, 'core-%d.img' % get_task_id(p, 'pid')))
        ps = ps_item(p, core['entries'][0])
        pss[ps.pid] = ps

    # Build tree
    psr = None
    for pid in pss:
        p = pss[pid]
        if p.ppid == 0:
            psr = p
            continue

        pp = pss[p.ppid]
        pp.kids.append(p)

    print("%7s%7s%7s   %s" % ('PID', 'PGID', 'SID', 'COMM'))
    show_ps(psr, opts)


files_img = None


def ftype_find_in_files(opts, ft, fid):
    global files_img

    if files_img is None:
        try:
            files_img = pycriu.images.load(dinf(opts, "files.img"))['entries']
        except:
            files_img = []

    if len(files_img) == 0:
        return None

    for f in files_img:
        if f['id'] == fid:
            return f

    return None


def ftype_find_in_image(opts, ft, fid, img):
    f = ftype_find_in_files(opts, ft, fid)
    if f:
        return f[ft['field']]

    if ft['img'] is None:
        ft['img'] = pycriu.images.load(dinf(opts, img))['entries']
    for f in ft['img']:
        if f['id'] == fid:
            return f
    return None


def ftype_reg(opts, ft, fid):
    rf = ftype_find_in_image(opts, ft, fid, 'reg-files.img')
    return rf and rf['name'] or 'unknown path'

def ftype_reg2(opts, ft, fid):
    rf = ftype_find_in_image(opts, ft, fid, 'files.img')
    return rf and rf['name'] or 'unknown path'

def ftype_pipe(opts, ft, fid):
    p = ftype_find_in_image(opts, ft, fid, 'pipes.img')
    return p and 'pipe[%d]' % p['pipe_id'] or 'pipe[?]'


def ftype_unix(opts, ft, fid):
    ux = ftype_find_in_image(opts, ft, fid, 'unixsk.img')
    if not ux:
        return 'unix[?]'

    n = ux['name'] and ' %s' % ux['name'] or ''
    return 'unix[%d (%d)%s]' % (ux['ino'], ux['peer'], n)


file_types = {
    'REG': {
        'get': ftype_reg,
        'img': None,
        'field': 'reg'
    },
    'PIPE': {
        'get': ftype_pipe,
        'img': None,
        'field': 'pipe'
    },
    'UNIXSK': {
        'get': ftype_unix,
        'img': None,
        'field': 'usk'
    }
}


def ftype_gen(opts, ft, fid):
    return '%s.%d' % (ft['typ'], fid)


files_cache = {}


def get_file_str(opts, fd):
    key = (fd['type'], fd['id'])
    f = files_cache.get(key, None)
    if not f:
        ft = file_types.get(fd['type'], {'get': ftype_gen, 'typ': fd['type']})
        f = ft['get'](opts, ft, fd['id'])
        files_cache[key] = f

    return f


def explore_fds(opts):
    ps_img = pycriu.images.load(dinf(opts, 'pstree.img'))
    for p in ps_img['entries']:
        pid = get_task_id(p, 'pid')
        idi = pycriu.images.load(dinf(opts, 'ids-%s.img' % pid))
        fdt = idi['entries'][0]['files_id']
        fdi = pycriu.images.load(dinf(opts, 'fdinfo-%d.img' % fdt))

        print("%d" % pid)
        for fd in fdi['entries']:
            print("\t%7d: %s" % (fd['fd'], get_file_str(opts, fd)))

        fdi = pycriu.images.load(dinf(opts, 'fs-%d.img' % pid))['entries'][0]
        print("\t%7s: %s" %
              ('cwd', get_file_str(opts, {
                  'type': 'REG',
                  'id': fdi['cwd_id']
              })))
        print("\t%7s: %s" %
              ('root', get_file_str(opts, {
                  'type': 'REG',
                  'id': fdi['root_id']
              })))


class vma_id:
    def __init__(self):
        self.__ids = {}
        self.__last = 1

    def get(self, iid):
        ret = self.__ids.get(iid, None)
        if not ret:
            ret = self.__last
            self.__last += 1
            self.__ids[iid] = ret

        return ret


def explore_mems(opts):
    ps_img = pycriu.images.load(dinf(opts, 'pstree.img'))
    vids = vma_id()
    for p in ps_img['entries']:
        pid = get_task_id(p, 'pid')
        mmi = pycriu.images.load(dinf(opts, 'mm-%d.img' % pid))['entries'][0]

        print("%d" % pid)
        print("\t%-36s    %s" % ('exe',
                                 get_file_str(opts, {
                                     'type': 'REG',
                                     'id': mmi['exe_file_id']
    
                                 })))
        for vma in mmi['vmas']:
            st = vma['status']
            if st & (1 << 10):
                fn = ' ' + 'ips[%lx]' % vids.get(vma['shmid'])
            elif st & (1 << 8):
                fn = ' ' + 'shmem[%lx]' % vids.get(vma['shmid'])
            elif st & (1 << 11):
                fn = ' ' + 'packet[%lx]' % vids.get(vma['shmid'])
            elif st & ((1 << 6) | (1 << 7)):
                fn = ' ' + get_file_str(opts, {
                    'type': 'REG',
                    'id': vma['shmid']
                })
                if vma['pgoff']:
                    fn += ' + %#lx' % vma['pgoff']
                if st & (1 << 7):
                    fn += ' (s)'
            elif st & (1 << 1):
                fn = ' [stack]'
            elif st & (1 << 2):
                fn = ' [vsyscall]'
            elif st & (1 << 3):
                fn = ' [vdso]'
            elif vma['flags'] & 0x0100:  # growsdown
                fn = ' [stack?]'
            else:
                fn = ''

            if not st & (1 << 0):
                fn += ' *'

            prot = vma['prot'] & 0x1 and 'r' or '-'
            prot += vma['prot'] & 0x2 and 'w' or '-'
            prot += vma['prot'] & 0x4 and 'x' or '-'

            astr = '%08lx-%08lx' % (vma['start'], vma['end'])
            print("\t%-36s%s%s" % (astr, prot, fn))


def explore_rss(opts):
    ps_img = pycriu.images.load(dinf(opts, 'pstree.img'))
    for p in ps_img['entries']:
        pid = get_task_id(p, 'pid')
        vmas = pycriu.images.load(dinf(opts, 'mm-%d.img' %
                                       pid))['entries'][0]['vmas']
        pms = pycriu.images.load(dinf(opts, 'pagemap-%d.img' % pid))['entries']

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


explorers = {
    'ps': explore_ps,
    'fds': explore_fds,
    'mems': explore_mems,
    'rss': explore_rss
}


def explore(opts):
    explorers[opts['what']](opts)

# Print shared library info for a library
def sli(opts):
    vstr = ''
    flag = 0
    shared_library_name = opts['library_name']
    ps_img = pycriu.images.load(dinf(opts, 'pstree.img'))
    for p in ps_img['entries']:
        pid = get_task_id(p, 'pid')
        vmas = pycriu.images.load(dinf(opts, 'mm-%d.img' %
                                       pid))['entries'][0]['vmas']
    
    with open(os.path.join(opts['dir'], 'files.img')) as ffile:
        files_img = pycriu.images.load(ffile)['entries']
    
    for vma in vmas[0:]:
        for files in files_img:
            if (files['id'] == vma['shmid']):
                if(files['type'] == "REG"):
                    file_name = files['reg']['name']
                    if shared_library_name in file_name:
                        vstr += ' %08lx / %-8d' % (
                                    vma['start'], (vma['end'] - vma['start']) >> 12)
                        
                        prot = vma['prot'] & 0x1 and 'r' or '-'
                        prot += vma['prot'] & 0x2 and 'w' or '-'
                        prot += vma['prot'] & 0x4 and 'x' or '-'

                        astr = '%08lx-%08lx' % (vma['start'], vma['end'])
                        print("\t%-36s%s%s" % (astr, prot, file_name))
                        flag = 1
    if not flag:
            print("No matching vma entry found for: ", shared_library_name)

# Find the base address of a library given the name 
def find_lib_offset(opts, name):
    vma_address = 0
    ps_img = pycriu.images.load(dinf(opts, 'pstree.img'))
    with open(os.path.join(opts['dir'], 'files.img')) as ffile:
        files_img = pycriu.images.load(ffile)['entries']
    for p in ps_img['entries']:
        pid = get_task_id(p, 'pid')
        vmas = pycriu.images.load(dinf(opts, 'mm-%d.img' %
                                       pid))['entries'][0]['vmas']
    for vma in vmas[0:]:
        for files in files_img:
            if (files['id'] == vma['shmid']):
                if(files['type'] == "REG"):
                    file_name = files['reg']['name']
                    if name in file_name:
                        vma_address = vma['start']
                        return vma_address
    return 0

# Driver function for config handler
def config_handler(opts):
    filepath = opts['dir']
    jump_offset = opts['jump_offset']
    library_address_trap = find_lib_offset(opts, opts['library_name'])
    jump_address = library_address_trap + int(jump_offset, 16)
    pycriu.add_sig_handler.config_add_sig_handler(filepath, library_address_trap, jump_address)

# Driver function for add signal handler
def add_sig_handler(opts):
    filepath = opts['dir']
    libpath = opts['lib_dir']
    handler_address = opts['handler_address']
    vma_start_address = opts['vma_start_address']
    
    if((int(vma_start_address, 16) % 4096) != 0):
        raise Exception("VMA start address is not 4k aligned")
    library_address_libc = find_lib_offset(opts, "libc-")
    pycriu.add_sig_handler.add_signal_handler(filepath, libpath, handler_address,\
                                                        vma_start_address, library_address_libc)

def main():
    desc = 'CRiu Image Tool'
    parser = argparse.ArgumentParser(
        description=desc, formatter_class=argparse.RawTextHelpFormatter)

    subparsers = parser.add_subparsers(
        help='Use crit CMD --help for command-specific help')

    # Decode
    decode_parser = subparsers.add_parser(
        'decode', help='convert criu image from binary type to json')
    decode_parser.add_argument(
        '--pretty',
        help=
        'Multiline with indents and some numerical fields in field-specific format',
        action='store_true')
    decode_parser.add_argument(
        '-i',
        '--in',
        help='criu image in binary format to be decoded (stdin by default)')
    decode_parser.add_argument(
        '-o',
        '--out',
        help='where to put criu image in json format (stdout by default)')
    decode_parser.set_defaults(func=decode, nopl=False)

    # Encode
    encode_parser = subparsers.add_parser('encode', help='convert criu image from json type to binary')
    encode_parser.add_argument('-i','--in',help='criu image in json format to be encoded (stdin by default)')
    encode_parser.add_argument('-o','--out',help='where to put criu image in binary format (stdout by default)')
    encode_parser.set_defaults(func=encode)

    # Info
    info_parser = subparsers.add_parser('info', help='show info about image')
    info_parser.add_argument("in")
    info_parser.set_defaults(func=info)

    # Explore
    x_parser = subparsers.add_parser('x', help='explore image dir')
    x_parser.add_argument('dir')
    x_parser.add_argument('what', choices=['ps', 'fds', 'mems', 'rss', 'sli'])
    x_parser.set_defaults(func=explore)

    # Show
    show_parser = subparsers.add_parser('show', help="convert criu image from binary to human-readable json")
    show_parser.add_argument("in")
    show_parser.add_argument('--nopl',help='do not show entry payload (if exists)',action='store_true')
    show_parser.set_defaults(func=decode, pretty=True, out=None)

    # Add VMAs
    addvma_parser = subparsers.add_parser('addvma',help='Adds VMA sections to CRIU images')
    addvma_parser.add_argument('-d','--directory', help='directory containing the images (local by default)')
    addvma_parser.add_argument('-sa','--startaddress', help='VMA start address (Default: 0x1000)')
    addvma_parser.add_argument('-ea','--endaddress', help='end address of VMA section (Default: 0x5000)')
    addvma_parser.set_defaults(func=addvma, nopl=False)

    #Disassemble binary
    disasm_parser = subparsers.add_parser('disasm',help='Disassembles code VMA sections in CRIU images')
    disasm_parser.add_argument('-d','--directory', help='directory containing the images (local by default)')
    disasm_parser.set_defaults(func=disasm, nopl=False)

    #Modify Binary
    mb_parser = subparsers.add_parser('mb',help='Writes INT3 to the specified offset location')
    mb_parser.add_argument('-d','--directory', help='directory containing the images (local by default)')
    mb_parser.add_argument('-a','--address', help='Address to be modified')
    mb_parser.set_defaults(func=mb, nopl=False)

    #Modify Binary Dynamic
    mbd_parser = subparsers.add_parser('mbd',help='Writes INT3 to the specified offset location for a dynamically linked binary')
    mbd_parser.add_argument('-d','--directory', help='directory containing the images (local by default)')
    mbd_parser.add_argument('-sa','--startaddress', help='VMA start address')
    mbd_parser.add_argument('-off', '--offset', help='Offset of the location from the beginning of the shared library')
    mbd_parser.set_defaults(func=mbd, nopl=False)

    shared_lib_info_parser = subparsers.add_parser('sli',help='Prints shared library info')
    shared_lib_info_parser.add_argument('-d','--dir', help='directory containing the images (local by default)')
    shared_lib_info_parser.add_argument('-name','--library_name', help='name of the shared library whose info is to be printed')
    shared_lib_info_parser.set_defaults(func=sli, nopl=False)


    config_parser = subparsers.add_parser('config',help='Configure the Dump for adding signal handler')
    config_parser.add_argument('-d','--dir', help='directory containing the CRIU images')
    config_parser.add_argument('-name','--library_name', help='Name of library where trap is to be inserted')
    config_parser.add_argument('-ja','--jump_offset', help='Jump offset of RIP')
    config_parser.set_defaults(func=config_handler, nopl=False)

    add_sig_handler_parser = subparsers.add_parser('ash',help='Adds sig handler into process image')
    add_sig_handler_parser.add_argument('-d','--dir', help='directory containing the CRIU images')
    add_sig_handler_parser.add_argument('-dl','--lib_dir', help='Path to the library that is to be loaded')
    add_sig_handler_parser.add_argument('-ha','--handler_address', help='Address of the signal handler')
    add_sig_handler_parser.add_argument('-vsa','--vma_start_address', help='VMA start address at which library has to be mapped')
    add_sig_handler_parser.set_defaults(func=add_sig_handler, nopl=False)

    opts = vars(parser.parse_args())


    if not opts:
        sys.stderr.write(parser.format_usage())
        sys.stderr.write("crit: error: too few arguments\n")
        sys.exit(1)

    opts["func"](opts)


if __name__ == '__main__':
    main()
