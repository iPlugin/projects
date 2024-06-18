# ============= Makefile ============= #

CC = g++
DIROBJS = obj
DIRLOGS = logs
CREATE_DIROBJS = mkdir -p $(DIROBJS)
CREATE_DIRLOGS = mkdir -p $(DIRLOGS)


all: folders runClient runServer

folders:
	$(CREATE_DIROBJS)
	$(CREATE_DIRLOGS)

runClient: client/run_client.cpp logger utils
	$(CC) client/run_client.cpp tools/client.cpp \
		$(DIROBJS)/logger.o $(DIROBJS)/utils.o \
			-o runClient -Wall -Werror -pedantic

runServer: server/run_server.cpp server logger utils searcher images
	$(CC) server/run_server.cpp tools/server.cpp \
		$(DIROBJS)/logger.o $(DIROBJS)/utils.o \
		$(DIROBJS)/searcher.o $(DIROBJS)/images.o \
			-o runServer -Wall -Werror -pedantic

logger: tools/logger.cpp
	$(CC) -c tools/logger.cpp \
		-o $(DIROBJS)/logger.o

utils: tools/utils.cpp
	$(CC) -c tools/utils.cpp \
		-o $(DIROBJS)/utils.o

searcher: tools/searcher.cpp
	$(CC) -c tools/searcher.cpp \
		-o $(DIROBJS)/searcher.o

images: template/images.cpp
	$(CC) -c template/images.cpp \
		-o $(DIROBJS)/images.o


clean:
	rm -f runClient runServer
	if [ -d $(DIROBJS) ]; then rm -r $(DIROBJS); fi
# if [ -d $(DIRLOGS) ]; then rm -r $(DIRLOGS); fi
