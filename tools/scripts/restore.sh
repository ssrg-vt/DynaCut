#!/bin/bash

if [ $# != 1 ]; then
    echo "Use ./restore.sh <dir>"
    exit 1
fi

sudo ./criu/criu/criu restore -j -D $1
