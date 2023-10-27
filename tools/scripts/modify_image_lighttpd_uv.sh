#!/bin/bash

if [ $# != 4 ]; then
     echo "Use ./modify_image.sh <program name> <dump dir> <path to criu modified> <start address of VMA page that needs to be removed>"
fi

# Prepare the dir for process dump
mkdir -p vanilla-dump
rm vanilla-dump/* -rf

pid=$(pidof -s $1)

# Run criu dump and change the dump image ownership
sudo $3/criu/criu dump -D vanilla-dump -j -t $(pidof -s $1)
sudo chown $USER:$(id -gn) vanilla-dump -R

# Copy vanilla images from dump
cp ./vanilla-dump/* .

# Unmap a VMA page
$3/crit/crit uv -d ./ -va $4 -np 1 -p $pid

# Restore the modified binary
sudo $3/criu/criu restore -j -D $2
