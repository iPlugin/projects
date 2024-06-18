#include "../includes/client.h"

using namespace std;

// Check count argc and int port
bool Client::validateArgs(int argc, char* argv[]){
    string msg_type = "[ VALID ]\t";
    string msg_done = "Valid argumants";
    string msg_error = "Invalid arguments";

    if (argc != 4 && stoi(argv[2])){
        std::cerr << "Example: " << program_invocation_short_name << " <ip> <port> <fileSearch>\n"; 
        logger.log(msg_type + msg_error + strerror(errno), Logger::ERROR);
        return false;
    }
    else{
        #ifdef debug
            cout << BOLDGREEN << msg_type << RESET << msg_done << "\n";
        #endif // debug
        logger.log(msg_type + msg_done, Logger::INFO);
        return true;
    }
}

// [ SOCKET ] create client socket
bool Client::clientSocket(){
    string msg_type = "[ SOCKET ]\t";
    string msg_done = "Socket created successfully";
    string msg_error = "Socket wasn`t created: ";

    clientFD = createSocket();
    if (clientFD == -1){
        cerr << BOLDRED << msg_type << RESET << strerror(errno) << "\n";
        logger.log(msg_type + msg_error + strerror(errno), Logger::ERROR);
        return false;
    }
    else{ // clientFD >= 0
        #ifdef debug
            cout << BOLDGREEN << msg_type << RESET << msg_done << "\n";
        #endif // debug
        logger.log(msg_type + msg_done, Logger::INFO);
        return true;
    }
}

// [ CONNECT ] create connect
bool Client::connectToServer(const string& ip, int port){
    string msg_type = "[ CONNECT ]\t";
    string msg_done = "Connection was successfully";
    string msg_error = "Connect was`t created: ";

    int connectRes = createAddress(clientFD, ip, port, address);
    if (connectRes == -1){
        cerr << BOLDRED << msg_type << RESET << msg_error << "\n";
        logger.log(msg_type + msg_error + strerror(errno), Logger::ERROR);
        return false;
    }
    else{ // connectRes == 0
        #ifdef debug
            cout << BOLDGREEN << msg_type << RESET << msg_done << "\n";
        #endif // debug
        logger.log(msg_type + msg_done, Logger::INFO);
        return true;
    }
}

// [ SEND ]
bool Client::sendMessage(Message &pkg){
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
        #ifdef debug
            cout << BOLDGREEN << msg_type << RESET << msg_done + ": "
            << BOLDMAGENTA << pkg.msg.file_search.filename << RESET << "\n";
        #endif // debug
        logger.log(msg_type + msg_done, Logger::INFO);
        return true;
    }
}


// [ RECV ]
string Client::recvMessage(){
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
        #ifdef debug
            cout << BOLDYELLOW << "[ CONNECT ]\t" << RESET << msg_warn << "\n";
        #endif // debug
        logger.log("[ CONNECT ]\t" + msg_warn, Logger::WARNING);
        return "";
    }
    else{
        string recvBuffer;

        switch (msg.type){
        case Message::Type::INTRO:
            recvBuffer = msg.msg.server_introduced.intro;
            
            #ifdef debug
                cout << BOLDGREEN << msg_type << RESET << msg_done + ": " << "\n";
            #endif // debug
            cout << BOLDRED << recvBuffer << RESET << "\n";
            logger.log(msg_type + "[ Intro ]\t" + msg_done, Logger::INFO);
            return recvBuffer;
            break;
        case Message::Type::WAIT:
            recvBuffer = msg.msg.please_wait.plswait;

            #ifdef debug
                cout << BOLDGREEN << msg_type << RESET << msg_done + ": ";
            #endif // debug
            cout << recvBuffer << "\n"; 
            logger.log(msg_type + "[ PlsWait ]\t" + msg_done, Logger::INFO);
            return recvBuffer;
        default: // Message::Type::RESULT
            recvBuffer = msg.msg.result_path.result;

            #ifdef debug
                cout << BOLDGREEN << msg_type << RESET << msg_done + ": ";
            #endif // debug
            cout << recvBuffer << "\n";
            logger.log(msg_type + "[ Result ]\t" + msg_done, Logger::INFO);
            return recvBuffer;
            break;
        }
    }
}