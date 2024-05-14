/*

    ███████╗██╗██╗     ███████╗   ██████╗███████╗██████╗ ██╗   ██╗███████╗██████╗
    ██╔════╝██║██║     ██╔════╝  ██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
    █████╗  ██║██║     █████╗    ╚█████╗ █████╗  ██████╔╝╚██╗ ██╔╝█████╗  ██████╔╝
    ██╔══╝  ██║██║     ██╔══╝     ╚═══██╗██╔══╝  ██╔══██╗ ╚████╔╝ ██╔══╝  ██╔══██╗
    ██║     ██║███████╗███████╗  ██████╔╝███████╗██║  ██║  ╚██╔╝  ███████╗██║  ██║
    ╚═╝     ╚═╝╚══════╝╚══════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

                                                        Create by iPlugin © 
               ██████████
              ████████████
              ██        ██              MIT License
              ██▄▄▄▄▄▄▄▄▄█              
              ██▀███ ███▀█              Copyright (c) 2024 iPlugin
█             ▀█        █▀              
 █              ██                      Permission is hereby granted, free of 
██                  █                   charge, to any person obtaining a copy
█▄            ████ ██  ████             of this software and associated
 ▄███████████████  ██  ██████           documentation files (the "Software"), to
    █████████████  ██  █████████        deal in the Software without restriction,
             ████  ██ █████  ███        including without limitation the rights to
              ███  ██ █████  ███        use, copy, modify, merge, publish,
              ███     █████████         distribute, sublicense, and/or sell copies
              ██     ████████▀          of the Software, and to permit persons to
                ██████████              whom the Software is furnished to do so,
                ██████████              subject to the following conditions:
                 ████████               
                  ██████████▄▄          The above copyright notice and this
                    █████████▀          permission notice shall be included in all
                     ████  ███          copies or substantial portions of the
                    ▄████▄  ██          Software.
                    ██████   ▀
                    ▀▄▄▄▄▀

*/


#include "../includes/utils.h"
#include "../includes/searcher.h"

using namespace std;


class Server{

private:
    int serverFD;
    int clientFD;
    Logger logger;
    struct sockaddr_in address;

    
public:
    bool stopWaiting = false;

    Server(const string& logFilePath): logger(logFilePath){}
    ~Server(){}
    
    // Check count argc and int port
    bool validateArgs(int argc, char* argv[]){
        string msg_type = "[ VALID ]\t";
        string msg_done = "Valid argumants";
        string msg_error = "Invalid arguments";

        if (argc != 2 && stoi(argv[1])){
            cerr << "Example: " << program_invocation_short_name << " <port>\n"; 
            logger.log(msg_type + msg_error + strerror(errno), Logger::ERROR);
            return false;
        }
        else{
            cout << BOLDGREEN << msg_type << RESET << msg_done << "\n";
            logger.log(msg_type + msg_done, Logger::INFO);
            return true;
        }
    }


    // [ SOCKET ] create server socket
    bool serverSocket(){
        string msg_type = "[ SOCKET ]\t";
        string msg_done = "Socket created successfully";
        string msg_error = "Socket wasn`t created: ";

        serverFD = createSocket();
        if (serverFD == -1){
            cerr << BOLDRED << msg_type << RESET << strerror(errno) << "\n";
            logger.log(msg_type + msg_error + strerror(errno), Logger::ERROR);
            return false;
        }
        else{ // serverFD >= 0
            cout << BOLDGREEN << msg_type << RESET << msg_done << "\n";
            logger.log(msg_type + msg_done, Logger::INFO);
            return true;
        }
    }

    // [ BIND ]
    bool connectToServer(int port){
        string msg_type = "[ BIND ]\t";
        string msg_done = "Connection was successfully";
        string msg_error = "Connect was`t created: ";

        int bindRes = createAddress(serverFD, "", port, address);
        if (bindRes == -1){
            cerr << BOLDRED << msg_type << RESET << msg_error << strerror(errno) << "\n";
            logger.log(msg_type + msg_error + strerror(errno), Logger::ERROR);
            return false;
        }
        else{ // bindRes == 0
            cout << BOLDGREEN << msg_type << RESET << msg_done << "\n";
            logger.log(msg_type + msg_done, Logger::INFO);
            return true;
        }
    }

    // [ LISTEN ]
    bool listenServer(){
        string msg_type = "[ LISTEN ]\t";
        string msg_done = "Listening successfully";
        string msg_error = "Listen was`t created: ";

        int listenRes = listen(serverFD, 10);
        if (listenRes == -1){
            cerr << BOLDRED << msg_type << RESET << msg_error << strerror(errno) << "\n";
            logger.log(msg_type + msg_error + strerror(errno), Logger::ERROR);
            return false;
        }
        else{ // listenRes == 0
            cout << BOLDGREEN << msg_type << RESET << msg_done << "\n";
            logger.log(msg_type + msg_done, Logger::INFO);
            return true;
        }
    }


    // [ ACCEPT ]
    struct sockaddr_in *clientAddress;
    int clientAddressSize = sizeof(clientAddress);

