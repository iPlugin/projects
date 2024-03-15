# ============= Makefile ============= #

all: project

project: main.o class_table.o PGconnector.o
	g++ obj/main.o obj/class_table.o obj/PGconnector.o -o project -lpqxx -lpq

main.o: main.cpp
	mkdir obj
	g++ -c main.cpp -o obj/main.o

class_table.o: src/class_table.cpp # headers/class_table.h
	g++ -c src/class_table.cpp -o obj/class_table.o

PGconnector.o: src/PGconnector.cpp # headers/PGconnector.h
	g++ -c src/PGconnector.cpp -o obj/PGconnector.o

clear:
	rm -f project
	rm -f obj/main.o obj/class_table.o obj/PGconnector.o
	rmdir obj
