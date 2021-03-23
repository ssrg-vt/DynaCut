#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>

int main()
{
    int i = 0;
    printf("PID:%d \n", getpid());
    printf("Location: %p \n", &i);

    while(i < 5) {
        sleep(5);
        printf("%d \n", ++i);
    }
    asm("int3");
    return 0;
}


