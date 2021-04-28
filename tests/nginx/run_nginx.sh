#!/bin/bash

mkdir -p /home/$USER/nginx/html
mkdir -p /home/$USER/nginx/dav
mkdir -p /home/$USER/nginx/dav/temp

sed -i 's/usrname/'$USER'/g' nginx.conf
sed -i 's/grpname/'$(id -gn)'/g' nginx.conf

./nginx-1.18.0/objs/nginx -g 'daemon off;' -c $PWD/nginx.conf
