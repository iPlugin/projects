#ifndef SERVER_H
#define SERVER_H

#include "../includes/utils.h"
#include "../includes/searcher.h"

class Server{
private:
    int serverFD;
    int clientFD;
    Logger logger;
    struct sockaddr_in address;
public:
    bool stopWaiting = false;

    Server(const string& logFilePath): logger(logFilePath){}
    ~Server(){}
    
    void runServer();

    // Check count argc and int port
    bool parseArgs(int argc, char* argv[]);

    // [ SOCKET ] create server socket
    bool serverSocket();

    // [ BIND ]
    bool connectToServer(int port);

    // [ LISTEN ]
    bool listenServer();

    // [ ACCEPT ]
    struct sockaddr_in *clientAddress;
    int clientAddressSize = sizeof(clientAddress);
    bool acceptServer();

    // [ SEND ]
    bool sendMessage(Message &pkg);

    // [ RECV ]
    string recvMessage();

    void notification(Server &server);

    void sendResult(Server &server, string &responce);
};

#endif