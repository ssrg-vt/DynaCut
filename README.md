# Dynamic and Adaptive Code Customization with Process Rewriting

This project aims to dynamically customize code of a running process. The major component is an extended CRIU/CRIT tool that can rewrite the saved process images.
This repo contains a modified version of CRIU that can edit a process, disable code path, and insert library pages to a process at arbitrary VMA location.

## Install pre-requisites, build CRIU and test examples

Apart from [the packages needed by Vanilla CRIU](https://criu.org/Installation), the following packages are required:
```
❯ pip install capstone pyelftools
```

Once you installed all the required packages, build the CRIU with:
```
❯ make -C criu
...
  LINK     lib/c/libcriu.so
  LINK     lib/c/libcriu.a
  GEN      lib/py/images/magic.py
```

Build the toy application with:
```
❯ make -C tests/example multi_path
```
We inserted `int3` on multiple places in this toy application (`multi_path`). Each `int3` code block indicates an unwanted feature that we don't want to touch. To disable that feature dynamically, we checkpoint the running process with CRIU and use our tool to inject a signal handler that skips the `int3` code blocks.

### Disable the `int3` code blocks with injected signal handler
First, we need to indentify the unwanted code block locations. You can use
`objdump -S <bin>` to find the `int3` code block location and the length. Fill
the value pairs to `tests/sighandler/config.h`. The following is an example:
```
❯ cat tests/sighandler/config.h
{0x229, 1}, {0x2265, 2}, {0x3b3, 3}
```
Next, build the signal handler:
```
❯ make -C tests/sighandler multi_path_sighandler
```

Now let's checkpoint a running process:
```
❯ ./tests/example/multi_path -n 7 &
pid: 43585, cnt: 7
1
2
3
[1]    43585 killed     ./tests/example/multi_path -n 7
❯ ./tools/scripts/dump.sh multi_path
```
The saved process image should be in `./vanilla-dump`.

Use the CRIT tool to rewrite the process image:
```
❯ ./criu/crit/crit ash -d vanilla-dump -dl $(pwd)/tests/sighandler/multi_sig.so -ha 0x7000001159 -vsa 0x7000000000
```

Let's restore the modified process:
```
❯ ./tools/scripts/restore.sh vanilla-dump
4 
5 
6 
7 
In function main, trap (int3) next ...

===trap_handler===
Signal #5. arr_len 3. rip: 0x55d3ece7e3b4
Found sig handler offset: 0x3b3. rip: ++3
Updated rip 0x55d3ece7e3b6
===trap_handler===

main: You cannot see me unless you use some tricks :)
```

## Example: adding a signal handler to a process

To add a signal handler as a library to a process, the following steps need to be followed: 

1. An example handler library and Makefile is provided in /PopSnapshot/tests/handler_example 

2. An example process to which this signal handler has been added is located in /PopSnapshot/tests/criu-example

4. Currently this method only supports handling the SIGTRAP signal

5. To insert traps in the binary, use the CRIT mbd option (`crit mbd -h`)

5. Example commands: 

`~/SSRG/PopSnapshot/criu/crit/crit mbd -d ./ -sa 0x5645f0d26000 -off 0x8158f`

`~/SSRG/PopSnapshot/criu/crit/crit ash -d ./ -dl /home/abhijit/criu-dump/nginx-dump/multi_sig_2.so -ha 0x7f0000001119 -vsa 0x7f0000000000`

## Installing Lighttpd and nginx
To install lighttpd and NGINX with webdav support, follow the below steps: 

1. Copy the lighttpd or nginx folder from /PopSnapshot/tests

2. Run the build script first, this will untar the lighttpd or NGINX source and build it with webdav support

3. Next, run the run_lighttpd.sh or run_nginx.sh script. This will create dav folders at `/home/$USER/lighttpd` or `/home/$USER/nginx`

4. The run script also starts up lighttpd/nginx from the configuration files provided in the folder

## Testing adding signal handler to Lighttpd and Multiple features removal (GCC 9.3.0 and Ubuntu 20.04)

1. Copy the modify_image_lighttpd script from /PopSnapshot/tools/scripts into a new folder

2. Copy the trap_locations file from /PopSnapshot/tests/traps_lighttpd (This file has the trap locations for PUT and DELETE pre-filled)

3. Copy the multi_sig_2.c file from /PopSnapshot/tests/handler_example (This is the shared library that will be loaded into lighttpd address space)

4. Run the modify_image script with the following input:
  - Name of the binary which to be modified (In this case, lighttpd)
  - The dump directory location
  - Path to the parent criu folder
  - **Full Path** to the folder that contains the multi_sig_2.c sig handler file

5. Example command: 

`./modify_image.sh lighttpd . ~/SSRG/PopSnapshot/criu /home/abhijit/criu-dump/test_lighttpd_handler2/`

## Testing adding signal handler to NGINX and Multiple features removal (GCC 9.3.0 and Ubuntu 20.04)

1. Copy the modify_image_nginx script from /PopSnapshot/tools/scripts into a new folder

2. Copy the trap_locations file from /PopSnapshot/tests/traps_nginx (This file has the trap locations for PUT and DELETE pre-filled)

3. Copy the multi_sig_2.c file from /PopSnapshot/tests/handler_example (This is the shared library that will be loaded into nginx address space)

4. Run the modify_image script with the following input:
  - Name of the binary which to be modified (In this case, nginx)
  - The dump directory location
  - Path to the parent criu folder
  - **Full Path** to the folder that contains the multi_sig_2.c sig handler file

5. Example command: 

`./modify_image.sh nginx . ~/SSRG/PopSnapshot/criu /home/abhijit/criu-dump/nginx-dump/`

## CURL commands to test PUT, DELETE and GET

1. GET: Gets the file hello-demo from the server if it's PUT there first

`curl -v 'http://0.0.0.0:8888/webdav/hello-demo'` 

2. PUT: PUTs the given file to the server. In this case, hello-demo

`curl -v -H "Expect:" -T "hello-demo" 'http://0.0.0.0:8888/webdav/'`

3. DELETE: DELETEs a file from the server. In this case, hello-demo, if it is PUT there first

`curl -v -X "DELETE" 'http://0.0.0.0:8888/webdav/hello-demo'`
