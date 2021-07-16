all:
	gcc -shared -Wall -g -o libhandler.so handler.c
	gcc -shared -Wall -g -o sig.so sig.c
	gcc -shared -Wall -fPIC -g -o sighandler.so sighandler.c
	gcc -shared -Wall -fPIC -g -o multi_sig.so multi_sig.c
	gcc -shared -Wall -fPIC -g -o multi_sig_init.so multi_sig_init.c

multi_path_sighandler:
	gcc -shared -Wall -fPIC -g -o multi_sig.so multi_sig.c

simple_handler:
	gcc -shared -Wall -fPIC -g -o libhandler.so handler.c

init_handler: 
	gcc -shared -Wall -fPIC -g -o multi_sig_init.so multi_sig_init.c

clean:
	rm -rf *.o libhandler.so sig.so sighandler.so
