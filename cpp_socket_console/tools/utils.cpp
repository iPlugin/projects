#include "../includes/utils.h"


int createSocket(){
    return socket(AF_INET, SOCK_STREAM, 0);
}

int createAddress(int socketFD, const string &ip, int port, sockaddr_in &address){
    address.sin_port = htons(port);
    address.sin_family = AF_INET;

    if (ip.size() == 0){ // for server
        address.sin_addr.s_addr = INADDR_ANY;
        return bind(socketFD, (sockaddr*)&address, sizeof(address));
    }
    else{ // for client
        inet_pton(AF_INET, ip.c_str(), &address.sin_addr.s_addr);
        return connect(socketFD, (sockaddr*)&address, sizeof(address));
    }  
}