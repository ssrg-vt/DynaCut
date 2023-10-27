# Docker build instructions 

## We have also created a dockerbuild environment to test DynaCut. 

Please follow the steps below to test on the docker env:

1. Build the container in the DynaCut git folder using: 

> **_NOTE:_** `chown takes some time to finish, it may seem like the build is hung. 
```
sudo docker build . -t dynacut-ubuntu
```

> **_NOTE:_**  the umask value needs to be set to 0002 inside the container. If using `docker exec` to attach a new terminal to the container, run `umask=0002`. 

2. Run the container using: 
```
sudo docker run -it --privileged dynacut-ubuntu bash
```

3. To attach a new terminal to the running container, use the following command: 

```
sudo docker exec -it --privileged <name of running container> bash
```
