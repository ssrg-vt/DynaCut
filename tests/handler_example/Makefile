all:
	gcc -shared -Wall -g -o libhandler.so handler.c
	gcc -shared -Wall -g -o sig.so sig.c
	gcc -shared -Wall -g -o sighandler.so sighandler.c
	gcc -shared -Wall -fPIC -g -o multi_sig.so multi_sig.c

clean:
	rm -rf *.o libhandler.so sig.so sighandler.so
