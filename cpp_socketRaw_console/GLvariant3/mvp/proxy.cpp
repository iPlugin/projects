#include <iostream> // utils
#include <cstring> // utils
#include <unistd.h> // utils
#include <ctime> // utils
#include "utils.h"

struct pseudo_header {
    unsigned int src_addr;
    unsigned int dst_addr;
    unsigned char zero;
    unsigned char protocol;
    unsigned short length;
};

// Функція для розрахунку контрольної суми
unsigned short ip_checksum(void* buffer, int length) {
    unsigned short* buf = static_cast<unsigned short*>(buffer);
    unsigned int sum = 0;
    for (sum = 0; length > 1; length -= 2) {
        sum += *buf++;
    }
    if (length == 1) {
        sum += *reinterpret_cast<unsigned char*>(buf);
    }
    sum = (sum >> 16) + (sum & 0xffff);
    sum += (sum >> 16);
    return static_cast<unsigned short>(~sum);
}

unsigned short tcp_checksum(package* packet) {
    // Створення псевдо заголовка
    pseudo_header psh;
    psh.src_addr = packet->iph.saddr;
    psh.dst_addr = packet->iph.daddr;
    psh.zero = 0;
    psh.protocol = IPPROTO_TCP;
    psh.length = htons(sizeof(tcphdr) + packet->data.size());

    // Обчислення розміру псевдо-заголовка + заголовка TCP + даних
    int psize = sizeof(pseudo_header) + sizeof(tcphdr) + packet->data.size();

    char* pseudogram = new char[psize];
    memcpy(pseudogram, &psh, sizeof(pseudo_header));
    memcpy(pseudogram + sizeof(pseudo_header), &packet->tcph, sizeof(tcphdr));
    memcpy(pseudogram + sizeof(pseudo_header) + sizeof(tcphdr), packet->data.c_str(), packet->data.size());

    unsigned short checksum = ip_checksum(pseudogram, psize);

    delete[] pseudogram;

    return checksum;
}


void print_packet(const package &packet) {
    std::cout << "Sending packet:" << std::endl;
    std::cout << "Package ID: " << packet.iph.id << std::endl;
    std::cout << "Source IP: " << inet_ntoa(*(in_addr*)&packet.iph.saddr) << std::endl;
    std::cout << "Destination IP: " << inet_ntoa(*(in_addr*)&packet.iph.daddr) << std::endl;
    std::cout << "Source Port: " << ntohs(packet.tcph.th_sport) << std::endl;
    std::cout << "Destination Port: " << ntohs(packet.tcph.th_dport) << std::endl;
    std::cout << "Data: " << packet.data << std::endl;
}

bool send_packet(int socketFD, int sender, int receiver, std::string message){
    package packet; // IP + TCP + DATA
    
    packet.data = message;

    packet.iph.ihl = 5; 
    packet.iph.version = 4; 
    packet.iph.tos = 0; 
    packet.iph.tot_len = htons(sizeof(struct iphdr) + sizeof(struct tcphdr) + packet.data.size()); 
    packet.iph.id = htons(rand() % 65535);; 
    packet.iph.frag_off = 0; 
    packet.iph.ttl = 64;
    packet.iph.protocol = IPPROTO_TCP; 
    packet.iph.check = 0; // ---------------------------------------------+
    packet.iph.saddr = inet_addr("127.0.0.1");                         // |
    packet.iph.daddr = inet_addr("127.0.0.1");                         // |
                                                                       // |
    packet.tcph.th_sport = htons(sender);                              // |
    packet.tcph.th_dport = htons(receiver);                            // |
    packet.tcph.seq = 0;                                               // |
    packet.tcph.ack = 0;                                               // |
    packet.tcph.th_off = 5;                                            // |
    packet.tcph.res1 = 0;                                              // |
    packet.tcph.th_flags = TH_SYN;                                     // |
    packet.tcph.th_win = htons(5840);                                  // |
    packet.tcph.check = 0; // ----------------------------+               |
    packet.tcph.urg_ptr = 0; // if th_flags = TH_URG   // |               |
                                                       // |               |
    packet.tcph.check = tcp_checksum(&packet); // <-------+               |
    packet.iph.check = ip_checksum(&packet.iph, sizeof(packet.iph)); // <-+

    // Print the packet before sending
    std::cout << "\nSEND" << std::endl;
    print_packet(packet);

    // Destination address setup
    sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_port = packet.tcph.th_dport;
    address.sin_addr.s_addr = packet.iph.daddr;


    // Set option to include IP headers
    int one = 1;
    const int *val = &one;
    if (setsockopt(socketFD, IPPROTO_IP, IP_HDRINCL, val, sizeof(one)) < 0) {
        std::cerr << "Error setting IP_HDRINCL" << std::endl;
        close(socketFD);
        return 1;
    }

    // Send the packet
    char buffer[2048];
    serialize_package(packet, buffer, sizeof(buffer));
    if (sendto(socketFD, buffer, ntohs(packet.iph.tot_len), 0, (sockaddr*)&address, sizeof(address)) < 0) {
        std::cerr << "Sendto failed" << std::endl;
    } else {
        std::cout << "Packet sent successfully" << std::endl;
    }

    return true;
}

