#ifndef SERVER_H
#define SERVER_H

#include <pthread.h>

#include "../includes/utils.h"
#include "../sources/searcher.h"
#include "../audio/audio.h"


class Server{
private:
    // constructor
    Logger logger;

    // startServer -> parseArgs
    string server_ip;
    int server_port;
    int proxy_port;

    // startServer -> createSocket
    int serverFD;

    // sendPacket
    struct sockaddr_in sender_addr;
    // recvPacket
    struct sockaddr_in recver_addr;
    string filename;
    bool originalityCheck(package &packet);

    // startServer
    bool parseArgs(string &msg_type, char *argv[]);
    bool createSocket();
    bool createIp();

    // startSearch
    string filepath;
    void sendResult();
    void notification();

public:

    bool stopWaiting = false;
    std::atomic<bool> stopMusic;

    Server(const string &logFilePath): logger(logFilePath){}
    ~Server(){}

    bool startServer(char *argv[]);
    bool startSearch();
    bool sendPacket(const string &message);
    bool recvPacket();
// -------------------------------------------------

};

#endif // SERVER_H           ▐███████▌
//                           ▐       ▌
//                     ▄▀▀▀█ ▐ ▀▀▄▀▀ ▌ █▀▀▀▄
//                     ▌▌▌▌▐ ▄▌ ▄▄▄ ▐▄ ▌▐▐▐▐