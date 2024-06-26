#ifndef CLIENT_H
#define CLIENT_H

#include <sys/socket.h>
#include <iostream>
#include <unistd.h>
#include <arpa/inet.h>
#include <cstring>

class Client
{
private:
    int client_fd;

    std::string server_ip = "127.0.0.1";
    int server_port = 2001;
    struct sockaddr_in server_addr;

    bool connectServer();

public:
    Client();
    ~Client();

    bool run();
};

#endif // CLIENT_H