# Build, run and dynamic customize a test program
## Build the toy program
Build the toy application with:
```
❯ make -C tests/example multi_path
```
The `multi_path` program accecpts 3 parameters and has 3 code paths. `./multi_path -a` and `./multi_path -b` will call `function_path_a()` and `function_path_b()` respectively. In both function, we inserted `int3` instructions. Using `-n` with an integer number will cause the `main()` function to sleep `5*n` seconds before hitting another code blocks of `int3`.

In `multi_path`, each `int3` code block indicates an unwanted feature that we don't want to touch. To disable that feature dynamically, we checkpoint the running process with CRIU and use our tool to inject a signal handler that skips the `int3` code blocks.

The following commands show what happens when running `multi_path` directly without dynamic code customization:
```
❯ ./tests/example/multi_path -a
pid: 151500, cnt: 5 
In function func_path_a, trap (int3) next ...
zsh: trace trap (core dumped)  ./tests/example/multi_path -a
❯ ./tests/example/multi_path -b
pid: 151509, cnt: 5 
In function func_path_b, trap (int3) next ...
zsh: trace trap (core dumped)  ./tests/example/multi_path -b
❯ dmesg|tail -n 2
[1623504.942755] traps: multi_path[151500] trap int3 ip:55555555522a sp:7fffffffe930 error:0 in multi_path[555555555000+1000]
[1623509.116895] traps: multi_path[151509] trap int3 ip:555555555266 sp:7fffffffe930 error:0 in multi_path[555555555000+1000]

❯ ./tests/example/multi_path -n 2
pid: 1016353, cnt: 2
1
2
In function main, trap (int3) next ...
zsh: trace trap (core dumped)  ./tests/example/multi_path -n 2
❯ dmesg|tail -n 1
[4168258.792816] traps: multi_path[1016353] trap int3 ip:5555555553b4 sp:7fffffffe950 error:0 in multi_path[555555555000+1000]
```

## Disable the `int3` code blocks by dynamically injecting a signal handler
First, we need to indentify the unwanted code block locations. You can use
`objdump -S <bin>` to find the `int3` code block location and the length. Fill
the value pairs to `tests/sighandler/config.h`. The following is an example:
```
❯ cat tests/sighandler/config.h
{0x229, 1}, {0x2265, 2}, {0x3b3, 3}
```
Next, build the signal handler:
```
❯ make -C tests/sighandler multi_path_sighandler
```

Now let's checkpoint a running process. You need to open two terminals one for running this toy program, the other for checkpointing this running process with our script.
```
# Terminal 1
❯ ./tests/example/multi_path -n 7
pid: 1017144, cnt: 7
1
2
3
zsh: killed     ./tests/example/multi_path -n 7
```
```
# Terminal 2
❯ ./tools/scripts/dump.sh multi_path
```
The saved process image should be in `./vanilla-dump`.

Use the CRIT tool to rewrite the process image by adding a signal handler:
```
❯ ./criu/crit/crit edit insert sighandler vanilla-dump 0x1000000 -path $(pwd)/tests/sighandler/multi_sig.so
```

Let's restore the modified process:
```
❯ ./tools/scripts/restore.sh vanilla-dump
4 
5 
6 
7 
In function main, trap (int3) next ...

===trap_handler===
Signal #5. arr_len 3. rip: 0x55d3ece7e3b4
Found sig handler offset: 0x3b3. rip: ++3
Updated rip 0x55d3ece7e3b6
===trap_handler===

main: You cannot see me unless you use some tricks :)
```