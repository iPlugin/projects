#ifndef PACKAGE_H
#define PACKAGE_H

#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <string>
#include <cstring>

// packet = IP + TCP + DATA
struct package {
    iphdr iph;           // IP заголовок
    tcphdr tcph;         // TCP заголовок
    std::string data;    // Дані для передачі
};

// Оголошення функцій для серіалізації та десеріалізації структури package
void serialize_package(const package& pkt, char* buffer, size_t buffer_size);
void deserialize_package(const char* buffer, size_t buffer_size, package& pkt);


#endif // PACKAGE_H
