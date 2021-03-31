#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdint.h>

#define __USE_GNU
#include <signal.h>
#include <ucontext.h>

#define OFFSET_MASK 	0xFFFUL

int trap_map[][2] = {
    #include "config.h"
};

void trap_handler(int sig, siginfo_t *si, void* arg)
{
    ucontext_t *context = (ucontext_t *)arg;
    uint64_t rip = context->uc_mcontext.gregs[REG_RIP];
    size_t arr_len = sizeof(trap_map) / (2*sizeof(int));
    int i;

    printf("\n===%s===\nSignal #%d. arr_len %lu. rip: 0x%lx\n", __func__,
            sig, arr_len, rip);
    for (i = 0; i < arr_len; i++) {
        if ((rip & OFFSET_MASK) == trap_map[i][0]) {
            printf("Found sig handler offset: 0x%x. rip: ++0x%x\n", trap_map[i][0],
                trap_map[i][1]);
            rip += trap_map[i][1];
        }
    }
    context->uc_mcontext.gregs[REG_RIP] = rip;
    printf("Updated rip 0x%lx\n===%s===\n\n", rip, __func__);
}

__attribute__((constructor)) void initFunc()
{
   	struct sigaction sa;
    sa.sa_sigaction = &trap_handler;
	sa.sa_flags = SA_SIGINFO; /* Use sa_sigaction instead of sa_handler. */
	sigaction(SIGTRAP, &sa, NULL);
}