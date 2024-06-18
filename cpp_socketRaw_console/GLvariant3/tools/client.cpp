#include "../includes/client.h"

/*                         ▄   ▄
----------------       ▄█▄ █▀█▀█ ▄█▄         I am            ----------------
---- Part 1 ----      ▀▀████▄█▄████▀▀       Batman           ---- Part 1 ----
----------------           ▀█▀█▀                             ----------------
*/

bool Client::startClient(char* argv[]) {
    string msg_type_clt = "[ CLIENT ]\t";
    string msg_type_arg = "[ PARAMS ]\t";
    string msg_type_sok = "[ SOCKET ]\t";
    string msg_type_hrl = "[ HDRINCL ]\t";

    string start_client = "Starting ...\n";
    printAndLogs(logger, msg_type_clt, start_client, 1);

    sleepTime(1);

    if (parseArgs(msg_type_arg, argv)){
        string message = "Client received arguments\n";
        printAndLogs(logger, msg_type_arg, message, 1);
    }
    else {
        string message = "Client received no arguments\n\n";
        printAndLogs(logger, msg_type_arg, message, 3);
        return false;
    }

    sleepTime(1);

    if (createSocket()) {
        string message = "Socket was created\n";
        printAndLogs(logger, msg_type_sok, message, 1);
    }
    else {
        string message = "Socket was not created\n\n";
        printAndLogs(logger, msg_type_sok, message, 3);
        return false;
    }

    sleepTime(1);

    if (createIp()) {
        string message = "Setting IP_HDRINCL successfully\n";
        printAndLogs(logger, msg_type_hrl, message, 1);
    }
    else {
        string message = "Error setting IP_HDRINCL\n\n";
        printAndLogs(logger, msg_type_hrl, message, 3);
        close(clientFD);
        return false;
    }

    sleepTime(1);
    return true;
}

bool Client::parseArgs(string &msg_type, char* argv[]) {
    client_ip = "127.0.0.1"; // Client::client_ip

    string temp_port = argv[1]; // Client::client_port
    auto [ptr1, ec1] = std::from_chars(temp_port.data(),
        temp_port.data() + temp_port.size(), client_port);
    if (ec1 != std::errc()) {
        string message = "Error convert client_port\n";
        printAndLogs(logger, msg_type, message, 2);
        // logger.log("Error convert client_port\n", Logger::WARNING);
        return false; 
    }

    temp_port = argv[2]; // Client::proxy_port
    auto [ptr2, ec2] = std::from_chars(temp_port.data(),
        temp_port.data() + temp_port.size(), proxy_port);
    if (ec2 != std::errc()) {
        string message = "Error convert proxy_port\n";
        printAndLogs(logger, msg_type, message, 2);
        // logger.log("Error convert proxy_port\n", Logger::WARNING);
        return false;
    }

    filename = argv[3]; // Client::filename
    return true;
}

bool Client::createSocket() {
    clientFD = getSocket();
    return clientFD;
}

bool Client::createIp() {
    if (settingIp(clientFD))
        return true;
    return false;
}

/*                         ▄█▄▄▄█▄
----------------    ▄▀    ▄▌─▄─▄─▐▄    ▀▄   Devil will break ----------------
---- Part 2 ----    █▄▄█  ▀▌─▀─▀─▐▀  █▄▄█       his head     ---- Part 2 ----
----------------     ▐▌    ▀▀███▀▀    ▐▌                     ----------------
                    ████ ▄█████████▄ ████
*/

bool Client::sendPacket() {
    string msg_type_snd = "[ SEND ]\t";

    package packet; // IP + TCP + DATA
    
    // Data
    packet.data = filename;

    // IP і TCP заголовки
    packet.iph.ihl = 5; 
    packet.iph.version = 4; 
    packet.iph.tos = 0; 
    packet.iph.tot_len = htons(sizeof(struct iphdr) + sizeof(struct tcphdr) + packet.data.size()); 
    packet.iph.id = htons(rand() % 65535); 
    packet.iph.frag_off = 0; 
    packet.iph.ttl = 64;
    packet.iph.protocol = IPPROTO_TCP; 
    packet.iph.check = 0; // ---------------------------------------------+
    packet.iph.saddr = inet_addr(client_ip.c_str());                   // |
    packet.iph.daddr = inet_addr(client_ip.c_str());                   // |
                                                                       // |
    packet.tcph.th_sport = htons(client_port);                         // |
    packet.tcph.th_dport = htons(proxy_port);                          // |
    packet.tcph.seq = 0;                                               // |
    packet.tcph.ack = 0;                                               // |
    packet.tcph.th_off = 5;                                            // |
    packet.tcph.res1 = 0;                                              // |
    packet.tcph.th_flags = TH_SYN;                                     // |
    packet.tcph.th_win = htons(5840);                                  // |
    packet.tcph.check = 0; // ----------------------------+               |
    packet.tcph.urg_ptr = 0; // if th_flags = TH_URG   // |               |
                                                       // |               |
    packet.tcph.check = ntohs(tcp_checksum(&packet)); // <+               |
    packet.iph.check = (ip_checksum(&packet.iph, sizeof(packet.iph))); //<+

    // Client::sender_addr
    sender_addr.sin_family = AF_INET;
    sender_addr.sin_addr.s_addr = packet.iph.daddr;
    sender_addr.sin_port = packet.tcph.th_dport;

    // Send the packet
    char buffer[2048];
    serialize_package(packet, buffer, sizeof(buffer));
    if (sendto(clientFD, buffer, ntohs(packet.iph.tot_len), 0, (sockaddr*)&sender_addr, sizeof(sender_addr)) > 0) {
        string message = "Packet: " + packet.data + "\n";
        packet.data = filename + "\n";
        printAndLogs(logger, msg_type_snd, message, 1);
    }
    else {
        string message = "Send failed\n\n";
        packet.data = filename + "\n";
        printAndLogs(logger, msg_type_snd, message, 3);
    }

    return true;
}

bool Client::recvPacket() {
    string msg_type_rcv = "[ RECV ]\t";
    
    while (true) {
        char buffer[4096];
        socklen_t recver_addr_len = sizeof(sockaddr_in);
        ssize_t packet_size = recvfrom(clientFD, buffer, sizeof(buffer), 0, (struct sockaddr*)&recver_addr, &recver_addr_len);

        // Upload packet
        package packet;
        deserialize_package(buffer, packet_size, packet);

        if (packet.iph.daddr == inet_addr(client_ip.c_str()) && packet.tcph.th_dport == htons(client_port) && !packet.data.empty()) {
            string message = "Packet: " + packet.data + "\n";
            printAndLogs(logger, msg_type_rcv, message, 1);
        }
    }
    return true;
}