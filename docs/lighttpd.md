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

```
❯ ../../tools/scripts/tracediff.py -u drcov.lighttpd.488622.0000.proc.log -b drcov.lighttpd.488622.0001.proc.log | grep "\[  5\]:" | awk '{print substr($4, 1, length($4)-1)}' > lighttpd-init.log.0
```


```
❯ ./criu/crit/crit x lighttpd.img mems
489967
	exe                                     /home/xiaoguang/works/proc-edit/DynaCut/tests/lighttpd/lighttpd-1.4.59/src/lighttpd
	5607c229a000-5607c22a6000           r-- /home/xiaoguang/works/proc-edit/DynaCut/tests/lighttpd/lighttpd-1.4.59/src/lighttpd
	5607c22a6000-5607c22fa000           r-x /home/xiaoguang/works/proc-edit/DynaCut/tests/lighttpd/lighttpd-1.4.59/src/lighttpd + 0xc000
... ...
```