#!/bin/bash

if [ $# != 1 ]; then
    echo "Use ./restore.sh <dir>"
fi

sudo ./criu_modified/criu/criu restore -j -D $1