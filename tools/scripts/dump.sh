#!/bin/bash

if [ $# != 1 ]; then
    echo "Use ./dump.sh <program name>"
    exit 1
fi

# Get the pid and dir name from the program binary name.
PID=$(pidof -s $1)
echo $PID

DIR=$1.img
echo $DIR

# Prepare the dir for process dump
mkdir -p $DIR
rm $DIR/* -rf

# Run criu dump and change the dump image ownership
sudo ./criu/criu/criu dump -D $DIR -j -t $PID
sudo chown $(id -un):$(id -gn) $DIR -R
