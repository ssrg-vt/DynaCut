#!/bin/bash

# Prepare lighttpd www root dir
mkdir -p ./www-root/web
mkdir -p ./www-root/html

echo "<http>
<head></head>
<body>Hello world. Running on lighttpd.</body>
</http>" > www-root/html/index.html

echo "<http>
<head></head>
<body>Hello world. Lighttpd WebDAV.</body>
</http>" > www-root/web/index.html

# Copy the configuration file and update the config
cp lighttpd.conf.template lighttpd.conf

sed -i 's/usrname/'$(id -un)'/g' lighttpd.conf
sed -i 's/grpname/'$(id -gn)'/g' lighttpd.conf
sed -i 's?\/current-dir?'`pwd`'?' lighttpd.conf

head -n 7 lighttpd.conf
echo "..."
echo

# Run the Lighttpd server
./lighttpd-1.4.59/src/lighttpd -f lighttpd.conf -m ./lighttpd-1.4.59/src/.libs -D
