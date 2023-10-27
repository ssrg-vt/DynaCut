# Customize Lighty in Docker

In this example, we test customizing the lighttpd server inside the docker container. 

Follow instructions here to build and run a DynaCut docker container: https://github.com/ssrg-vt/DynaCut/blob/main/docs/docker-build.md#docker_build. 

## Testing adding signal handler to Lighttpd and Multiple features removal

Once inside the docker container, follow the steps below: 

```
❯ dynacut-usr@c223a1eae4f1:~/DynaCut$ mkdir test-lighty
❯ dynacut-usr@c223a1eae4f1:~/DynaCut$ cp tools/scripts/modify_image_lighttpd.sh tests/traps_lighttpd/trap_locations tests/sighandler/multi_sig_2.c ./test-lighty/
❯ dynacut-usr@c223a1eae4f1:~/DynaCut$ cd tests/lighttpd/
❯ dynacut-usr@c223a1eae4f1:~/DynaCut/tests/lighttpd$ ./run_lighttpd.sh

```
> **_NOTE:_**  For the sake of this example, the locations where the traps needs to be inserted to block `PUT` and `DELETE` have already been pre-filled in the `trap_locations` file. 

Lighty should be running now. In a different terminal, docker exec into the running container. Also set the umask value to 0002. 

```
❯ sudo docker exec -it --privileged c223a1eae4f1 bash
❯ dynacut-usr@c223a1eae4f1:~/DynaCut$ umask 0002
```

Test that the `PUT` and `DELETE` commands work using the CURL commands as described in https://github.com/ssrg-vt/DynaCut/blob/main/docs/curl_commands.md#curl_commands

Now, we will customize the running lighty server to disable the PUT and DELETE commands. 

In the second terminal, run the following commands: 

```
❯ dynacut-usr@c223a1eae4f1:~/DynaCut$ cd test-lighty
❯ dynacut-usr@c223a1eae4f1:~/DynaCut/test-lighty$ ./modify_image_lighttpd.sh lighttpd . ~/DynaCut/criu/ ~/DynaCut/test-lighty/
```

A customized version of lighty with `PUT` and `DELETE` blocked should run in the second terminal. Check that the `PUT` and `DELETE` commands are blocked by running the CURL commands again. They should return an output similar to: 

```
dynacut-usr@c223a1eae4f1:~/DynaCut$ curl -v -X "DELETE" 'http://0.0.0.0:8888/webdav/hello-demo'
*   Trying 0.0.0.0:8888...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 8888 (#0)
> DELETE /webdav/hello-demo HTTP/1.1
> Host: 0.0.0.0:8888
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 403 Forbidden
< Content-Type: text/html
< Content-Length: 341
< Date: Fri, 27 Oct 2023 12:20:25 GMT
< Server: lighttpd/1.4.59
< 
<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
         "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
 <head>
  <title>403 Forbidden</title>
 </head>
 <body>
  <h1>403 Forbidden</h1>
 </body>
</html>
* Connection #0 to host 0.0.0.0 left intact
```

## Unmapping a VMA 
To unmap a VMA region for lighty, follow the steps below. 

```
❯ dynacut-usr@c2fa13ae34f5:~/DynaCut$ mkdir test
❯ dynacut-usr@c2fa13ae34f5:~/DynaCut$ cp /tools/scripts/modify_image_lighttpd_uv.sh ./test
❯ cd test
❯ dynacut-usr@c2fa13ae34f5:~/DynaCut/test$ ./modify_image_lighttpd_uv.sh lighttpd . ~/DynaCut/criu <start address of VMA region>
```
> **_NOTE:_**  Lighttpd uses `libpthread-2.31.so`. An example of a VMA region that can be unmapped might look like: `7fe48eb58000-7fe48eb69000 r-xp 00006000 00:78 8929620                    /usr/lib/x86_64-linux-gnu/libpthread-2.31.so`

After the above steps, the process should be restored with one page unmapped. the script would need to be modified to unmap more than a page.  
