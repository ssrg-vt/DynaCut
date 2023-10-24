#!/bin/bash

if [ $# != 5 ]; then
    echo "Use ./config_init.sh <program name> <path to drcov log> <path to second drcov log> <path to criu modified> <init BB address>"
fi

# Prepare the dir for process dump
mkdir -p vanilla-dump
rm vanilla-dump/* -rf

# Create a test dump directory to store modified images
mkdir -p test-dump
rm test-dump/* -rf

# Run criu dump and change the dump image ownership
sudo $4/criu/criu dump -D vanilla-dump -j -t $(ps -o ppid= $(pidof -s $1))
sudo chown $USER:$(id -gn) vanilla-dump -R

cp ./vanilla-dump/* ./test-dump
cp multi_sig_init.c ./test-dump
$4/crit/crit config_init -d ./test-dump -name $1 -input $2 $3 -ip $5
gcc -g -shared -fPIC ./test-dump/multi_sig_init.c -o ./test-dump/multi_sig_init.so
$4/crit/crit ash -d ./test-dump -ha 0x10001199 -vsa 0x10000000 -dl $PWD/test-dump/multi_sig_init.so

sudo $4/criu/criu restore -j -D ./test-dump