bool recv_packet(int socketFD){
    // std::unordered_set<unsigned short> processed_ids;
    while (true) {
        char buffer[2048]; // Буфер для "сырих" даних
        // memset(buffer, 0, sizeof(buffer));
        socklen_t addr_len = sizeof(sockaddr_in);
        sockaddr_in client_addr;

        // Приймаємо дані
        ssize_t packet_size = recvfrom(socketFD, buffer, sizeof(buffer), 0, (struct sockaddr*)&client_addr, &addr_len);
        if (packet_size < 0) {
            std::cerr << "Recvfrom error" << std::endl;
            continue;
        }

        if (packet_size < sizeof(iphdr) + sizeof(tcphdr)) {
            std::cerr << "Incomplete packet received" << std::endl;
            continue;
        }

        // Розпаковуємо дані у структуру package за допомогою функції deserialize_package
        package packet;
        deserialize_package(buffer, packet_size, packet);

        // // Перевіряємо чи пакет уже оброблений
        // if (processed_ids.find(packet.iph.id) != processed_ids.end()) {
        //     continue; // Пропускаємо оброблені пакети
        // }

        // // Додаємо ID пакету до оброблених
        // processed_ids.insert(packet.iph.id);

        if (packet.iph.daddr == inet_addr("127.0.0.1") && packet.tcph.th_dport == htons(2001) && packet.data != "") {
            // Виводимо прийнятий пакет
            std::cout << "\nRECV" << std::endl;
            print_packet(packet);

            if (packet.tcph.th_sport == htons(2000)) {
                send_packet(socketFD, 2001, 2002, packet.data);
            }
            else if (packet.tcph.th_sport == htons(2002)){
                send_packet(socketFD, 2001, 2000, packet.data);
            }
            
            // break;
        }
    }
    return true;
}

int main() {
    srand(time(NULL));
    int socketFD = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
    if (socketFD < 0) {
        std::cerr << "Socket creation error" << std::endl;
        return 1;
    }

    // if (!send_packet(socketFD))
    //     return 1;
    
    // if (!send_packet(socketFD))
    //     return 1;
    
    if (!recv_packet(socketFD))
        return 1;

    // if (!recv_packet(socketFD))
    //     return 1;
    

    // Close the socket
    close(socketFD);

    return 0;
}









// РЕАЛІЗУВАТИ CIN ДЛЯ PROXY 1 OR 2 ЗРУЙНУВАТИ ЧИ НІ
// А ДЛЯ СЕРВЕРУ І КЛІЄНТА ПЕРЕВІРКУ cheaksum

// ПРИЄДНАТИ до проєкту №1 
// Орматувати фунцію і налаштувати ООП