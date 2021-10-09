# Dynamically remove unwanted features for Redis-server
## Build the Redis-server from source
The first step is to identify the code to remove. Here we leverage the [code coverage tool in DynamoRIO](https://dynamorio.org/page_drcov.html) to dump out which basic blocks have been executed.

Unzip the redis tar ball (`tests/redis-6.2.3.tar.gz`) to the `tests` directory, and build the `redis server/benchmark`:
```
❯ ls
tests   tools   criu   DynamoRIO-Linux-8.0.0-1   ...
❯ cd tests; tar xvf redis-6.2.3.tar.gz; cd ..
❯ make -C tests/redis-6.2.3
...
    LINK redis-server
    INSTALL redis-sentinel
    LINK redis-cli
    LINK redis-benchmark
...
```
## Find the basic blocks of the unwanted feature
In this example, we consider redis `set` is an unwanted feature, and consider `get`, `ping` are wanted feature. To find the BB of the unwanted feature, follow steps 1 - 4:

1. Start the `redis-server` with the DynamoRIO code coverage tool running:
```
❯ ./DynamoRIO-Linux-8.0.0-1/bin64/drrun -t drcov -dump_text -- ./tests/redis-6.2.3/src/redis-server
```

2. Generate the code coverage trace of **wanted features**:

Open a new terminal, generate requests for wanted features and terminate the `redis-server` process (type `ctrl-c` on the `redis-server` terminal)
```
❯ ./tests/redis-6.2.3/src/redis-benchmark -q -t get -n 100
❯ ./tests/redis-6.2.3/src/redis-benchmark -q -t ping -n 100
```
Now you can get a DynamoRIO log similar to `drcov.redis-server.581030.0000.proc.log`. Rename it to `redis_wanted_feature.log` (by typing `mv drcov.redis-server.581030.0000.proc.log redis_wanted_feature.log`).

Note: If you have multiple code coverage logs for wanted features, you can merge them into one log with `sort -u`:
```
❯ sort -u drcov.redis-server.ping.log drcov.redis-server.get.log > redis_wanted_feature.log
```

3. Generate the code coverage trace of **unwanted features**:

Repeat step 1, and for step 2, we want to generate the log of unwanted features (e.g., we assume the Redis `set` is an unwanted feature)
```
❯ ./tests/redis-6.2.3/src/redis-benchmark -q -t set -n 100
```
Terminate the `redis-server` process. Rename the DynamoRIO log to `redis_unwanted_feature.log`

4. Run a script to filter out the unwanted basic blocks.
```
❯ ./tools/scripts/logdiff.py -u redis_unwanted_feature.log -b redis_wanted_feature.log
The unwanted feature log file: redis_unwanted_feature.log
The wanted log file: redis_wanted_feature.log

[  0] BB Table: 18145 bbs
[  1] module[  5]: 0x0000000000163870,  37
[  2] module[  5]: 0x000000000016943d,  23
[  3] module[  5]: 0x0000000000169454,  10
[  4] module[  5]: 0x000000000016945e,   5
[  5] module[  5]: 0x0000000000169463,  33
[  6] module[  5]: 0x000000000016949a,  21
[  7] module[  5]: 0x0000000000169360,  59
[  8] module[  5]: 0x000000000004ec71,  14
[  9] module[  5]: 0x000000000004ee33,  17
... ...
```
If we look at source code of this basic block `0x4ec71`, it is in `src/server.c:processCommand(client *c)` function. It passes the command from the client. By comparing the code coverage log, we can deduce the basic block `0x4ec71` is the code that handles the `set` command in `processCommand(client *c)`.

## Disable the unwanted feature by rewriting the CRIU process image
We can do *simple feature disable* or *full feature removal*. To simply disable a feature, we inject `int3` at the beginning of an unwanted feature basic block. We can also insert a simple signal handler that calls `exit()` on executing that `int3` trap instruction.

The following instructions will describe how to dynamically remove unwanted features by blocking the unwanted basic blocks:

Start the `redis-server` (`./tests/redis-6.2.3/src/redis-server`). Checkpoint the running `redis-server` with the following command:
```
❯ ./tools/scripts/dump.sh redis-server
❯ mv vanilla-dump redis.img
```

Before inserting the signal handler, we can examine the memory layout:
```
❯ ./criu/crit/crit x redis.img mems
159906
	exe                                     /<path to redis>/redis-6.2.3/src/redis-server
	555555554000-555555594000           r-- /<path to redis>/redis-6.2.3/src/redis-server
	555555594000-5555556eb000           r-x /<path to redis>/redis-6.2.3/src/redis-server + 0x40000
... ...
```
We can insert the signal handler at any address not being used. For example, we insert the signal handler at `0x1000000`:
```
❯ ./criu/crit/crit edit insert sighandler redis.img 0x1000000 -path $(pwd)/tests/sighandler/libhandler.so
❯ ./criu/crit/crit edit insert int3 redis.img 0x555555554000 -offset 0x4ec71
```
We also inserted the `int3` at the beginning of the basic block `0x4ec71` obtained from step 4. Let's check the updated memory layout:
```
❯ ./criu/crit/crit x redis.img mems
159906
	exe                               /<path to redis>/redis-6.2.3/src/redis-server
	01000000-01001000             r-- /<path to DynaCut>/DynaCut/tests/sighandler/libhandler.so
	01001000-01002000             r-x /<path to DynaCut>/DynaCut/tests/sighandler/libhandler.so + 0x1000
	01002000-01003000             r-- /<path to DynaCut>/DynaCut/tests/sighandler/libhandler.so + 0x2000
	01003000-01005000             rw- /<path to DynaCut>/DynaCut/tests/sighandler/libhandler.so + 0x2000
	555555554000-555555594000     r-- /<path to redis>/redis-6.2.3/src/redis-server
	555555594000-5555556eb000     r-x /<path to redis>/redis-6.2.3/src/redis-server + 0x40000
... ...
```
## Test the correctness of dynamic feature removal
We use the `redis-benchmark` to test the `redis-server`'s response to different requests.
```
❯ ./tests/redis-6.2.3/src/redis-benchmark -q -t ping -n 1000
PING_INLINE: 100000.00 requests per second, p50=0.239 msec         
PING_MBULK: 100000.00 requests per second, p50=0.247 msec

❯ ./tests/redis-6.2.3/src/redis-benchmark -q -t get -n 1000
GET: 111111.12 requests per second, p50=0.223 msec         

❯ ./tests/redis-6.2.3/src/redis-benchmark -q -t set -n 1000
Error: Connection reset by peer_msec=-nan (overall: -nan)
```
As expected, the `redis-server` exits when receiving the `set` test case.
```
❯ ./tools/scripts/restore.sh redis.img
The PID is 159906. signal #5. rip: 0x5555555a2c71
The signal is: 5
```
