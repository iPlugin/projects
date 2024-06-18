#ifndef CLIENT_H
#define CLIENT_H

#include "../includes/utils.h"
#define debug

class Client{
private:
    int clientFD;
    Logger logger;
    struct sockaddr_in address;
public:

    Client(const string& logFilePath): logger(logFilePath){}
    ~Client(){}

    // Check count argc and int port
    bool validateArgs(int argc, char* argv[]);

    // [ SOCKET ] create client socket
    bool clientSocket();

    // [ CONNECT ] create connect
    bool connectToServer(const string& ip, int port);

    // [ SEND ]
    bool sendMessage(Message &pkg);

    // [ RECV ]
    string recvMessage();
};

#endif