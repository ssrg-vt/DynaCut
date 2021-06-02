/* **********************************************************
 * Copyright (c) 2014-2018 Google, Inc.  All rights reserved.
 * Copyright (c) 2008 VMware, Inc.  All rights reserved.
 * **********************************************************/

/*
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * * Redistributions of source code must retain the above copyright notice,
 *   this list of conditions and the following disclaimer.
 *
 * * Redistributions in binary form must reproduce the above copyright notice,
 *   this list of conditions and the following disclaimer in the documentation
 *   and/or other materials provided with the distribution.
 *
 * * Neither the name of VMware, Inc. nor the names of its contributors may be
 *   used to endorse or promote products derived from this software without
 *   specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL VMWARE, INC. OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 */

/* Code Manipulation API Sample:
 * bbcount.c
 *
 * Reports the dynamic execution count of all basic blocks.
 * Illustrates how to perform performant inline increments with analysis
 * on whether flags need to be preserved.
 */

#include <stddef.h> /* for offsetof */
#include <limits.h> /* for USHRT_MAX */
#include "dr_api.h"
#include "drmgr.h"
#include "drreg.h"
#include "drx.h"
#include "utils.h"
#include "drcovlib.h"

#ifdef WINDOWS
#    define DISPLAY_STRING(msg) dr_messagebox(msg)
#else
#    define DISPLAY_STRING(msg) dr_printf("%s\n", msg);
#endif

#define NULL_TERMINATE(buf) (buf)[(sizeof((buf)) / sizeof((buf)[0])) - 1] = '\0'

#define TESTALL(mask, var) (((mask) & (var)) == (mask))
#define TESTANY(mask, var) (((mask) & (var)) != 0)

#define ASSERT(x)                                            \
    do {                                                     \
        if (!(x)) {                                          \
            dr_printf("ASSERT failed on line %d", __LINE__); \
            dr_flush_file(STDOUT);                           \
            dr_abort();                                      \
        }                                                    \
    } while (0)

#define HASH_TABLE_SIZE 10000
#define UNKNOWN_MODULE_ID USHRT_MAX

typedef struct node {
    int count;
    app_pc addr;
    uint64 timestamp_first;
    uint64 timestamp_last;
    uint start;
    ushort mod_id;
    uint size;
} node_t;

typedef node_t **hash_table_t;

static client_id_t client_id;
static int tls_idx;
static uint64 timestamp_start = 0;
static uint64 fork_timestamp = 0;

/* thread private log file and hashtable */
typedef struct {
    hash_table_t table;
    file_t log;
} per_thread_t;

static node_t *
new_elem(app_pc addr, void *drcontext, app_pc start, uint size)
{
    node_t *elem = (node_t *)dr_thread_alloc(drcontext, sizeof(node_t));
    ASSERT(elem != NULL);

    uint mod_id;
    app_pc mod_start;

    //elem-> count = 1;
    elem -> addr = addr;
    elem -> timestamp_first = dr_get_microseconds() - timestamp_start;
    elem -> size = size;
    drcovlib_status_t res = drmodtrack_lookup(drcontext, start, &mod_id, &mod_start);
    if (res == DRCOVLIB_SUCCESS) {
        if(!(mod_id < USHRT_MAX))
            dr_fprintf(STDERR, "module id overflow");
        elem->mod_id = (ushort)mod_id;
        if(!(start > mod_start))
            dr_fprintf(STDERR, "wrong module");
        elem->start = (uint)(start - mod_start);
    }
    else {
        /* XXX: we just truncate the address, which may have wrong value
         * in x64 arch. It should be ok now since it is an unknown module,
         * which will be ignored in the post-processing.
         * Should be handled for JIT code in the future.
         */
        elem->mod_id = UNKNOWN_MODULE_ID;
        elem->start = (uint)(ptr_uint_t)start;
    }

    return elem;
}

static void
delete_elem(node_t *elem, void *drcontext)
{
    dr_thread_free(drcontext, elem, sizeof(node_t));
}

hash_table_t
new_table(void *drcontext)
{
    int i;
    hash_table_t table =
        (hash_table_t)dr_thread_alloc(drcontext, sizeof(node_t *) * HASH_TABLE_SIZE);

    for (i = 0; i < HASH_TABLE_SIZE; i++) {
        table[i] = NULL;
    }

    return table;
}

