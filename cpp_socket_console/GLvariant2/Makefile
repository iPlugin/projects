# ============= Makefile ============= #

# [ Configuration variables ]
CXX = g++ # Компілятор
CXXFLAGS = -std=c++17 -pthread -Iinclude # Прапори компілятора
LDFLAGS = -lcurl # Прапори бібліотек

# Folders
DIROBJS = obj

# Компіляція liboai файлів
LIBOAI_OBJS = $(DIROBJS)/audio.o \
              $(DIROBJS)/azure.o \
              $(DIROBJS)/chat.o \
              $(DIROBJS)/completions.o \
              $(DIROBJS)/edits.o \
              $(DIROBJS)/embeddings.o \
              $(DIROBJS)/files.o \
              $(DIROBJS)/fine_tunes.o \
              $(DIROBJS)/images.o \
              $(DIROBJS)/models.o \
              $(DIROBJS)/moderations.o \
              $(DIROBJS)/authorization.o \
              $(DIROBJS)/netimpl.o \
              $(DIROBJS)/response.o

# [ Compilation rules ]
$(shell mkdir -p $(DIROBJS))

all: runServer runClient

runServer: server/runServer.cpp $(DIROBJS)/server.o $(LIBOAI_OBJS)
	$(CXX) $(CXXFLAGS) \
		server/runServer.cpp \
		$(DIROBJS)/server.o \
		$(LIBOAI_OBJS) \
		$(LDFLAGS) -o runServer

runClient: client/runClient.cpp $(DIROBJS)/client.o
	$(CXX) $(CXXFLAGS) \
		client/runClient.cpp \
		$(DIROBJS)/client.o \
		-o runClient

$(DIROBJS)/server.o: server/server.cpp
	$(CXX) $(CXXFLAGS) -c \
		server/server.cpp \
		-o $(DIROBJS)/server.o

$(DIROBJS)/client.o: client/client.cpp
	$(CXX) $(CXXFLAGS) -c \
		client/client.cpp \
		-o $(DIROBJS)/client.o




$(DIROBJS)/audio.o: src/liboai/components/audio.cpp
	$(CXX) $(CXXFLAGS) -c src/liboai/components/audio.cpp -o $(DIROBJS)/audio.o

$(DIROBJS)/azure.o: src/liboai/components/azure.cpp
	$(CXX) $(CXXFLAGS) -c src/liboai/components/azure.cpp -o $(DIROBJS)/azure.o

$(DIROBJS)/chat.o: src/liboai/components/chat.cpp
	$(CXX) $(CXXFLAGS) -c src/liboai/components/chat.cpp -o $(DIROBJS)/chat.o

$(DIROBJS)/completions.o: src/liboai/components/completions.cpp
	$(CXX) $(CXXFLAGS) -c src/liboai/components/completions.cpp -o $(DIROBJS)/completions.o

$(DIROBJS)/edits.o: src/liboai/components/edits.cpp
	$(CXX) $(CXXFLAGS) -c src/liboai/components/edits.cpp -o $(DIROBJS)/edits.o

$(DIROBJS)/embeddings.o: src/liboai/components/embeddings.cpp
	$(CXX) $(CXXFLAGS) -c src/liboai/components/embeddings.cpp -o $(DIROBJS)/embeddings.o

$(DIROBJS)/files.o: src/liboai/components/files.cpp
	$(CXX) $(CXXFLAGS) -c src/liboai/components/files.cpp -o $(DIROBJS)/files.o

$(DIROBJS)/fine_tunes.o: src/liboai/components/fine_tunes.cpp
	$(CXX) $(CXXFLAGS) -c src/liboai/components/fine_tunes.cpp -o $(DIROBJS)/fine_tunes.o

$(DIROBJS)/images.o: src/liboai/components/images.cpp
	$(CXX) $(CXXFLAGS) -c src/liboai/components/images.cpp -o $(DIROBJS)/images.o

$(DIROBJS)/models.o: src/liboai/components/models.cpp
	$(CXX) $(CXXFLAGS) -c src/liboai/components/models.cpp -o $(DIROBJS)/models.o

$(DIROBJS)/moderations.o: src/liboai/components/moderations.cpp
	$(CXX) $(CXXFLAGS) -c src/liboai/components/moderations.cpp -o $(DIROBJS)/moderations.o

$(DIROBJS)/authorization.o: src/liboai/core/authorization.cpp
	$(CXX) $(CXXFLAGS) -c src/liboai/core/authorization.cpp -o $(DIROBJS)/authorization.o

$(DIROBJS)/netimpl.o: src/liboai/core/netimpl.cpp
	$(CXX) $(CXXFLAGS) -c src/liboai/core/netimpl.cpp -o $(DIROBJS)/netimpl.o

$(DIROBJS)/response.o: src/liboai/core/response.cpp
	$(CXX) $(CXXFLAGS) -c src/liboai/core/response.cpp -o $(DIROBJS)/response.o



clean:
	rm -f runServer
	if [ -d $(DIROBJS) ]; then rm -r $(DIROBJS); fi