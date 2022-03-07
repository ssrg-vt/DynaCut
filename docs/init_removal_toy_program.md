# Remove initialization code for a test program
## Build the toy program
Build and run the toy application with:
```
❯ make -C tests/example init-example
❯ ./tests/example/init-example
In init1 function (used only once).
In init2 function (initialization).
In real_func function (real functional code).
In init2 function (initialization).
The initialization has been finished! You can dump now.
[ 9]
... ...
[ 0]
In real_func function (real functional code).
```

The toy application has two init functions (`init1` and `init2`) and a real function. It uses a simple loop to simulate the event loop of server applications.
In this example, we want to **automatically identify** the init functions and remove them from the process's memory space.


## Remove initialization code using code coverage information
Export the the DynamoRIO Home path:
```
source ./export_drio.sh
```

Run the `init-example` using `dynamorio/drcov`. We want to ask `drcov` to dump the code coverage information to a file after the initialization phase.
```
./dynamorio/exports/bin64/drrun -root ./dynamorio/build -c ./dynamorio/build/clients/lib64/debug/libdrcov.so -dump_text -nudge_dump --  ./tests/example/init-example
```
Open another terminal and use nudge to dump the execution log for the initialization phase:
```
./dynamorio/build/bin64/nudgeunix  -pid $(pidof init-example) -client 0 2
```

You will get two log files. This first one is the code coverage of the 1st execution phase (init phase); the 2nd file is the code coverage of the 2nd execution phase (serving phase):
```
❯ ls drcov.init-example.885048.000*
drcov.init-example.885048.0000.proc.log  drcov.init-example.885048.0001.proc.log
```
Next, run the `./tracediff.py` tool to find the basic blocks that only belong to the initialization execution phase. Note module[  5] is the code section of the `init-example`:
```
❯ ./tools/scripts/tracediff.py -u drcov.init-example.885048.0000.proc.log -b drcov.init-example.885048.0001.proc.log | grep "\[  5\]:"
[1718] module[  5]: 0x00000000000000a0,  46
[1738] module[  5]: 0x0000000000000260,  49
[1739] module[  5]: 0x0000000000000000,  20
[1740] module[  5]: 0x0000000000000016,   5
... ...
```
In this case, there are 29 basic block that only belongs to the initialization phase.

## Abhijit's document
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