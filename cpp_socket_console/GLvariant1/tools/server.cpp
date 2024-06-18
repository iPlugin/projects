#include "../includes/server.h"

using namespace std;

// Check count argc and int port
bool Server::parseArgs(int argc, char* argv[]){
    string msg_type = "[ VALID ]\t";
    string msg_done = "Valid argumants";
    string msg_error = "Invalid arguments";

    if (argc != 2){
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
bool Server::serverSocket(){
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
bool Server::connectToServer(int port){
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
bool Server::listenServer(){
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
bool Server::acceptServer(){
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
bool Server::sendMessage(Message &pkg){  
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
        if (pkg.type == Message::Type::INTRO){
            cout << BOLDGREEN << msg_type << RESET << msg_done + ": \n" + pkg.msg.server_introduced.intro << "\n";
            logger.log(msg_type + msg_done, Logger::INFO);
            return true;
        }
        else if (pkg.type == Message::Type::WAIT){
            cout << BOLDGREEN << msg_type << RESET << msg_done + ": " + pkg.msg.please_wait.plswait << "\n";
            logger.log(msg_type + msg_done, Logger::INFO);
            return true;
        }
        else{ // pkg.type == Message::Type::RESULT
            cout << BOLDGREEN << msg_type << RESET << msg_done + ": " + pkg.msg.result_path.result << "\n";
            logger.log(msg_type + msg_done, Logger::INFO);
            return true;
        }
    }
}


// [ RECV ]
string Server::recvMessage(){
    string msg_type = "[ RECV ]\t";
    string msg_done = "Received message";
    string msg_warn = "Connection closed";
    string msg_error = "Error receiving data: ";

    Message pkg;

    ssize_t recvRes = recv(clientFD, &pkg, sizeof(Message), 0);

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

        pkg.type == Message::Type::FILE;
        recvBuffer = pkg.msg.file_search.filename;

        cout << BOLDGREEN << msg_type << RESET << msg_done + ": "
        << BOLDBLUE << recvBuffer << RESET << "\n";
        logger.log(msg_type + "[ FileName ]\t" + msg_done , Logger::INFO);
        return recvBuffer;
    }
    return "";
}

void Server::notification(Server &server){
    Message pkg;
    pkg.type = Message::Type::WAIT;
    string waiting = "Download...";
    strcpy(pkg.msg.please_wait.plswait, waiting.c_str());

    while (!stopWaiting){
        server.sendMessage(pkg);
        this_thread::sleep_for(std::chrono::milliseconds(500));
    }
}

void Server::sendResult(Server &server, string &responce){
    string path;
    FileSearch search("/");
    path = search.search(responce);

    Message pkg;
    pkg.type = Message::Type::RESULT;
    strcpy(pkg.msg.result_path.result, path.c_str());
    server.sendMessage(pkg);
    stopWaiting = true;
}