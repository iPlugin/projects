#include "../includes/proxy.h"

/*                         ▄   ▄
----------------       ▄█▄ █▀█▀█ ▄█▄         I am            ----------------
---- Part 1 ----      ▀▀████▄█▄████▀▀       Batman           ---- Part 1 ----
----------------           ▀█▀█▀                             ----------------
*/

bool Proxy::startProxy(char* argv[]) {
    string msg_type_clt = "[ PROXY ]\t";
    string msg_type_arg = "[ PARAMS ]\t";
    string msg_type_sok = "[ SOCKET ]\t";
    string msg_type_hrl = "[ HDRINCL ]\t";

    string start_proxy = "Starting ...\n";
    printAndLogs(logger, msg_type_clt, start_proxy, 1);

    sleepTime(1);

    if (parseArgs(msg_type_arg, argv)) {
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
        close(proxyFD);
        return false;
    }

    sleepTime(1);
    return true;
}

bool Proxy::parseArgs(string &msg_type, char* argv[]) {
    proxy_ip = "127.0.0.1"; // Proxy::client_ip

    string temp_port = argv[2]; // Proxy::proxy_port
    auto [ptr1, ec1] = std::from_chars(temp_port.data(),
        temp_port.data() + temp_port.size(), proxy_port);
    if (ec1 != std::errc()) {
        string message = "Error convert proxy_port\n";
        printAndLogs(logger, msg_type, message, 2);
        // logger.log("Error convert proxy_port\n", Logger::WARNING);
        return false; 
    }

    temp_port = argv[3]; // Proxy::server_port
    auto [ptr2, ec2] = std::from_chars(temp_port.data(),
        temp_port.data() + temp_port.size(), server_port);
    if (ec2 != std::errc()) {
        string message = "Error convert server_port\n";
        printAndLogs(logger, msg_type, message, 2);
        // logger.log("Error convert server_port\n", Logger::WARNING);
        return false;
    }

    temp_port = argv[4]; // Proxy::client_port
    auto [ptr3, ec3] = std::from_chars(temp_port.data(),
        temp_port.data() + temp_port.size(), client_port);
    if (ec3 != std::errc()) {
        string message = "Error convert client_port\n";
        printAndLogs(logger, msg_type, message, 2);
        // logger.log("Error convert client_port\n", Logger::WARNING);
        return false;
    }
    return true;
}

bool Proxy::createSocket() {
    proxyFD = getSocket();
    return proxyFD;
}

bool Proxy::createIp() {
    if (settingIp(proxyFD))
        return true;
    return false;
}

/*                         ▄█▄▄▄█▄
----------------    ▄▀    ▄▌─▄─▄─▐▄    ▀▄   Devil will break ----------------
---- Part 2 ----    █▄▄█  ▀▌─▀─▀─▐▀  █▄▄█       his head     ---- Part 2 ----
----------------     ▐▌    ▀▀███▀▀    ▐▌                     ----------------
                    ████ ▄█████████▄ ████
*/

