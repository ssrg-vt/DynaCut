#!/bin/bash

if [ $# != 3 ]; then
     echo "Use ./remove_init.sh <name> <path to criu modified> <path to locations.txt>"
fi

cp ./vanilla-dump/* ./test-dump
$2/crit/crit rid -d ./test-dump -name $1 -tf $3

sudo ~/SSRG/PopSnapshot/criu/criu/criu restore -j -D ./test-dump
