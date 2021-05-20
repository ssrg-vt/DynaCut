#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

#define __USE_GNU
#include <signal.h>
#include <ucontext.h>

#define ADVANCE	2

void trap_handler(int sig, siginfo_t *si, void* arg)
{
    ucontext_t *context = (ucontext_t *)arg;
    printf("signal #%d. rip: 0x%llx\n", sig, context->uc_mcontext.gregs[REG_RIP]);
    printf("The signal is: %d\n", sig);
    context->uc_mcontext.gregs[REG_RIP] += ADVANCE;
    printf("Updated rip by advancing it %d\n", ADVANCE);
//    exit(1);
}
