#include "trace_route.h"
#include "print_table.h"
#include "raw_socket.h"
#include "logger_net.h"


TraceRoute::TraceRoute(const std::string &input_fqdn):nickname("TraceRoute"){
    initArguments(input_fqdn);
}

TraceRoute::TraceRoute(const std::string &input_fqdn,
    const std::string &input_nickname):nickname(input_nickname){
    initArguments(input_fqdn);
}

TraceRoute::~TraceRoute(){}


Answer TraceRoute::start(){
    Answer program;
    RawSocket rawSocket;
    PrintTable table({"Hop", "IP", "DNS", "TIME"});
    Logger logger("log/traceroute.log");

    logger.log("Початок роботи програми", Logger::INFO);

    program.isError = false;

    auto startTime = Clock::now();

    const int bufferSize = 1024;
    char buffer[bufferSize];

    for (int ttl = 1; ttl <= MAX_HOPS; ++ttl){
        auto hopStartTime = Clock::now();

        if (!rawSocket.sendPacket(dest_ip, ttl)){
            logger.log("Не вдалося надіслати пакет!", Logger::ERROR);
            program.isError = true;
            break;
        }
        else{
            logger.log("Пакет успішно відправлено", Logger::INFO);
        }

        std::string senderIP;
        int icmpType;

        if (rawSocket.receivePacket(buffer, bufferSize, senderIP, icmpType)){
            logger.log("Пакет успішно отримано", Logger::INFO);

            auto hopEndTime = Clock::now();
            auto hopDuration = std::chrono::duration_cast
                <std::chrono::milliseconds>(hopEndTime - hopStartTime).count();

            // DNS lookup
            sockaddr_in sa {};
            sa.sin_family = AF_INET;
            inet_pton(AF_INET, senderIP.c_str(), &sa.sin_addr);
        
            char host[NI_MAXHOST];
            int dnsResult = getnameinfo((sockaddr*)&sa, sizeof(sa), host, sizeof(host), nullptr, 0, 0);
        
            std::string dnsName = (dnsResult == 0) ? std::string(host) : "None";

            table.addRow({
                std::to_string(ttl),
                senderIP,
                dnsName,
                std::to_string(hopDuration) + " ms"
            });

            if (icmpType == ICMP_ECHOREPLY) {break;}
        }
        else{
            logger.log("Не вдалося отримати пакет!", Logger::WARNING);
            table.addRow({
                std::to_string(ttl),
                senderIP,
                "***", "***"
            });

            continue;
        }
        
    }

    table.showTable();

    auto endTime = Clock::now();
    auto duration = std::chrono::duration_cast
        <std::chrono::milliseconds>(endTime - startTime).count();
    program.time = std::to_string(duration) + " ms";

    logger.log("Завершення роботи програми", Logger::INFO);

    return program;
}

void TraceRoute::initArguments(const std::string &input_data){
    if (!isValidFqdn(input_data)){
        throw std::invalid_argument("FQDN: - не існує або недоступний");
    }
    this->fqdn = input_data;

    if (!getIpFromFqdn(fqdn)){
        throw std::invalid_argument("IP: - не вдалося витягнути ip з fqdn");
    }
    std::cout << "| " << nickname << " to " << fqdn << " (" << dest_ip 
        << "), " << MAX_HOPS << " hops max" << std::endl;
}

bool TraceRoute::getIpFromFqdn(const std::string& fqdn){
    struct sockaddr_in sa;
    int result = inet_pton(AF_INET, fqdn.c_str(), &(sa.sin_addr));
    if (result != 0){
        dest_ip = fqdn;
        return true;
    }

    addrinfo hints{}, *res = nullptr;

    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;

    int status = getaddrinfo(fqdn.c_str(), nullptr, &hints, &res);
    if (status != 0 || !res) return false;

    char ipStr[INET_ADDRSTRLEN];
    sockaddr_in* ipv4 = reinterpret_cast<sockaddr_in*>(res->ai_addr);
    inet_ntop(AF_INET, &(ipv4->sin_addr), ipStr, sizeof(ipStr));
    dest_ip = ipStr;

    freeaddrinfo(res);

    return true;
}

bool TraceRoute::isValidFqdn(const std::string& fqdn){
    struct addrinfo addr = {}, *res = nullptr;
    addr.ai_family = AF_UNSPEC;
    addr.ai_socktype = SOCK_STREAM;
    
    int status = getaddrinfo(fqdn.c_str(), nullptr, &addr, &res);
    if (res) {
        freeaddrinfo(res);
    }
    return status == 0;
}