    bool acceptServer(){
        string msg_type = "[ ACCEPT ]\t";
        string msg_done = "Accept created successfully";
        string msg_error = "Accept was`t created: ";

        clientFD = accept(serverFD, (sockaddr*)&clientAddress, (socklen_t*)&clientAddressSize);
        if (clientFD == -1){
            cerr << BOLDRED << msg_type << RESET << msg_error << strerror(errno) << "\n";
            logger.log(msg_type + msg_error + strerror(errno), Logger::ERROR);
            return false;
        }
        else{ // clientFD == 0
            cout << BOLDGREEN << msg_type << RESET << msg_done << "\n";
            logger.log(msg_type + msg_done, Logger::INFO);
            return true;
        }
    }


    // [ SEND ]
    bool sendMessage(Message &pkg){  
        string msg_type = "[ SEND ]\t";
        string msg_done = "Sent message";
        string msg_error = "Error while sending: ";

        ssize_t sendRes = send(clientFD, &pkg, sizeof(Message), 0);
        if (sendRes == -1){
            cerr << BOLDRED << msg_type << RESET << msg_error << strerror(errno) << "\n";
            logger.log(msg_type + msg_error + strerror(errno), Logger::ERROR);
            return false;
        }
        else{
            if (pkg.type == Message::SERVER_INTRODUCED){
                cout << BOLDGREEN << msg_type << RESET << msg_done + ": \n" + pkg.msg.msg_intro.intro << "\n";
                logger.log(msg_type + msg_done, Logger::INFO);
                return true;
            }
            else if (pkg.type == Message::PLEASE_WAIT){
                cout << BOLDGREEN << msg_type << RESET << msg_done + ": " + pkg.msg.msg_plswait.plswait << "\n";
                logger.log(msg_type + msg_done, Logger::INFO);
                return true;
            }
            else if (pkg.type == Message::DURATION){
                cout << BOLDGREEN << msg_type << RESET << msg_done + ": " + pkg.msg.msg_duration.duration << "\n";
                logger.log(msg_type + msg_done, Logger::INFO);
                return true;
            }
            else{ // pkg.type == Message::RESULT
                cout << BOLDGREEN << msg_type << RESET << msg_done + ": " + pkg.msg.msg_result.result << "\n";
                logger.log(msg_type + msg_done, Logger::INFO);
                return true;
            }
        }
    }


    // [ RECV ]
    string recvMessage(){
        string msg_type = "[ RECV ]\t";
        string msg_done = "Received message";
        string msg_warn = "Connection closed";
        string msg_error = "Error receiving data: ";

        Message msg;

        ssize_t recvRes = recv(clientFD, &msg, sizeof(Message), 0);
        if (recvRes == -1){
            cerr << BOLDRED << msg_type << RESET << msg_error << strerror(errno) << "\n";
            logger.log(msg_type + msg_error + strerror(errno), Logger::ERROR);
            return "";
        }
        else if (recvRes == 0){
            cout << BOLDYELLOW << "[ CONNECT ]\t" << RESET << msg_warn << "\n";
            logger.log("[ CONNECT ]\t" + msg_warn, Logger::WARNING);
            return "";
        }
        else{
            string recvBuffer;

            if (msg.type == Message::FILE_SEARCH){
                recvBuffer = msg.msg.msg_file_search.filename;

                cout << BOLDGREEN << msg_type << RESET << msg_done + ": "
                << BOLDBLUE << recvBuffer << RESET << "\n";
                logger.log(msg_type + "[ FileName ]\t" + msg_done , Logger::INFO);
                return recvBuffer;
            }
        }
        return "";
    }

    void notification(Server &server){
        Message pkg;
        pkg.type = Message::PLEASE_WAIT;
        string waiting = "Download...";
        strcpy(pkg.msg.msg_intro.intro, waiting.c_str());

        while (!stopWaiting){
            server.sendMessage(pkg);
            this_thread::sleep_for(std::chrono::milliseconds(500));
        }
    }

    void sendResult(Server &server, string &responce){
        string path;
        FileSearch search("/");
        path = search.search(responce);

        Message pkg;
        pkg.type = Message::RESULT;
        strcpy(pkg.msg.msg_intro.intro, path.c_str());
        server.sendMessage(pkg);
        stopWaiting = true;
    }
};



int main(int argc, char* argv[]){
    Server server("logs/logServer.log");                //  ▄   ▄
                                                    //  ▄█▄ █▀█▀█ ▄█▄
    if(!server.validateArgs(argc, argv)){           // ▀▀████▄█▄████▀▀
        return 1;                                       //  ▀█▀█▀
    }

    if (!server.serverSocket()){
        return 1;
    }

    int port = stoi(argv[1]);
    if (!server.connectToServer(port)){
        return 1;
    }

    if (!server.listenServer()){
        return 1;
    }
    
    if (!server.acceptServer()){
        return 1;
    }

// Part 2
    // Get filename
    string responce = server.recvMessage();
    if (responce.empty()){return 1;}


    Message pkg;
    
    // Send Intro to client
    extern string intro;    
    pkg.type = Message::SERVER_INTRODUCED;
    strcpy(pkg.msg.msg_intro.intro, intro.c_str());
    if (!server.sendMessage(pkg)){return 1;}


    thread threads_result([&server, &responce](){server.sendResult(server,responce);});
    thread status_work([&server](){server.notification(server);});

    threads_result.join();
    status_work.join();

    return 0;
}                 


//                        ▐███████▌
//                        ▐░░░░░░░▌
//                  ▄▀▀▀█ ▐░▀▀▄▀▀░▌ █▀▀▀▄
//                  ▌▌▌▌▐ ▄▌░▄▄▄░▐▄ ▌▐▐▐▐