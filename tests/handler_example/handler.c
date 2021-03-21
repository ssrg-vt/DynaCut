#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>

void trap_handler(int sig)
{
     printf("The signal is: %d\n", sig);
     exit(1);
}


