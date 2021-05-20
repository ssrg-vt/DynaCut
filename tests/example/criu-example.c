#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>

int i = 0;

void sigint_trap_handler(int sig)
{
     printf("SIGINT: The signal is: %d\n", sig);
     exit(1);
}

int main()
{
    printf("PID:%d \n", getpid());
    printf("Location: %p \n", &i);
    signal(SIGINT, sigint_trap_handler);
    while(i < 30){
        sleep(5);
        i = i + 1;
        printf("%d \n", i);
    }
    asm("int3");
    return 0;
}


