#include "../includes/utils.h"


bool check_args(int argc, char* argv[], char *envp[], int count) {
    if (argc != count) {
        const char *user_prefix = "USER=";
        const char *user_value = nullptr;

        // Search username
        for (int i = 0; envp[i] != nullptr; ++i){
            if (strncmp(envp[i], user_prefix, strlen(user_prefix)) == 0) {
                user_value = envp[i] + strlen(user_prefix);
                break;
            }
        }

        std::string short_name(program_invocation_name);
        std::string correct_form;
        switch (count) {
        case 3: // for server
            correct_form = "Correct is: " + short_name + " <portServer> <portProxy>\n";
            break;
        case 4: // for client
            correct_form = "Correct is: " + short_name + " <portClient> <portProxy> <FileName>\n";
            break;
        case 5:
            correct_form = "Correct is: " + short_name + " proxy <portProxy> <portServer> <portClient>\n";
            break;
        default:
            break;
        }

        // Print error
        if (user_value != nullptr) {
            std::cerr << "Dear " << BOLDGREEN << user_value << RESET
                << ", you can not do this!\n" << correct_form;
        }
        else {
            std::cerr << "Dear user, you can not do this!\n" << correct_form;
        }
        return false;
    }
    return true;
}

void printAndLogs(Logger &logger, string &msg_type, string &message, int status) {
    switch (status) {
    case 1:
        cerr << BOLDGREEN << msg_type << RESET << message;
        logger.log(msg_type + message, Logger::INFO);
        break;
    case 2:
        cerr << BOLDYELLOW << msg_type << RESET << message;
        logger.log(msg_type + message, Logger::WARNING);
        break;
    case 3:
        cerr << BOLDRED << msg_type << RESET << message;
        logger.log(msg_type + message, Logger::ERROR);
        break;
    }
}

void sleepTime(int sec) {
    sleep(sec);
}

int getSocket(){
    return socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
}

// ----------------------------------------------------
void printPacket(const package &packet) {
    std::cout << "Sending packet:" << std::endl;
    std::cout << "Package ID: " << packet.iph.id << std::endl;
    std::cout << "Source IP: " << inet_ntoa(*(in_addr*)&packet.iph.saddr) << std::endl;
    std::cout << "Destination IP: " << inet_ntoa(*(in_addr*)&packet.iph.daddr) << std::endl;
    std::cout << "Source Port: " << ntohs(packet.tcph.th_sport) << std::endl;
    std::cout << "Destination Port: " << ntohs(packet.tcph.th_dport) << std::endl;
    std::cout << "Data: " << packet.data << std::endl;
}


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
