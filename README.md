# Dynamic and Adaptive Code Customization with Process Rewriting

This project aims to dynamically customize code of a running process. The major component is an extended CRIU/CRIT tool that can rewrite the saved process images.
This repo contains a modified version of CRIU that can edit a process, disable code path, and insert library pages to a process at arbitrary VMA location.

Table of Contents
=================

* [Dynamic and Adaptive Code Customization with Process Rewriting](#dynamic-and-adaptive-code-customization-with-process-rewriting)
   * [Install pre-requisites, build CRIU and test examples](#install-pre-requisites-build-criu-and-test-examples)
      * [Disable the int3 code blocks with injected signal handler](#disable-the-int3-code-blocks-with-injected-signal-handler)
   * [Dynamically remove unwanted features for application process](#dynamically-remove-unwanted-features-for-application-process)
      * [Find the basic blocks of the unwanted feature](#find-the-basic-blocks-of-the-unwanted-feature)
      * [Disable the unwanted feature by rewriting the CRIU process image](#disable-the-unwanted-feature-by-rewriting-the-criu-process-image)
      * [Test the correctness of dynamic feature removal](#test-the-correctness-of-dynamic-feature-removal)
   * [Dynamically remove the initialization code](#dynamically-remove-the-initialization-code)
   * [Example: adding a signal handler to a process](#example-adding-a-signal-handler-to-a-process)
   * [Installing Lighttpd and nginx](#installing-lighttpd-and-nginx)
   * [Testing adding signal handler to Lighttpd and Multiple features removal (GCC 9.3.0 and Ubuntu 20.04)](#testing-adding-signal-handler-to-lighttpd-and-multiple-features-removal-gcc-930-and-ubuntu-2004)
   * [Testing adding signal handler to NGINX and Multiple features removal (GCC 9.3.0 and Ubuntu 20.04)](#testing-adding-signal-handler-to-nginx-and-multiple-features-removal-gcc-930-and-ubuntu-2004)
   * [CURL commands to test PUT, DELETE and GET](#curl-commands-to-test-put-delete-and-get)




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
❯ ./criu/crit/crit edit insert sighandler vanilla-dump 0x1000000 -path $(pwd)/tests/sighandler/multi_sig.so
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

## Dynamically remove unwanted features for application process
Let's use a Redis server as an example. The first step is to identify the code to remove. Here we leverage the [code coverage tool in DynamoRIO](https://dynamorio.org/page_drcov.html) to dump out which basic blocks have been executed.

**Preparation**: [Download DynamoRIO](https://dynamorio.org/page_releases.html) and unzip the [tar ball](https://github.com/DynamoRIO/dynamorio/releases/download/release_8.0.0-1/DynamoRIO-Linux-8.0.0-1.tar.gz) to the `DynaCut` root directory.
Unzip the redis tar ball (`tests/redis-6.2.3.tar.gz`) to the `tests` directory, and build the `redis server/benchmark`:
```
❯ tar xvf DynamoRIO-Linux-8.0.0-1.tar.gz
❯ ls
tests   tools   criu   DynamoRIO-Linux-8.0.0-1   ...
❯ cd tests; tar xvf redis-6.2.3.tar.gz; cd ..
❯ make -C tests/redis-6.2.3
...
    LINK redis-server
    INSTALL redis-sentinel
    LINK redis-cli
    LINK redis-benchmark
...
```
### Find the basic blocks of the unwanted feature
In this example, we consider redis `set` is an unwanted feature, and consider `get`, `ping` are wanted feature. To find the BB of the unwanted feature, follow steps 1 - 4:

1. Start the `redis-server` with the DynamoRIO code coverage tool running:
```
❯ ./DynamoRIO-Linux-8.0.0-1/bin64/drrun -t drcov -dump_text -- ./tests/redis-6.2.3/src/redis-server
```

2. Generate the code coverage trace of **wanted features**:

Open a new terminal, generate requests for wanted features and terminate the `redis-server` process (type `ctrl-c` on the `redis-server` terminal)
```
❯ ./tests/redis-6.2.3/src/redis-benchmark -q -t get -n 100
❯ ./tests/redis-6.2.3/src/redis-benchmark -q -t ping -n 100
```
Now you can get a DynamoRIO log similar to `drcov.redis-server.581030.0000.proc.log`. Rename it to `redis_wanted_feature.log` (by typing `mv drcov.redis-server.581030.0000.proc.log redis_wanted_feature.log`).

Note: If you have multiple code coverage logs for wanted features, you can merge them into one log with `sort -u`:
```
❯ sort -u drcov.redis-server.ping.log drcov.redis-server.get.log > redis_wanted_feature.log
```

3. Generate the code coverage trace of **unwanted features**:

Repeat step 1, and for step 2, we want to generate the log of unwanted features (e.g., we assume the Redis `set` is an unwanted feature)
```
❯ ./tests/redis-6.2.3/src/redis-benchmark -q -t get -n 100
```
Terminate the `redis-server` process. Rename the DynamoRIO log to `redis_unwanted_feature.log`

4. Run a script to filter out the unwanted basic blocks.
```
❯ ./tools/scripts/logdiff.py -u redis_unwanted_feature.log -b redis_wanted_feature.log
The unwanted feature log file: redis_unwanted_feature.log
The wanted log file: redis_wanted_feature.log

[  0] BB Table: 18145 bbs
[  1] module[  5]: 0x0000000000163870,  37
[  2] module[  5]: 0x000000000016943d,  23
[  3] module[  5]: 0x0000000000169454,  10
[  4] module[  5]: 0x000000000016945e,   5
[  5] module[  5]: 0x0000000000169463,  33
[  6] module[  5]: 0x000000000016949a,  21
[  7] module[  5]: 0x0000000000169360,  59
[  8] module[  5]: 0x000000000004ec71,  14
[  9] module[  5]: 0x000000000004ee33,  17
... ...
```
If we look at source code of this basic block `0x4ec71`, it is in `src/server.c:processCommand(client *c)` function. It passes the command from the client. By comparing the code coverage log, we can deduce the basic block `0x4ec71` is the code that handles the `set` command in `processCommand(client *c)`.
### Disable the unwanted feature by rewriting the CRIU process image
We can do *simple feature disable* or *full feature removal*. To simply disable a feature, we inject `int3` at the beginning of an unwanted feature basic block. We can also insert a simple signal handler that calls `exit()` on executing that `int3` trap instruction.

The following instructions will describe how to dynamically remove unwanted features by blocking the unwanted basic blocks:

Start the `redis-server` (`./tests/redis-6.2.3/src/redis-server`). Checkpoint the running `redis-server` with the following command:
```
❯ ./tools/scripts/dump.sh redis-server
❯ mv vanilla-dump redis.img
```

Before inserting the signal handler, we can examine the memory layout:
```
❯ ./criu/crit/crit x redis.img mems
159906
	exe                                     /<path to redis>/redis-6.2.3/src/redis-server
	555555554000-555555594000           r-- /<path to redis>/redis-6.2.3/src/redis-server
	555555594000-5555556eb000           r-x /<path to redis>/redis-6.2.3/src/redis-server + 0x40000
... ...
```
We can insert the signal handler at any address not being used. For example, we insert the signal handler at `0x1000000`:
```
❯ ./criu/crit/crit edit insert sighandler redis.img 0x1000000 -path $(pwd)/tests/sighandler/libhandler.so
❯ ./criu/crit/crit edit insert int3 redis.img 0x555555554000 -offset 0x4ec71
```
We also inserted the `int3` at the beginning of the basic block `0x4ec71` obtained from step 4. Let's check the updated memory layout:
```
❯ ./criu/crit/crit x redis.img mems
159906
	exe                               /<path to redis>/redis-6.2.3/src/redis-server
	01000000-01001000             r-- /<path to DynaCut>/DynaCut/tests/sighandler/libhandler.so
	01001000-01002000             r-x /<path to DynaCut>/DynaCut/tests/sighandler/libhandler.so + 0x1000
	01002000-01003000             r-- /<path to DynaCut>/DynaCut/tests/sighandler/libhandler.so + 0x2000
	01003000-01005000             rw- /<path to DynaCut>/DynaCut/tests/sighandler/libhandler.so + 0x2000
	555555554000-555555594000     r-- /<path to redis>/redis-6.2.3/src/redis-server
	555555594000-5555556eb000     r-x /<path to redis>/redis-6.2.3/src/redis-server + 0x40000
... ...
```
### Test the correctness of dynamic feature removal
We use the `redis-benchmark` to test the `redis-server`'s response to different requests.
```
❯ ./tests/redis-6.2.3/src/redis-benchmark -q -t ping -n 1000
PING_INLINE: 100000.00 requests per second, p50=0.239 msec         
PING_MBULK: 100000.00 requests per second, p50=0.247 msec

❯ ./tests/redis-6.2.3/src/redis-benchmark -q -t get -n 1000
GET: 111111.12 requests per second, p50=0.223 msec         

❯ ./tests/redis-6.2.3/src/redis-benchmark -q -t set -n 1000
Error: Connection reset by peer_msec=-nan (overall: -nan)
```
As expected, the `redis-server` exits when receiving the `set` test case.
```
❯ ./tools/scripts/restore.sh redis.img
The PID is 159906. signal #5. rip: 0x5555555a2c71
The signal is: 5
```

## Dynamically remove the initialization code

To remove initialization basic blocks, follow the below steps: 

We have two scripts to remove initialization code. The first script is the `config_init.sh` script located in tools/scripts/initialization_functions_removal and the `remove_init.sh` script located in tools/scripts/initialization_functions_removal 

Copy these scripts to the CRiU dump folder of the application. Also copy the signal handler code to this location. The Signal Handler code is located in: tests/sighandler/multi_sig_init.c

For NGINX, use the `config_init_nginx.sh` script. 

First, run the config_init.sh script inside the CRiU dump folder. Note that the application has to be checkpointed before running this script. 


The input to the script is: 
1. The name of the application. 
2. The path to the drcov log of the application 
3. Path to modified CRiU 
4. The initialization point to be considered; For lighttpd: location of `server_main_loop` and for NGINX: before the process forks.
5. The VMA base address of the application. 

Example for lighttpd: 
```
❯ ./config_init.sh "lighttpd" ~/drrun-dump/drcov.lighttpd.84903.0000.thd.log ~/SSRG/PopSnapshot/criu 0x11831 0x557711fb2000
```

Example for NGINX: 
```
❯ ./config_init.sh "nginx" ~/drio-nginx/drcov.nginx.131318.0000.thd.log ~/drio-nginx/drcov.nginx.131319.0000.thd.log ~/SSRG/PopSnapshot/criu 0x5baeb 0x56528a783000
```

The next step is to restore the application after the configuration step. This step is to create the whitelist of the basic blocks that should not be removed. 

Once the required functionality is executed in this step, SIGINT the application or let it exit(in the case of SPEC applications). A `locations.txt` file is created in the folder which contains the application binary. 

Next, run the `remove_init.sh` script located in tools/scripts/initialization_functions_removal/remove_init.sh. This script also should be run from the dump folder itself. 

The input to this script is: 

1. Path to modified CRiU. 
2. VMA base address, same as the one used for the configure step. 
3. Path to locations.txt, which is the whitelist of the locations. This file is usually generated in the same folder as the path to the binary. 

Example:

```
❯ ./remove_init.sh ~/SSRG/PopSnapshot/criu 0x56528a783000 ~/SSRG/PopSnapshot/tests/nginx/locations.txt
```

Example:

```
❯ ./remove_init.sh ~/SSRG/PopSnapshot/criu 0x557711fb2000 ~/SSRG/PopSnapshot/tests/lighttpd/locations.txt
```

We have removed all the basic blocks which were considered as init basic blocks and which were not present in the whitelist. 

Finally, to see the output, set the `DEBUG flag = True` in remove_init.py located in  criu/lib/py/remove_init.py

The application can then be restored with the init functions removed. 

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
