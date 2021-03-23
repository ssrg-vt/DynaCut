all: criu-example simple

criu-example: criu-example.c
	gcc -Wall -g -o $@ $<

simple: simple.c
	gcc -Wall -g -o $@ $<

clean:
	rm -rf *.o criu-example simple
