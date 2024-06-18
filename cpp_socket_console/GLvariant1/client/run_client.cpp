#include "../includes/client.h"


int main(int argc, char* argv[]){
    Client client("logs/logClient.log");
    
    if(!client.validateArgs(argc, argv)){
        return 1;
    }

    if (!client.clientSocket()){
        return 1;
    }

    string ip = argv[1];
    int port = stoi(argv[2]);
    if (!client.connectToServer(ip, port)){
        return 1;
    }
    
    string message = argv[3];
    Message pkg;
    pkg.type = Message::Type::FILE;
    strcpy(pkg.msg.file_search.filename, message.c_str());
    if (!client.sendMessage(pkg)){
        return 1;
    }

    while (true){
        string responce = client.recvMessage();
        if (responce.empty()){return 1;}
    }

    return 0;
}