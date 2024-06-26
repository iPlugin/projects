#ifndef SERVER_H
#define SERVER_H

#include <sys/socket.h>
#include <iostream>
#include <unistd.h>
#include <arpa/inet.h>
#include <cstring>
#include <sstream> // для нарізання по слову

#include "../include/liboai/liboai.h"
#include "../include/process/ProcessManager.h"

class Server
{
private:
    int server_fd;
    std::string server_ip = "127.0.0.1";
    int server_port = 2001;
    std::string OPENAI_API_KEY = "OPENAI_API_KEY";
    struct sockaddr_in server_addr;


    int client_fd;
    struct sockaddr_in client_addr;
    socklen_t client_addr_len;

    bool bindServer();
    bool listenServer();
    bool acceptServer();

    std::string chatgpt(std::string message);

public:
    Server();
    ~Server();
    
    bool run();
};

#endif // SERVER_H