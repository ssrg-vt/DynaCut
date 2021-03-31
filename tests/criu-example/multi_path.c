#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>

void func_path_a()
{
    asm("int3");
    printf("%s: You cannot see me unless you advance a correct value to RIP\n",
            __func__);
}

void func_path_b()
{
    asm("int3");
    asm("int3");
    printf("%s: You cannot see me unless you advance a correct value to RIP\n",
            __func__);
}

/**
 * @brief Use ./multi_path -a | -b | -n <loop cnt>
 */
int main(int argc, char *argv[])
{
    int i = 0, cnt = 5;
    int flags, opt;

    /**
     * @brief Simulate a multi-option program.
     */
    while ((opt = getopt(argc, argv, "abn:")) != -1) {
        switch (opt) {
        case 'a':
            flags = 1;
            break;
        case 'b':
            flags = 2;
            break;
        case 'n':
            cnt = atoi(optarg);
            break;
        default: /* '?' */
            fprintf(stderr, "Usage: %s [-c loop_cnt] [-a] [-b]\n",
                    argv[0]);
            exit(EXIT_FAILURE);
        }
    }
    printf("pid: %d, cnt: %d \n", getpid(), cnt);

    if (flags == 1) func_path_a();
    if (flags == 2) func_path_b();

    while(i < cnt) {
        sleep(5);
        printf("%d \n", ++i);
    }
    asm("int3");
    asm("int3");
    asm("int3");
    printf("%s: You cannot see me unless you use some tricks :)\n", __func__);
    return 0;
}


