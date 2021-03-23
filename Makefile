all:
	make -C tests/criu-example
	make -C tests/handler_example

clean:
	make -C tests/criu-example clean
	make -C tests/handler_example clean