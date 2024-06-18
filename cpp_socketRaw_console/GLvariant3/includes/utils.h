#ifndef UTILS_H
#define UTILS_H

#include <arpa/inet.h> // inet_addr()
#include <charconv> // from_chars()
#include <unistd.h> // close()

#include "../includes/colors.h"
    // nothing
#include "../includes/logger.h"
    // #include <iostream>
    // #include <fstream>
    // #include <string>
    // #include <ctime>
#include "../package/package.h"
    // #include <netinet/ip.h>
    // #include <netinet/tcp.h>
    // #include <cstring>
#include "../linux/settingsOS.h"
    // #include <sys/socket.h>
    // #include <netinet/in.h>

using namespace std;

// part 1
bool check_args(int argc, char *argv[], char *envp[], int count);
void printAndLogs(Logger &logger, string &msg_type, string &message, int status);
void sleepTime(int sec);
int getSocket();

// part 2
unsigned short ip_checksum(void *vdata, int length);
unsigned short tcp_checksum(package *p);


#endif  // UTILS_H