#ifndef TRACEROUTE_H
#define TRACEROUTE_H

#include <string>
#include <netdb.h>
#include <stdexcept> // for invalid_argument
#include <arpa/inet.h>
#include <chrono>

#define MAX_HOPS 30
using Clock = std::chrono::high_resolution_clock;

struct Answer{
    bool isError;
    std::string time;
};


class TraceRoute{
private:
    std::string fqdn;
    std::string nickname;
    std::string dest_ip;

    void initArguments(const std::string &input_data);
    bool isValidFqdn(const std::string& fqdn);
    bool getIpFromFqdn(const std::string& fqdn);

public:
    TraceRoute(const std::string &input_fqdn);
    TraceRoute(const std::string &input_fqdn,
        const std::string &input_nickname);
    ~TraceRoute();

    Answer start();
};

#endif // TRACEROUTE_H