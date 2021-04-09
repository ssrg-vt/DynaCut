#!/bin/bash

if [ $# != 4 ]; then
     echo "Use ./modify_image.sh <program name> <dump dir> <path to criu modified> <full path to signal handler library"
fi

# Prepare the dir for process dump
mkdir -p vanilla-dump
rm vanilla-dump/* -rf

# Run criu dump and change the dump image ownership
sudo $3/criu/criu dump -D vanilla-dump -j -t $(pidof $1)
sudo chown $USER:$(id -gn) vanilla-dump -R

cp ./vanilla-dump/* .

$3/crit/crit config -d ./ -name "webdav" -ja 0x5797

gcc -shared -fPIC multi_sig_2.c -o multi_sig_2.so

$3/crit/crit ash -d . -dl $4/multi_sig_2.so -ha 0x7f0000001119 -vsa 0x7f0000000000

sudo $3/criu/criu restore -j -D $2
