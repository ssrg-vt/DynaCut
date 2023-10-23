# Remove initialization code for server applications

## Generating logs for initialization blocks removal

DynaCut uses drcov logs of an application to identify initialization basic blocks. These logs need to be generated only once. To generate drcov logs for the NGINX server, follow the steps below: 
```
❯  cd ~/Dynacut/tests/nginx
❯  ./build_nginx.sh
❯  ~/DynamoRIO-Linux-8.0.0-1/bin64/drrun -t drcov -dump_text -- ./nginx-1.18.0/objs/nginx -g 'daemon off;' -c $PWD/nginx.conf -p /home/$USER/nginx
```
Execute basic CURL commands to generate complete logs. Refer https://github.com/ssrg-vt/DynaCut/blob/main/docs#curl_commands.md. 
    
## Removing init basic blocks

To remove initialization basic blocks we will use the NGINX server as an example. Follow the steps below to use Dynacut to remove initialization code:

 - Run the `run_nginx.sh` script. This will create dav folder at `/home/$USER/nginx.
 - The run script also starts up nginx from the configuration files provided in the folder.

We have two scripts to remove initialization code. 
 - The first script is the `config_init_nginx.sh` script located in `tools/scripts/initialization_functions_removal` and 
 - The `remove_init.sh` script located in `tools/scripts/initialization_functions_removal`.

Copy these scripts to a test-folder for ease of use between runs. Also copy the signal handler code (`tests/sighandler/multi_sig_init.c`) to this location. 

At this point NGINX should be running. Next, run the `config_init_nginx.sh` script inside the test-folder.

The input to the script is:

    - The name of the application.
    - The path to the drcov log(s) of the application
    - Path to modified CRiU
    - The Initialization point to be considered; for NGINX: location of `ngx_worker_process_cycle`.

Example for NGINX:

```
❯ ./config_init_nginx.sh "nginx" ~/drio-logs/drcov.nginx.131318.0000.thd.log ~/drio-logs/drcov.nginx.131319.0000.thd.log ~/DynaCut/criu 0x5f356
```

The application is restored with the modifications. This step is to create the whitelist of the basic blocks that should not be removed -- test all the desired features in this step.

Once the required functionality is executed in this step, SIGINT the application. A locations.txt file is created in the folder which contains the application binary.

Next, run the `remove_init.sh` script located in `tools/scripts/initialization_functions_removal/remove_init.sh`. This script also should be run from the dump folder itself.

The input to this script is:

    -Name of the application.
    -Path to modified CRiU.
    -Path to locations.txt, which is the whitelist of the locations generated in the first step. This file is usually generated in the same folder as the path to the binary.

To see the output, set the `DEBUG = True` in `criu/lib/py/remove_init.py` before executing the following command.

Example:
```
❯ ./remove_init.sh "nginx" ~/DynaCut/criu ~/Dynacut/tests/nginx/locations.txt
```

We have removed all the basic blocks which were considered as init basic blocks and which were not present in the whitelist.

The application is then restored with the init functions removed.
