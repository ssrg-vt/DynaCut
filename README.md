# Dynamic and Adaptive Code Customization with Process Rewriting

This project aims to dynamically customize code of a running process. The major component is an extended CRIU/CRIT tool that can rewrite the saved process images.
This repo contains a modified version of CRIU that can edit a process, disable code path, and insert library pages to a process at arbitrary VMA location.

Table of Contents
=================

* [Dynamic and Adaptive Code Customization with Process Rewriting](#dynamic-and-adaptive-code-customization-with-process-rewriting)
* [Table of Contents](#table-of-contents)
   * [Build DynaCut](#build-dynacut)
   * [<a href="docs/customize_toy_program.md">Build and customize a toy program</a>](#build-and-customize-a-toy-program)
   * [Dynamically remove unwanted features for application process](#dynamically-remove-unwanted-features-for-application-process)
   * [Dynamically remove the Initialization code for a toy example](#dynamically-remove-the-initialization-code-for-a-toy-example)
   * [Dynamically remove the Initialization code for macrobenchmarks](#dynamically-remove-the-initialization-code-for-macrobenchmarks)
   * [Example: adding a signal handler to a process](#example-adding-a-signal-handler-to-a-process)
   * [Installing Lighttpd and nginx](#installing-lighttpd-and-nginx)
   * [Testing adding signal handler to Lighttpd and Multiple features removal (GCC 9.3.0 and Ubuntu 20.04)](#testing-adding-signal-handler-to-lighttpd-and-multiple-features-removal-gcc-930-and-ubuntu-2004)
   * [Testing adding signal handler to NGINX and Multiple features removal (GCC 9.3.0 and Ubuntu 20.04)](#testing-adding-signal-handler-to-nginx-and-multiple-features-removal-gcc-930-and-ubuntu-2004)
   * [CURL commands to test PUT, DELETE and GET](#curl-commands-to-test-put-delete-and-get)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc). (To generate the ToC of README.md, just run `./gh-md-toc README.md`)

## [Build DynaCut](docs/build_dynacut.md)

## [Build and customize a toy program](docs/customize_toy_program.md)

## Dynamically remove unwanted features for application process
### Redis-server
Let's use a Redis server as an example:
[Removing unwanted features in Redis-server](docs/redis.md)

## Dynamically remove the Initialization code for a toy example
In this example, we simulate initialization functions removal.

First compile the init-example.c file located in tests/example.

This file has an SIGINT handler that we consider as *undesired*.

Follow the steps below to test this example: 

1. Generate a `drcov` trace of this executable, at the end of the execution, the application prints "SIGINT me now", send a SIGINT then, this is to record the execution of the SIGINT handler in the trace. 

```
❯ ~/SSRG/DynamoRIO-Linux-8.0.0-1/bin64/drrun -t drcov -dump_text -- ./init-example


CRiU dump me now
SIGINT me now

^C2 received
```

We now have the trace for the application. 

To remove initialization basic blocks, follow the below steps: 

Copy the `config_init.sh` script located in tools/scripts/initialization_functions_removal and the `remove_init.sh` script located in tools/scripts/initialization_functions_removal to a test-folder. 

Copy the signal handler code to this location. The Signal Handler code is located in: tests/sighandler/multi_sig_init.c

Run the executable again.

First run the `config_init.sh` script when the application prints "CRiU dump me now". 

The input to the script is: 
1. The name of the application. 
2. The path to the drcov log(s) of the application 
3. Path to modified CRiU 
4. The Initialization point to be considered -- use any address in the application from the execution trace that is executed *after* the SIGINT handler. 

For example, if the address of the SIGINT handler is `0x11e9`, it will be recorded in the execution trace. Choose an address *in the application* that is executed after this address, in this case we chose `0x128c`.

**Do not SIGINT the application now, wait for it to finish execution**

Example:
```
./config_init.sh "init-example" ./drcov.init-example.81382.0000.proc.log ~/SSRG/PopSnapshot/criu 0x128c
```
The application will be restored with the SIGINT handler disabled. 

Now, run the `remove_init.sh` script. 

The input to this script is: 

1. Name of the application.
2. Path to modified CRiU. 
3. Path to locations.txt, which is the whitelist of the locations generated in the first step. This file is usually generated in the same folder as the path to the binary. 

Example:
```
./remove_init.sh "init-example" ~/SSRG/PopSnapshot/criu ./locations.txt
```
We have removed the SIGINT handler and restored the application. 

When a SIGINT is sent to this modified application, it should crash with a SIGTRAP signal. 

## Dynamically remove the Initialization code for macrobenchmarks

To remove initialization basic blocks, follow the below steps: 

We have two scripts to remove initialization code. The first script is the `config_init.sh` script located in tools/scripts/initialization_functions_removal and the `remove_init.sh` script located in tools/scripts/initialization_functions_removal 

For NGINX, use the `config_init_nginx.sh` script. 

Copy these scripts to a test-folder. Also copy the signal handler code to this location. The Signal Handler code is located in: tests/sighandler/multi_sig_init.c

First, run the application using step [Installing Lighttpd and nginx](#installing-lighttpd-and-nginx). Next, run the config_init.sh script inside the test-folder. 


The input to the script is: 
1. The name of the application. 
2. The path to the drcov log(s) of the application 
3. Path to modified CRiU 
4. The Initialization point to be considered; For lighttpd: location of `server_main_loop` and for NGINX: location of `ngx_worker_process_cycle`.

Example for lighttpd: 
```
❯ ./config_init.sh "lighttpd" ~/drrun-dump/drcov.lighttpd.84903.0000.thd.log ~/SSRG/PopSnapshot/criu 0x11831
```

Example for NGINX: 
```
❯ ./config_init_nginx.sh "nginx" ~/drio-nginx/drcov.nginx.131318.0000.thd.log ~/drio-nginx/drcov.nginx.131319.0000.thd.log ~/SSRG/PopSnapshot/criu 0x5f356
```

The application is restored with the modifications. This step is to create the whitelist of the basic blocks that should not be removed -- test all the desired features in this step.  

Once the required functionality is executed in this step, SIGINT the application or let it exit(in the case of SPEC applications). A `locations.txt` file is created in the folder which contains the application binary. 

Next, run the `remove_init.sh` script located in tools/scripts/initialization_functions_removal/remove_init.sh. This script also should be run from the dump folder itself. 

The input to this script is: 

1. Name of the application.
2. Path to modified CRiU. 
3. Path to locations.txt, which is the whitelist of the locations generated in the first step. This file is usually generated in the same folder as the path to the binary. 

Example:

```
❯ ./remove_init.sh "lighttpd" ~/SSRG/PopSnapshot/criu ~/SSRG/PopSnapshot/tests/nginx/locations.txt
```

Example:

```
❯ ./remove_init.sh "nginx" ~/SSRG/PopSnapshot/criu ~/SSRG/PopSnapshot/tests/lighttpd/locations.txt
```

We have removed all the basic blocks which were considered as init basic blocks and which were not present in the whitelist. 

Finally, to see the output, set the `DEBUG flag = True` in remove_init.py located in  criu/lib/py/remove_init.py

The application is then restored with the init functions removed. 

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
