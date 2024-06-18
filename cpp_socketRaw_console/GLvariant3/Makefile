# ============= Makefile ============= #

CC = g++
DIROBJS = obj
DIRLOGS = logs
DIRTOOLS = tools
DIRPACKAGE = package
DIRLINUX = linux
CREATE_DIROBJS = mkdir -p $(DIROBJS)
CREATE_DIRLOGS = mkdir -p $(DIRLOGS)

all: folders runClient runServer runProxy

folders:
	$(CREATE_DIROBJS)
	$(CREATE_DIRLOGS)

runClient: client/runClient.cpp $(DIROBJS)/logger.o $(DIROBJS)/utils.o $(DIROBJS)/package.o $(DIROBJS)/settingsOS.o
	$(CC) client/runClient.cpp $(DIRTOOLS)/client.cpp \
		$(DIROBJS)/logger.o $(DIROBJS)/utils.o \
		$(DIROBJS)/package.o $(DIROBJS)/settingsOS.o \
		-o runClient -Wall -Werror -pedantic

runServer: server/runServer.cpp $(DIROBJS)/logger.o $(DIROBJS)/utils.o $(DIROBJS)/package.o $(DIROBJS)/settingsOS.o $(DIROBJS)/searcher.o $(DIROBJS)/audio.o
	$(CC) server/runServer.cpp $(DIRTOOLS)/server.cpp \
		$(DIROBJS)/logger.o $(DIROBJS)/utils.o \
		$(DIROBJS)/package.o $(DIROBJS)/settingsOS.o \
		$(DIROBJS)/searcher.o $(DIROBJS)/audio.o \
		-o runServer -Wall -Werror -pedantic -lSDL2 -lSDL2_mixer

runProxy: middleware/runProxy.cpp $(DIROBJS)/logger.o $(DIROBJS)/utils.o $(DIROBJS)/package.o $(DIROBJS)/settingsOS.o
	$(CC) middleware/runProxy.cpp $(DIRTOOLS)/proxy.cpp \
		$(DIROBJS)/logger.o $(DIROBJS)/utils.o \
		$(DIROBJS)/package.o $(DIROBJS)/settingsOS.o \
		-o runProxy -Wall -Werror -pedantic

$(DIROBJS)/logger.o: tools/logger.cpp
	$(CC) -c tools/logger.cpp -o $(DIROBJS)/logger.o

$(DIROBJS)/utils.o: tools/utils.cpp
	$(CC) -c tools/utils.cpp -o $(DIROBJS)/utils.o

$(DIROBJS)/package.o: package/package.cpp
	$(CC) -c package/package.cpp -o $(DIROBJS)/package.o

$(DIROBJS)/settingsOS.o: linux/settingsOS.cpp
	$(CC) -c linux/settingsOS.cpp -o $(DIROBJS)/settingsOS.o

$(DIROBJS)/searcher.o: sources/searcher.cpp
	$(CC) -c sources/searcher.cpp -o $(DIROBJS)/searcher.o

$(DIROBJS)/audio.o: audio/audio.cpp
	$(CC) -c audio/audio.cpp -o $(DIROBJS)/audio.o

clean:
	rm -f runClient runServer runProxy
	if [ -d $(DIROBJS) ]; then rm -r $(DIROBJS); fi
# if [ -d $(DIRLOGS) ]; then rm -r $(DIRLOGS); fi
