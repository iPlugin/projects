#ifndef RAW_SOCKET_H
#define RAW_SOCKET_H

#include <string>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <iostream>
#include <cstring>
#include <sys/socket.h>

class RawSocket{
private:
    int sockfd;
    bool setTTL(int ttl);
    unsigned short checkSum(const void* data, int length);

public:
    RawSocket();
    ~RawSocket();

    bool sendPacket(const std::string& destinationIP, int ttl);
    bool receivePacket(char* buffer, int bufferSize, std::string& senderIP, int& icmpType, int timeoutMs = 1000);

};

#endif // RAW_SOCKET_H
