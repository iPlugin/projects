// utils.h
#ifndef UTILS_H
#define UTILS_H

#include "package.h"
#include <unistd.h>
#include <arpa/inet.h>
#include <iostream>

// Функція для прийому пакету
bool recv_packet(int socketFD, package& packet) {
    char buffer[4096];
    socklen_t addr_len = sizeof(sockaddr_in);
    sockaddr_in client_addr;

    // Приймаємо дані
    ssize_t packet_size = recvfrom(socketFD, buffer, sizeof(buffer), 0, (struct sockaddr*)&client_addr, &addr_len);
    if (packet_size < 0) {
        std::cerr << "Recvfrom error" << std::endl;
        return false;
    }
    
    if (packet_size < sizeof(iphdr) + sizeof(tcphdr)) {
        std::cerr << "Incomplete packet received" << std::endl;
        return false;
    }

    // Десеріалізуємо дані у структуру package
    deserialize_package(buffer, packet_size, packet);
    return true;
}

// Функція для відправки пакету
bool send_packet(int socketFD, const package& packet, const sockaddr_in& dest_addr) {
    char buffer[4096];
    size_t packet_size = sizeof(iphdr) + sizeof(tcphdr) + packet.data.size();

    // Перевірка розміру буфера
    if (packet_size > sizeof(buffer)) {
        std::cerr << "Buffer is too small for serialization" << std::endl;
        return false;
    }

    // Сереалізуємо структуру package в буфер
    serialize_package(packet, buffer, sizeof(buffer));

    // Відправляємо дані
    ssize_t sent_size = sendto(socketFD, buffer, packet_size, 0, (struct sockaddr*)&dest_addr, sizeof(dest_addr));
    if (sent_size < 0) {
        std::cerr << "Sendto error" << std::endl;
        return false;
    }

    return true;
}

#endif // UTILS_H
