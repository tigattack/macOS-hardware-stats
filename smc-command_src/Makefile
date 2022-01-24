CC = gcc
CFLAGS = -mmacosx-version-min=10.4  -Wall -g -framework IOKit
CPPFLAGS = -DCMD_TOOL_BUILD
DESTDIR = /usr/local/bin

all: smc

smc: smc.o
	$(CC) $(CFLAGS) -o smc smc.o

smc.o: smc.h smc.c
	$(CC) $(CPPFLAGS) -c smc.c

.PHONY: clean
clean:
	-rm -f smc smc.o

.PHONY: install
install:
	install -m 755 smc $(DESTDIR)/smc
