#include "../includes/utils.h"

#define debug

using namespace std;


class Client{
private:
    int clientFD;
    Logger logger;
    struct sockaddr_in address;
public:

    Client(const string& logFilePath): logger(logFilePath){}
    ~Client(){}

    // Check count argc and int port
    bool validateArgs(int argc, char* argv[]){
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
    bool clientSocket(){
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
    bool connectToServer(const string& ip, int port){
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
            #ifdef debug
                cout << BOLDGREEN << msg_type << RESET << msg_done + ": "
                << BOLDMAGENTA << pkg.msg.msg_file_search.filename << RESET << "\n";
            #endif // debug
            logger.log(msg_type + msg_done, Logger::INFO);
            return true;
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
            #ifdef debug
                cout << BOLDYELLOW << "[ CONNECT ]\t" << RESET << msg_warn << "\n";
            #endif // debug
            logger.log("[ CONNECT ]\t" + msg_warn, Logger::WARNING);
            return "";
        }
        else{
            string recvBuffer;

            if (msg.type == Message::SERVER_INTRODUCED){
                recvBuffer = msg.msg.msg_intro.intro;
                
                #ifdef debug
                    cout << BOLDGREEN << msg_type << RESET << msg_done + ": " << "\n";
                #endif // debug
                cout << BOLDRED << recvBuffer << RESET << "\n";
                logger.log(msg_type + "[ Intro ]\t" + msg_done, Logger::INFO);
                return recvBuffer;
            }
            else if (msg.type == Message::PLEASE_WAIT){
                recvBuffer = msg.msg.msg_plswait.plswait;

                #ifdef debug
                    cout << BOLDGREEN << msg_type << RESET << msg_done + ": ";
                #endif // debug
                cout << recvBuffer << "\n"; 
                logger.log(msg_type + "[ PlsWait ]\t" + msg_done, Logger::INFO);
                return recvBuffer;
            }
            else if (msg.type == Message::DURATION){
                recvBuffer = msg.msg.msg_duration.duration;

                #ifdef debug
                    cout << BOLDGREEN << msg_type << RESET << msg_done + ": ";
                #endif // debug
                cout << recvBuffer << "\n";
                logger.log(msg_type + "[ Duration ]\t" + msg_done, Logger::INFO);
                return recvBuffer;
            }
            else{ // msg.type == Message::RESULT
                recvBuffer = msg.msg.msg_result.result;

                #ifdef debug
                    cout << BOLDGREEN << msg_type << RESET << msg_done + ": ";
                #endif // debug
                cout << recvBuffer << "\n";
                logger.log(msg_type + "[ Result ]\t" + msg_done, Logger::INFO);
                return recvBuffer;
            }
        }
    }
};


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

// Part 2
    
    string message = argv[3];
    Message pkg;
    pkg.type = Message::FILE_SEARCH;
    strcpy(pkg.msg.msg_file_search.filename, message.c_str());
    if (!client.sendMessage(pkg)){
        return 1;
    }

    while (true){
        string responce = client.recvMessage();
        if (responce.empty()){return 1;}
    }

    return 0;
}