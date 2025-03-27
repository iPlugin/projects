# ========= Local Makefile ========= #

SRC_DIR = source
SRC_FILES = \
	$(SRC_DIR)/trace_route.cpp \
	$(SRC_DIR)/raw_socket.cpp \
	$(SRC_DIR)/print_logo.cpp \
	$(SRC_DIR)/print_table.cpp \
	$(SRC_DIR)/logger_net.cpp

INC_DIR = include
INC_FILES = \
	$(INC_DIR)/ascii_art.h \
	$(INC_DIR)/trace_route.h \
	$(INC_DIR)/raw_socket.h \
	$(INC_DIR)/print_logo.h \
	$(INC_DIR)/print_table.h \
	$(INC_DIR)/logger_net.h

OBJ_DIR = object
OBJ_FILES = \
	$(OBJ_DIR)/run_project.o \
	$(OBJ_DIR)/trace_route.o \
	$(OBJ_DIR)/raw_socket.o \
	$(OBJ_DIR)/print_logo.o \
	$(OBJ_DIR)/print_table.o \
	$(OBJ_DIR)/logger_net.o

CXX = g++
CXXFLAGS = -c -I$(INC_DIR)
LOG_DIR = log

start: $(OBJ_FILES)
	$(CXX) $^ -o netrouter

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp $(INC_DIR)/%.h
	$(CXX) $(CXXFLAGS) $< -o $@

# окреме правило для головного файлу run_project.cpp
$(OBJ_DIR)/run_project.o: $(SRC_DIR)/run_project.cpp
	mkdir -p $(OBJ_DIR)
	mkdir -p $(LOG_DIR)
	$(CXX) $(CXXFLAGS) $< -o $@

clean:
	rm -r netrouter
	rm -rf $(OBJ_DIR)
	rm -rf $(LOG_DIR)

restart: clean start

help:
	@echo "Welcome to the traceroute project"
	@echo "make start 	- build the project"
	@echo "make clean 	- remove all files"
	@echo "make restart	- remove all files and build the project again"
	@echo "make help 	- show this message"