void
delete_table(hash_table_t table, void *drcontext)
{
    int i;
    for (i = 0; i < HASH_TABLE_SIZE; i++) {
        if (table[i] != NULL) {
            delete_elem(table[i], drcontext);
        }
    }

    dr_thread_free(drcontext, table, sizeof(node_t *) * HASH_TABLE_SIZE);
}

static uint
hash_func(app_pc addr)
{
    return ((uint)(((ptr_uint_t)addr) % HASH_TABLE_SIZE));
}

node_t *
lookup(hash_table_t table, app_pc addr)
{
    node_t *node = table[hash_func(addr)];
    if (node != NULL)
        return node;
    return NULL;
}

void
insert(hash_table_t table, app_pc addr, void *drcontext, app_pc start, uint size)
{
    node_t *elem = new_elem(addr, drcontext, start, size);

    uint index = hash_func(addr);
    node_t *node = table[index];
    if (node == NULL) {
        table[index] = elem;
    }
}

#ifdef SHOW_RESULTS
/* some meta-stats: static (not per-execution) */
static int bbs_eflags_saved;
static int bbs_no_eflags_saved;
#endif

static void
event_thread_init(void *drcontext)
{
    per_thread_t *data = (per_thread_t *)dr_thread_alloc(drcontext, sizeof(per_thread_t));
    data -> log =
        log_file_open(client_id, drcontext, NULL /* using client lib path */, "bbcount",
#ifndef WINDOWS
                      DR_FILE_CLOSE_ON_FORK |
#endif
                          DR_FILE_ALLOW_LARGE);
    DR_ASSERT(data -> log != INVALID_FILE);
    drmgr_set_tls_field(drcontext, tls_idx, data);
    data -> table = new_table(drcontext);
    dr_log(drcontext, DR_LOG_ALL, 1, "countBBs: set up for thread " TIDFMT "\n",
           dr_get_thread_id(drcontext));
}

static void
event_thread_exit(void *drcontext)
{
    per_thread_t *data = (per_thread_t *)drmgr_get_tls_field(drcontext, tls_idx);
    /* Print all the hash table contents seen over the life of the process */
    int i;
    drmodtrack_dump(data->log);
    dr_fprintf(data -> log, "\n");
    dr_fprintf(data->log, "BB Table: Module ID, BB addess, size, execution count, timestamp \n");
    hash_table_t table = data -> table;
    for (i = 0; i < HASH_TABLE_SIZE; i++) {
        if (table[i] != NULL) {
            node_t *iter = table[i];
                dr_fprintf(data -> log, "[%2hu] " PFX ": %5d timestamp_first: %10lu timestamp_last: %10lu\n",\
                 iter-> mod_id, iter->start, iter->size,\
                 iter-> timestamp_first, iter-> timestamp_last);
        }
    }
    delete_table(table, drcontext);
    log_file_close(data->log);
}

#ifndef WINDOWS
static void
event_fork(void *drcontext)
{
    per_thread_t *data = drmgr_get_tls_field(drcontext, tls_idx);

    fork_timestamp = dr_get_microseconds() - timestamp_start;
    dr_fprintf(STDERR, "The fork timestamp is: %lu\n", fork_timestamp);
    if (data != NULL) {
        dr_close_file(data->log);
        if (drcontext == NULL) {
        dr_fprintf(STDERR, "drcov_per_thread should not be set");
        dr_global_free(data, sizeof(*data));
    } else {
        dr_fprintf(STDERR, "drcov_per_thread is not set");
        dr_thread_free(drcontext, data, sizeof(*data));
    }
    }
    event_thread_init(drcontext);
}
#endif

static void
event_exit(void)
{
    if (!drmgr_unregister_tls_field(tls_idx))
        DR_ASSERT(false);
    drmodtrack_exit();
    drx_exit();
    drreg_exit();
    drmgr_exit();
}

