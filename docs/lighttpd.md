# Remove initialization code of Lighttpd
## Build Lighttpd from source
Under `DynaCut` root directory:
```
❯ cd tests/lighttpd
❯ ./build_lighttpd.sh
```
Run Lighttpd server:
```
❯ ./run_lighttpd.sh
##
## Basic lighttpd configuration.
... ...
2022-03-18 17:29:54: server.c.1513) server started (lighttpd/1.4.59)
```

## Lighttpd initialization code profiling
Running the `tracediff.py` tool to generate a list of init code locations. Find only code locations that belong to the lighttpd code segment:
```
❯ ../../tools/scripts/tracediff.py -u drcov.lighttpd.488622.0000.proc.log -b drcov.lighttpd.488622.0001.proc.log | grep "\[  5\]:" | awk '{print substr($4, 1, length($4)-1)}' > lighttpd-init.log.0
```

Dump the code segment start address:
```
❯ ./criu/crit/crit x lighttpd.img mems
489967
	exe                                     /home/xiaoguang/works/proc-edit/DynaCut/tests/lighttpd/lighttpd-1.4.59/src/lighttpd
	5607c229a000-5607c22a6000           r-- /home/xiaoguang/works/proc-edit/DynaCut/tests/lighttpd/lighttpd-1.4.59/src/lighttpd
	5607c22a6000-5607c22fa000           r-x /home/xiaoguang/works/proc-edit/DynaCut/tests/lighttpd/lighttpd-1.4.59/src/lighttpd + 0xc000
... ...
```

Apply the process rewriting command using the init code log and the Lighttpd code start address. We can also get a list of code locations and the bytes replaced.
```
❯ ./criu/crit/crit edit rm init lighttpd.img 5607c22a6000 -file ./tests/lighttpd/lighttpd-init.log.0 > lighttpd.h
```

Generate code init code removal verifier (a signal handler):
```
❯ mv lighttpd.h tests/sighandler/init_addr_map.h
❯ make -C tests/sighandler init_removal_verifier.so
... ...
gcc -shared -Wall -fPIC -g -o init_removal_verifier.so init_removal_verifier.c
```

Insert this signal handler:
```
❯ ./criu/crit/crit edit insert sighandler lighttpd.img 0x1000000 -path $PWD/tests/sighandler/init_removal_verifier.so
16777216
0x01001179
The entry function trap_handler() offset @0x1179 VA @0x1001179 (/home/xiaoguang/works/proc-edit/DynaCut/tests/sighandler/init_removal_verifier.so)
Done
```

Manually update the process image to make the code writable.

Restore the process image and you will get an allowlist of code locations that should not be in the initialization code (in `./tests/lighttpd/allowlist.txt`).
```
❯ ./tools/scripts/restore.sh lighttpd.img
```
