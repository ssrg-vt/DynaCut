# Build DynaCut

## Install pre-requisites and build CRIU
On Ubuntu 20.04, install the following packages required by [CRIU](https://criu.org/Installation). If you are using a different OS, please follow this link: [packages needed by CRIU](https://criu.org/Installation).
```
❯ sudo apt install libprotobuf-dev libprotobuf-c-dev protobuf-c-compiler protobuf-compiler python-protobuf libnl-3-dev libcap-dev libaio-dev libcap-dev python-ipaddress
```

You also need to install the following python modules required by DynaCut:
```
❯ pip2 install capstone pyelftools
```

Once you installed all the required packages, build the CRIU with:
```
❯ make -C criu
...
  LINK     lib/c/libcriu.so
  LINK     lib/c/libcriu.a
  GEN      lib/py/images/magic.py
```

## Download DynamoRIO
[Download DynamoRIO](https://dynamorio.org/page_releases.html) and unzip the [tar ball](https://github.com/DynamoRIO/dynamorio/releases/download/release_8.0.0-1/DynamoRIO-Linux-8.0.0-1.tar.gz) to the **`DynaCut` root** directory.

```
❯ wget https://github.com/DynamoRIO/dynamorio/releases/download/release_8.0.0-1/DynamoRIO-Linux-8.0.0-1.tar.gz
❯ tar xvf DynamoRIO-Linux-8.0.0-1.tar.gz
❯ ls
tests   tools   criu   DynamoRIO-Linux-8.0.0-1   ...
```

## DynaCut inside a Docker container

Follow instructions here to build and run DynaCut inside a Ubuntu 20 docker container [DynaCut docker](https://github.com/ssrg-vt/DynaCut/blob/main/docs/docker-build.md)
