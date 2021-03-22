#!/bin/bash

if [ $# != 1 ]; then
    echo "Use ./dump.sh <program name>"
fi

# Prepare the dir for process dump
mkdir -p vanilla-dump
rm vanilla-dump/* -rf

# Run criu dump and change the dump image ownership
sudo ./criu_modified/criu/criu dump -D vanilla-dump -j -t $(pidof $1)
sudo chown $USER:$(id -gn) vanilla-dump -R