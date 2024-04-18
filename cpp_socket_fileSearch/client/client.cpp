// client.cpp
#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <cstring>

int main(){

    //  [ SOCKET ]
    int socketFD = socket(AF_INET, SOCK_STREAM, 0);
    if (socketFD == -1){
        std::cerr << "[ CLIENT ] Error create socket = " << socketFD << std::endl;
        return 1; }
    else {
        std::cout << "[ CLIENT ] Created socket was successful" << std::endl; }


    //  Address for CONNECT
    struct sockaddr_in serverAddress;
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(80);
    inet_pton(AF_INET, "172.253.63.100", &serverAddress.sin_addr.s_addr);

    //  [ CONNECT ]
    int connectResult = connect(socketFD, (struct sockaddr *)&serverAddress, sizeof(serverAddress));
    if (connectResult == -1){
        std::cerr << "[ CLIENT ] Error result connect = " << connectResult << std::endl;
        return 1; }
    else {
        std::cout << "[ CLIENT ] Connection was successful" << std::endl; }


    //  [ SEND ]
    const char* send_buffer;
    send_buffer = "GET \\ HTTP/1.1\r\nHost:google.com\r\n\r\n";
    send(socketFD, send_buffer, strlen(send_buffer), 0);
    

    // [ RECV ]
    char recv_buffer[1024];
    recv(socketFD, recv_buffer, 1024, 0);

    // Answer server
    std::cout << "[ SERVER ] Response was:\n" << recv_buffer << std::endl;

    return 0;
}