bool Proxy::sendPacket(package &recv_packet) {
    string msg_type_snd = "[ SEND ]\t";

    package packet; // IP + TCP + DATA
    
    packet.data = recv_packet.data;

    packet.iph.ihl = 5; 
    packet.iph.version = 4; 
    packet.iph.tos = 0; 
    packet.iph.tot_len = htons(sizeof(struct iphdr) + sizeof(struct tcphdr) + recv_packet.data.size()); 
    packet.iph.id = htons(rand() % 65535); 
    packet.iph.frag_off = 0;
    packet.iph.ttl = 64;
    packet.iph.protocol = IPPROTO_TCP; 
    packet.iph.check = recv_packet.iph.check;
    packet.iph.saddr = inet_addr("127.0.0.1"); // inet_addr(proxy_ip.c_str());
    packet.iph.daddr = inet_addr("127.0.0.1"); // inet_addr(proxy_ip.c_str());

    packet.tcph.th_sport = htons(proxy_port);
    packet.tcph.th_dport = recv_packet.tcph.th_sport == htons(server_port) ? htons(client_port) : htons(server_port);
    packet.tcph.seq = 0;
    packet.tcph.ack = 0;
    packet.tcph.th_off = 5;
    packet.tcph.res1 = 0;
    packet.tcph.th_flags = TH_SYN;
    packet.tcph.th_win = htons(5840);
    packet.tcph.check = ntohs(recv_packet.tcph.check);
    packet.tcph.urg_ptr = 0;

    // packet.tcph.check = tcp_checksum(&packet);
    // packet.iph.check = ip_checksum(&packet.iph, sizeof(packet.iph));

    // Proxy::sender_addr
    sender_addr.sin_family = AF_INET;
    sender_addr.sin_addr.s_addr = packet.iph.daddr;
    sender_addr.sin_port = packet.tcph.th_dport;

    // Send the packet
    char buffer[2048];
    serialize_package(packet, buffer, sizeof(buffer));
    if (sendto(proxyFD, buffer, ntohs(packet.iph.tot_len), 0, (sockaddr*)&sender_addr, sizeof(sender_addr)) > 0) {
        string msg = "Packet: " + packet.data + "\n";
        packet.data = recv_packet.data + "\n";
        printAndLogs(logger, msg_type_snd, msg, 1);
        printPacketToSend(packet);
    }
    else {
        string msg = "Send failed\n\n";
        packet.data = recv_packet.data + "\n";
        printAndLogs(logger, msg_type_snd, msg, 3);
    }

    return true;
}

bool Proxy::recvPacket() {
    string msg_type_rcv = "[ RECV ]\t";
    string msg_type_dat = "[ DATA ]\t";

    while (true) {
        char buffer[2048];
        socklen_t recver_addr_len = sizeof(sockaddr_in);
        ssize_t packet_size = recvfrom(proxyFD, buffer, sizeof(buffer), 0, (struct sockaddr*)&recver_addr, &recver_addr_len);

        // Upload packet
        package packet;
        deserialize_package(buffer, packet_size, packet);

        if (packet.iph.daddr == inet_addr(proxy_ip.c_str()) && packet.tcph.th_dport == htons(proxy_port) && !packet.data.empty()) {
            string message = "Packet: " + packet.data + "\n";
            printAndLogs(logger, msg_type_rcv, message, 1);
            printPacketToRecv(packet);
                        
            // if (packet.tcph.th_sport == htons(client_port)) {
                // string option;
                // do {
                //     cout << "Change message? [1] yes / [2] no: ";
                //     cin >> option;
                // } while (option != "1" && option != "2");

                // if (option == "1") {
                    // string message = "Changes made to the message\n";
                    // printAndLogs(logger, msg_type_dat, message, 2);
                    // packet.data += "cpp";
                // } cout << endl;
            // }
            sendPacket(packet);
        }
    }
    return true;
}

void Proxy::printPacketToSend(const package &packet) {
    cout << "\tPackage ID: " << packet.iph.id << "\n";
    cout << "\tSource IP: " << inet_ntoa(*(in_addr*)&packet.iph.saddr) << "\n";
    cout << "\tDestination IP: " << inet_ntoa(*(in_addr*)&packet.iph.daddr) << "\n";
    cout << "\tSource Port: " << ntohs(packet.tcph.th_sport) << "\n";
    cout << "\tDestination Port: " << ntohs(packet.tcph.th_dport) << "\n";
    cout << "\tChecksum IP: " << ntohs(packet.iph.check) << "\n";
    cout << "\tChecksum TCP: " << ntohs(packet.tcph.check) << "\n";
    cout << "\tData: " << packet.data << "\n\n";
}

void Proxy::printPacketToRecv(const package &packet) {
    cout << "\tPackage ID: " << packet.iph.id << "\n";
    cout << "\tSource IP: " << inet_ntoa(*(in_addr*)&packet.iph.saddr) << "\n";
    cout << "\tDestination IP: " << inet_ntoa(*(in_addr*)&packet.iph.daddr) << "\n";
    cout << "\tSource Port: " << ntohs(packet.tcph.th_sport) << "\n";
    cout << "\tDestination Port: " << ntohs(packet.tcph.th_dport) << "\n";
    cout << "\tChecksum IP: " << packet.iph.check << "\n";
    cout << "\tChecksum TCP: " << ntohs(packet.tcph.check) << "\n";
    cout << "\tData: " << packet.data << "\n\n";
}