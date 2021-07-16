#!/bin/bash

if [ $# != 6 ]; then
    echo "Use ./config_init.sh <program name> <path to drcov log> <path to second drcov log> <path to criu modified> <init BB address> <vma base address of binary>"
fi

cp ./vanilla-dump/* .
$4/crit/crit config_init -d ./ -name $1 -input $2 $3 -sa $6 -ip $5
gcc -g -shared -fPIC multi_sig_init.c -o multi_sig_init.so
$4/crit/crit ash -d ./ -ha 0x10001199 -vsa 0x10000000 -dl $PWD/multi_sig_init.so
