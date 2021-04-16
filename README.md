# Testing Modifications to CRIU

This modified CRIU example has features to edit a process, add library pages to a process at any arbitrary VMA location (More examples can be found by running `crit -h` )

## Pre-requisites to test modified CRIU

Apart from the packages needed by Vanilla CRIU, the following packages are required by modified CRIU:
`pip install capstone`
`pip install pyelftools`

## Testing adding a signal handler to a process

To add a signal handler as a library to a process, the following steps need to be followed: 

1. Find any library functions needed by the shared library using the example script provided in /PopSnapshot/tools/scripts/find_print_exit.sh. This script can also be modified to find more library functions used by the shared library

2. The permission of the library needs to be 775 (Required by CRIU when restoring)

3. An example handler library and Makefile is provided in /PopSnapshot/tests/handler_example 

4. An example process to which this signal handler has been added is located in /PopSnapshot/tests/criu-example

5. If using the example executable and the example handler library, the restorer address can be the same as the SIGINT restorer 

6. Currently this method only supports handling the SIGTRAP signal

## Testing adding signal handler to Lighttpd and Multiple features removal

1. Copy the modify_image script from /PopSnapshot/tools/scripts into a new folder

2. Copy the trap_locations file from /PopSnapshot/tests (This file has the trap locations for PUT and DELETE pre-filled)

3. Copy the multi_sig_2.c file from /PopSnapshot/tests/handler_example (This is the shared library that will be loaded into lighttpd address space)

4. Run the modify_image script with the following input:
  - Name of the binary which to be modified (In this case, lighttpd)
  - The dump directory location
  - Path to the criu_modified folder
  - **Full Path** to the folder that contains the multi_sig_2.c sig handler file

5. Example command: 

`./modify_image.sh lighttpd . ~/SSRG/PopSnapshot/criu_modified /home/abhijit/criu-dump/test_lighttpd_handler2/`