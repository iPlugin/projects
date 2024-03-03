CC = g++
CFLAGS = -std=c++17 -g -Wall

all: search_app

search_app: main.cpp FileSearch.o ClassTimer.o
	$(CC) $(CFLAGS) -o search_app main.cpp FileSearch.o ClassTimer.o

FileSearch.o: FileSearch.cpp headers/FileSearch.h
	$(CC) $(CFLAGS) -c FileSearch.cpp

ClassTimer.o: ClassTimer.cpp headers/ClassTimer.h
	$(CC) $(CFLAGS) -c ClassTimer.cpp

clean:
	rm -f search_app FileSearch.o ClassTimer.o
