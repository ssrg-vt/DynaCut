all: criu-example simple multi_path init-example

criu-example: criu-example.c
	gcc -Wall -g -o $@ $<

simple: simple.c
	gcc -Wall -g -o $@ $<

multi_path: multi_path.c
	gcc -Wall -g -o $@ $<

loop: stack_obj_func_loop.c
	gcc -Wall -g -o $@ $<

init-example: init-example.c
	gcc -Wall -g -o $@ $<

clean:
	rm -rf *.o criu-example simple multi_path loop init-example
