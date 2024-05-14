# ============= Makefile ============= #

CC = g++
DIROBJS = obj
DIRLOGS = logs
CREATE_DIROBJS = mkdir -p $(DIROBJS)
CREATE_DIRLOGS = mkdir -p $(DIRLOGS)


all: runClient runServer
	$(CREATE_DIROBJS)
	$(CREATE_DIRLOGS)

runClient: client/client.cpp
	$(CC) client/client.cpp tools/logger.cpp tools/utils.cpp -o runClient

runServer: server/server.cpp
	$(CC) server/server.cpp tools/logger.cpp tools/utils.cpp tools/searcher.cpp template/images.cpp tools/timer.cpp -o runServer

clean:
	rm -f runClient runServer
	if [ -d $(DIROBJS) ]; then rm -r $(DIROBJS); fi
# if [ -d $(DIRLOGS) ]; then rm -r $(DIRLOGS); fi

# -Wall -Werror -pedantic