#include "package.h"

using namespace std;

void serialize_package(const package& pkt, char* buffer, size_t buffer_size) {
    // Перевірка розміру буфера
    if (buffer_size < sizeof(iphdr) + sizeof(tcphdr) + pkt.data.size()) {
        // std::cerr << "Buffer is too small for serialization" << std::endl;
        return;
    }

    // Копіювання IP заголовка в буфер
    memcpy(buffer, &pkt.iph, sizeof(iphdr));
    buffer += sizeof(iphdr);

    // Копіювання TCP заголовка в буфер
    memcpy(buffer, &pkt.tcph, sizeof(tcphdr));
    buffer += sizeof(tcphdr);

    // Копіювання даних в буфер
    memcpy(buffer, pkt.data.c_str(), pkt.data.size());
}

// Функція для десеріалізації структури package з буфера
void deserialize_package(const char* buffer, size_t buffer_size, package& pkt) {
    // Перевірка розміру буфера
    if (buffer_size < sizeof(iphdr) + sizeof(tcphdr)) {
        // std::cerr << "Buffer is too small for deserialization" << std::endl;
        return;
    }

    // Копіювання IP заголовка з буфера в структуру package
    memcpy(&pkt.iph, buffer, sizeof(iphdr));
    buffer += sizeof(iphdr);

    // Копіювання TCP заголовка з буфера в структуру package
    memcpy(&pkt.tcph, buffer, sizeof(tcphdr));
    buffer += sizeof(tcphdr);

    // Десеріалізація даних з буфера в структуру package
    pkt.data.assign(buffer, buffer_size - sizeof(iphdr) - sizeof(tcphdr));
}
