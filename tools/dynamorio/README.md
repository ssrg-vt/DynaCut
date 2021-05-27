# Dynamic and Adaptive Code Customization with Process Rewriting

## Instructions to build DynamoRIO tool

```
cmake -DDynamoRIO_DIR=/home/abhijit/SSRG/DynamoRIO-Linux-8.0.0-1/cmake ./
```

The build files are written to the same folder as the tool. 

Run ```make``` to build the tool. 

## Instructions to use the tool

``` 
bin64/drrun -c /bin/libbbcount_DynaCut.so -- <Application to be traced>

```

Example command to run an executable named "example":

```
~/SSRG/DynamoRIO-Linux-8.0.0-1/bin64/drrun -thread_private -c ~/SSRG/DynaCut/tools/dynamorio/bin/libbbcount_DynaCut.so -- ./example
```

Log files are written to the bin folder where the libbbcount.so is created