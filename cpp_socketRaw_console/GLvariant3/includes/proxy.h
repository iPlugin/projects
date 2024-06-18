#ifndef PROXY_H
#define PROXY_H

#include "../includes/utils.h"


class Proxy{
private:
    // constructor
    Logger logger;

    // startProxy -> parseArgs
    string proxy_ip;
    int proxy_port;
    int server_port;
    int client_port;

    // startClient -> createSocket
    int proxyFD;

    // sendPacket
    struct sockaddr_in sender_addr;
    // recvPacket
    struct sockaddr_in recver_addr;

    // startProxy
    bool parseArgs(string &msg_type, char *argv[]);
    bool createSocket();
    bool createIp();


    bool sendPacket(package &recv_packet);
    void printPacketToSend(const package &packet);
    void printPacketToRecv(const package &packet);

public:
    Proxy(const string &logFilePath): logger(logFilePath){}
    ~Proxy(){}

    bool startProxy(char *argv[]);
    bool recvPacket();

};

#endif // PROXY_H            ▐███████▌
//                           ▐░░░░░░░▌
//                     ▄▀▀▀█ ▐░▀▀▄▀▀░▌ █▀▀▀▄
//                     ▌▌▌▌▐ ▄▌░▄▄▄░▐▄ ▌▐▐▐▐