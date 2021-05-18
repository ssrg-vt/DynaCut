all:
	make -C tests/example
	make -C tests/sighandler

clean:
	make -C tests/example clean
	make -C tests/sighandler clean
	rm tags cscope.* -rf

tags:
	@echo "[GEN] tags"
	@ctags -R --exclude=@.ctagsignore

#cscope:
#	@echo "[GEN] cscope"
#	@find . \
		\( -path "./criu/criu/*" -o -path "./criu/include/*" \) \
		\( -name "*.[ch]" -o -name "*.cpp" \) \
		-print > $(PWD)/cscope.files
#	@cscope -b -q -k

.PHONY: clean tags #cscope
