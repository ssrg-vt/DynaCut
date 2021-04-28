#!/bin/bash

tar xvf nginx-1.18.0.tar.gz
pushd nginx-1.18.0
CFLAGS='-fPIC -g' LDFLAGS="-pie" CC=gcc ./configure --with-http_dav_module
make -j4
popd
