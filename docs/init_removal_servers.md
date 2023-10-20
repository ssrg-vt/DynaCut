# Remove initialization code for server applications
To remove initialization basic blocks we will use the NGINX server as an example. Follow the steps below to use Dynacut to remove initialization code:

We have two scripts to remove initialization code. The first script is the config_init.sh script located in tools/scripts/initialization_functions_removal and the remove_init.sh script located in tools/scripts/initialization_functions_removal

For NGINX, use the config_init_nginx.sh script.

Copy these scripts to a test-folder. Also copy the signal handler code to this location. The Signal Handler code is located in: tests/sighandler/multi_sig_init.c

First, run the application using step Installing Lighttpd and nginx. Next, run the config_init.sh script inside the test-folder.

The input to the script is:

    The name of the application.
    The path to the drcov log(s) of the application
    Path to modified CRiU
    The Initialization point to be considered; For lighttpd: location of server_main_loop and for NGINX: location of ngx_worker_process_cycle.

Example for lighttpd:

❯ ./config_init.sh "lighttpd" ~/drrun-dump/drcov.lighttpd.84903.0000.thd.log ~/SSRG/PopSnapshot/criu 0x11831

Example for NGINX:

❯ ./config_init_nginx.sh "nginx" ~/drio-nginx/drcov.nginx.131318.0000.thd.log ~/drio-nginx/drcov.nginx.131319.0000.thd.log ~/SSRG/PopSnapshot/criu 0x5f356

The application is restored with the modifications. This step is to create the whitelist of the basic blocks that should not be removed -- test all the desired features in this step.

Once the required functionality is executed in this step, SIGINT the application or let it exit(in the case of SPEC applications). A locations.txt file is created in the folder which contains the application binary.

Next, run the remove_init.sh script located in tools/scripts/initialization_functions_removal/remove_init.sh. This script also should be run from the dump folder itself.

The input to this script is:

    Name of the application.
    Path to modified CRiU.
    Path to locations.txt, which is the whitelist of the locations generated in the first step. This file is usually generated in the same folder as the path to the binary.

Example:

❯ ./remove_init.sh "lighttpd" ~/SSRG/PopSnapshot/criu ~/SSRG/PopSnapshot/tests/nginx/locations.txt

Example:

❯ ./remove_init.sh "nginx" ~/SSRG/PopSnapshot/criu ~/SSRG/PopSnapshot/tests/lighttpd/locations.txt

We have removed all the basic blocks which were considered as init basic blocks and which were not present in the whitelist.

Finally, to see the output, set the DEBUG flag = True in remove_init.py located in criu/lib/py/remove_init.py

The application is then restored with the init functions removed.