static dr_emit_flags_t
event_app_instruction(void *drcontext, void *tag, instrlist_t *bb, /*instr_t *instr ,*/
                      bool for_trace, bool translating, OUT void **user_data)
{
/* ignore tool-inserted instrumentation */
if (translating)
    return DR_EMIT_DEFAULT;

    app_pc tag_pc, start_pc, end_pc;
    node_t *elem;
    /* to find size */
    instr_t *instr_iter;
    /* By default drmgr enables auto-predication, which predicates all instructions with
     * the predicate of the current instruction on ARM.
     * We disable it here because we want to unconditionally execute the following
     * instrumentation.
     */

    tag_pc = dr_fragment_app_pc(tag);
    start_pc = instr_get_app_pc(instrlist_first_app(bb));
    if (dr_using_all_private_caches()) {
    per_thread_t *data = (per_thread_t *)drmgr_get_tls_field(drcontext, tls_idx);
    hash_table_t table = data -> table;
    //src = instr_get_app_pc(instr);
    elem = lookup(table, start_pc);

    end_pc = start_pc; /* for finding the size */
    for (instr_iter = instrlist_first_app(bb); instr_iter != NULL;
         instr_iter = instr_get_next_app(instr_iter)) {
        app_pc pc = instr_get_app_pc(instr_iter);
        int len = instr_length(drcontext, instr_iter);
        /* -opt_speed (elision) is not supported */
        /* For rep str expansion pc may be one back from start pc but equal to the tag. */
        if(!(pc != NULL && (pc >= start_pc || pc == tag_pc)))
               dr_printf("-opt_speed is not supported");
        if (pc + len > end_pc)
            end_pc = pc + len;
    }
    if (elem == NULL) {
        insert(table, start_pc, drcontext, tag_pc, (end_pc - start_pc));
    }
    else {
        elem -> timestamp_last = dr_get_microseconds() - timestamp_start;
            // drx_insert_counter_update(drcontext, bb, instr,
            //                   /* We're using drmgr, so these slots
            //                    * here won't be used: drreg's slots will be.
            //                    */
            //                   SPILL_SLOT_MAX + 1,
            //                   IF_AARCHXX_(SPILL_SLOT_MAX + 1) & elem -> count, 1, 0);
    }
    }
    // drmgr_disable_auto_predication(drcontext, bb);
    // if (!drmgr_is_first_instr(drcontext, instr))
    //     return DR_EMIT_DEFAULT;

#ifdef VERBOSE
    dr_printf("in dynamorio_basic_block(tag=" PFX ")\n", tag);
#    ifdef VERBOSE_VERBOSE
    instrlist_disassemble(drcontext, tag, bb, STDOUT);
#    endif
#endif

// #ifdef SHOW_RESULTS
//     if (drreg_are_aflags_dead(drcontext, instr, &aflags_dead) == DRREG_SUCCESS &&
//         !aflags_dead)
//         bbs_eflags_saved++;
//     else
//         bbs_no_eflags_saved++;
// #endif

#if defined(VERBOSE) && defined(VERBOSE_VERBOSE)
    dr_printf("Finished instrumenting dynamorio_basic_block(tag=" PFX ")\n", tag);
    instrlist_disassemble(drcontext, tag, bb, STDOUT);
#endif
    return DR_EMIT_DEFAULT;
}

DR_EXPORT void
dr_client_main(client_id_t id, int argc, const char *argv[])
{
    drcovlib_status_t res;
    timestamp_start = dr_get_microseconds();
    drreg_options_t ops = { sizeof(ops), 1 /*max slots needed: aflags*/, false };
    dr_set_client_name("DynamoRIO Sample Client 'bbcount'",
                       "http://dynamorio.org/issues");
    if (!drmgr_init() || !drx_init() || drreg_init(&ops) != DRREG_SUCCESS)
        DR_ASSERT(false);
    
    client_id = id;
    tls_idx = drmgr_register_tls_field();

    /* register events */
    dr_register_exit_event(event_exit);
    if (!drmgr_register_thread_init_event(event_thread_init) ||
        !drmgr_register_thread_exit_event(event_thread_exit) ||
        !drmgr_register_bb_instrumentation_event(event_app_instruction, NULL, NULL))
        DR_ASSERT(false);
    
    #ifdef UNIX
        dr_register_fork_init_event(event_fork);
    #endif
    drmodtrack_init();
    dr_fprintf(STDERR, "Init done\n");
    /* make it easy to tell, by looking at log file, which client executed */
    dr_log(NULL, DR_LOG_ALL, 1, "Client 'bbcount' initializing\n");
#ifdef SHOW_RESULTS
    /* also give notification to stderr */
    if (dr_is_notify_on()) {
#    ifdef WINDOWS
        /* ask for best-effort printing to cmd window.  must be called at init. */
        dr_enable_console_printing();
#    endif
        dr_fprintf(STDERR, "Client bbcount is running\n");
    }
#endif
}
