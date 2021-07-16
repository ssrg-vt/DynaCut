#!/bin/bash

if [ $# != 3 ]; then
     echo "Use ./remove_init.sh <path to criu modified> <vma base address of binary> <path to locations.txt>"
fi

cp ./vanilla-dump/* .
$1/crit/crit rid -d ./ -sa $2 -tf $3
