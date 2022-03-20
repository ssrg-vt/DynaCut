#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/stat.h>
#include <fcntl.h>

#define __USE_GNU
#include <signal.h>
#include <ucontext.h>

#define OFFSET_MASK	0xFFFUL

uint64_t trap_maps[][2] = {
    #include "init_addr_map.h"
};

/**
 * @brief Handling int3 exceptions: record all fault locations to a file.
 * 
 * @param sig 
 * @param si 
 * @param arg 
 */
void trap_handler(int sig, siginfo_t *si, void* arg)
{
    ucontext_t *context = (ucontext_t *)arg;
    uint64_t rip = context->uc_mcontext.gregs[REG_RIP];

    size_t trap_maps_len = sizeof(trap_maps) / (sizeof(uint64_t)*2);
    uint8_t byte = 0;

    int fd = open("allowlist.txt", O_CREAT|O_RDWR|O_APPEND, S_IWRITE|S_IREAD);
    printf("\n=== %s ===\nSignal #%d. arr_len %lu. rip: 0x%lx\n", __func__,
            sig, trap_maps_len, rip);
    for (int i = 0; i < trap_maps_len; i++) {
        if ((rip -1) == trap_maps[i][0]) {
            printf("Found trap address @0x%lx. offset: 0x%lx\n",
                trap_maps[i][0], trap_maps[i][1]);

            /* replace INT3 with the data byte at the location */
            byte = (uint8_t)trap_maps[i][1];
            *(uint8_t*)(rip-1) = byte;

            /* write the address of the trap to the file */
            rip -= 1;
            dprintf(fd, "0x%lx\n", rip);
        }
    }
    close(fd);
    context->uc_mcontext.gregs[REG_RIP] = rip;
    printf("Updated rip 0x%lx\n=== %s ===\n\n", rip, __func__);
}
