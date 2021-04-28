#!/bin/bash

mkdir -p /home/$USER/lighttpd/web
mkdir -p /home/$USER/lighttpd/html

sed -i 's/usrname/'$USER'/g' lighttpd.conf
sed -i 's/grpname/'$(id -gn)'/g' lighttpd.conf

head -n 7 lighttpd.conf
echo

./lighttpd-1.4.59/src/lighttpd -f lighttpd.conf -m ./lighttpd-1.4.59/src/.libs -D
