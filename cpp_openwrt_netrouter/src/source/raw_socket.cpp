#include "raw_socket.h"

RawSocket::RawSocket():sockfd(-1){
    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if (sockfd < 0) {
        throw std::runtime_error("Не вдалося створити сирий сокет! З sudo запускай!");
    }
}

RawSocket::~RawSocket(){
    if (sockfd != -1){
        close(sockfd);
    }
}

bool RawSocket::setTTL(int ttl) {
    if (setsockopt(sockfd, IPPROTO_IP, IP_TTL, &ttl, sizeof(ttl)) < 0){
        perror("setsockopt TTL");
        return false;
    }
    return true;
}

bool RawSocket::sendPacket(const std::string& destinationIP, int ttl){
    if (!setTTL(ttl)) {
        return false;
    }

    sockaddr_in destAddr {};
    destAddr.sin_family = AF_INET;
    inet_pton(AF_INET, destinationIP.c_str(), &(destAddr.sin_addr));

    char packet[64] = {0};
    struct icmphdr* icmp = (struct icmphdr*) packet;

    icmp->type = ICMP_ECHO;
    icmp->code = 0;
    icmp->un.echo.id = htons(1234);
    icmp->un.echo.sequence = htons(ttl);
    icmp->checksum = 0;


    int packetSize = sizeof(struct icmphdr);
    unsigned short* ptr = (unsigned short*)icmp;
    unsigned int checksum = 0;
    for (int i = 0; i < packetSize / 2; i++) {
        checksum += ptr[i];
    }
    checksum = (checksum >> 16) + (checksum & 0xffff);
    checksum += (checksum >> 16);
    icmp->checksum = checkSum(packet, packetSize);

    ssize_t sent = sendto(sockfd, packet, packetSize, 0, (sockaddr*)&destAddr, sizeof(destAddr));
    if (sent < 0) {
        perror("sendto");
        return false;
    }

    return true;
}

bool RawSocket::receivePacket(char* buffer, int bufferSize, std::string& senderIP, int& icmpType, int timeoutMs) {
    sockaddr_in senderAddr {};
    socklen_t senderLen = sizeof(senderAddr);

    ssize_t bytesReceived = recvfrom(sockfd, buffer, bufferSize, 0, (sockaddr*)&senderAddr, &senderLen);
    if (bytesReceived < 0) {
        perror("recvfrom");
        return false;
    }

    char ipStr[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &(senderAddr.sin_addr), ipStr, sizeof(ipStr));
    senderIP = ipStr;

    struct iphdr* ipHeader = (struct iphdr*) buffer;
    int ipHeaderLen = ipHeader->ihl * 4;
    struct icmphdr* icmpHeader = (struct icmphdr*)(buffer + ipHeaderLen);

    icmpType = icmpHeader->type;

    return true;
}

unsigned short RawSocket::checkSum(const void* data, int length){
    const unsigned short* ptr = static_cast<const unsigned short*>(data);
    unsigned int sum = 0;

    while (length > 1) {
        sum += *ptr++;
        length -= 2;
    }

    if (length == 1) {
        sum += *(const unsigned char*)ptr;
    }

    sum = (sum >> 16) + (sum & 0xFFFF);
    sum += (sum >> 16);

    return static_cast<unsigned short>(~sum);
}