#!/bin/bash

 objdump -TC /lib/x86_64-linux-gnu/libc.so.6 | grep " printf$"
 objdump -TC /lib/x86_64-linux-gnu/libc.so.6 | grep " exit$"
