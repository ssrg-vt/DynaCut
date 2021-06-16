#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/stat.h>
#include <fcntl.h>

#define __USE_GNU
#include <signal.h>
#include <ucontext.h>

#define OFFSET_MASK 	0xFFFUL

uint64_t trap_map_address[] = {
#include "config_init_address.h"
};

int trap_map_data[] = {
#include "config_init_data.h"
};

uint64_t base_address = {
#include"config_base.h"
};

void trap_handler(int sig, siginfo_t *si, void* arg)
{
    ucontext_t *context = (ucontext_t *)arg;
    uint64_t rip = context->uc_mcontext.gregs[REG_RIP];
    size_t arr_len_data = sizeof(trap_map_data) / (sizeof(int));
    int i;
    uint8_t byte = 0;
    int fd = open("locations.txt", O_CREAT | O_RDWR | O_APPEND, S_IRWXU);
    printf("\n===%s===\nSignal #%d. arr_len %lu. rip: 0x%lx\n", __func__,
            sig, arr_len_data, rip);
    for (i = 0; i < arr_len_data; i++) {
        if ((rip - base_address -1) == trap_map_address[i]) {
            printf("Found sig handler offset: 0x%x. rip: ++0x%lx\n", trap_map_data[i],
                trap_map_address[i]);

            /* replace INT3 with the data byte at the location */
            byte = (uint8_t)trap_map_data[i];
            *(uint8_t*)(rip-1) = byte;

            /* write the address of the trap to the file */
            rip -= 1;
            write(fd, &rip, sizeof(rip));
        }
    }
    close(fd);
    context->uc_mcontext.gregs[REG_RIP] = rip;
    printf("Updated rip 0x%lx\n===%s===\n\n", rip, __func__);
}