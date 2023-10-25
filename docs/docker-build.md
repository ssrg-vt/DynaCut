# Docker build instructions 

## We have also created a dockerbuild environment to test DynaCut. 

Please follow the steps below to test on the docker env:

1. Build the container in the DynaCut git folder using: 

```
sudo docker build . -t dynacut-ubuntu
```

2. Run the container using: 
```
sudo docker run -it --privileged dynacut-ubuntu bash
```

3. To attach a new terminal to the running container, use the following command: 

```
sudo docker exec -it --privileged <name of running container> bash
```
