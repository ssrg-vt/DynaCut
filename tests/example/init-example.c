#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <signal.h>

/* A SIGINT handler to demonstrate removal of 
 * initialization code */

void handler(sig)
int sig;
{
    printf("%d received\n",sig);
}


int main()
{
    /* register SIGINT handler */
    struct sigaction sa;
    sa.sa_handler = handler;
    sigaction(SIGINT, &sa, NULL);

    printf("CRiU dump me now\n");
    
    /* sleep to allow user to checkpoint */
    sleep(30);
    
    printf("SIGINT me now\n");
    printf("\n");
    
    /* sleep to allow user to send a SIGINT */
    sleep(40);
    
    return 0;
}
