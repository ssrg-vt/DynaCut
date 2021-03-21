# Testing Modifications to CRIU

This modified CRIU example has features to edit a process, add library pages to a process at any arbitrary VMA location (MOre examples can be found by running `crit -h` )

## Pre-requisites to test modified CRIU

Apart from the packages needed by Vanilla CRIU, the following packages are required by modified CRIU:
`pip install capstone`
`pip install pyelftools`

## Testing adding a signal handler to a process

To add a signal handler as a library to a process, the following steps need to be followed: 

1. Find any library functions needed by the shared library using the example script provided in /PopSnapshot/tools/scripts/find_print_exit.sh. This script can also be modified to find more library functions used by the shared library

2. The permission of the library needs to be 775 (Required by CRIU when restoring)

3. An example handler library and Makefile is provided in /PopSnapshot/tests/handler_example

4. Currently, all The PLT offsets used by the library and their corresponding offsets in libc need to be entered manually. 

The file plt-file.json in /PopSnapshot/tests has some entries filled for print and exit library functions for libc-2.31.so. 

Add any extra entries according to the format provided and place the plt-file.json in the CRIU dump folder which is to be modified. The name has to be the same. 

5. An example command for adding a signal handler is: 

`sudo ~/SSRG/PopSnapshot/criu_modified/crit/crit ash -d . -dl /home/abhijit/criu-dump/elf_loader -name libhandler.so -ha 0x7f0000001139 -ra 0x7f5ace2c3210 -vsa 0x7f0000000000`

In the example:
    1. `-d .` points to the criu dump folder
    2. `-dl /home/abhijit/criu-dump/elf_loader` points to the folder which contains the library to be loaded
    3. `-name` is the name of the library that is to be loaded into the address space
    4. `-ha` is the signal handler address (This is: vma_start_address + offset of function in library)
    5. `-ra` is the signal restorer address
    6. `-vsa` is the start address of the VMA region at which the library is to be mapped

6. An example process to which this signal handler has been added is located in /PopSnapshot/tests/criu-example

7. If using the example executable and the example handler library, the restorer address can be the same as the SIGINT restorer 

8. Currently this method only supports handling the SIGTRAP signal
