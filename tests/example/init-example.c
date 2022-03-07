#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <signal.h>

/* Initialization functions and real functions. */
void init1(void)
{
    printf("In %s function (used only once).\n", __func__);
}

void init2(void)
{
    printf("In %s function (initialization).\n", __func__);
}

void real_func(void)
{
    printf("In %s function (real functional executed).\n", __func__);
}

int main()
{
    int cnt = 10;

    init1();
    init2();
    real_func();
    init2();

    printf("The initialization has been finished! You can dump now.\n");
    
    while (cnt--) {
        printf("[%2d]\n", cnt);
        sleep(1);
    }

    real_func();
    
    return 0;
}
