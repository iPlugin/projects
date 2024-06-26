#include "server.h"

using namespace std;
using namespace liboai;

Server::Server()
{
    cout << "Server:\t  Starting..." << endl; 
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd != -1)
    {
        cout << "Socket:\t  Successfully" << endl;
    }
    else
    {
        cerr << "Socket:\t  Failed - " << strerror(errno) << endl;
    }
}

Server::~Server()
{
    close(server_fd);
}


bool Server::run()
{
    if (bindServer())
    {
        cout << "Bind:\t  Successfully" << endl;
    }
    else
    {
        cerr << "Bind:\t  Socket binding error" << endl;
        return false;
    }

    if (listenServer())
    {
        cout << "Listen:\t  Successfully\n" << endl;
    }
    else
    {
        cerr << "Listen:\t  Error listening on socket" << endl;
        return false;
    }

    while (true)
    {    
        if (acceptServer())
        {
            cout << "\nAccept:\t  New client" << endl;
        }
        else
        {
            cerr << "Accept:\t  Failed" << endl;
            return false;
        }

        while (true)
        {
            char recv_buf[1024];
            ssize_t bytes_recv = recv(client_fd, recv_buf, sizeof(recv_buf), 0);
            if (bytes_recv > 0)
            {
                recv_buf[bytes_recv] = '\0';
                string recv_str(recv_buf), command, action, object;
                istringstream iss(recv_str);
                iss >> command >> action >> object;

                cout << "Recv:\t  " << recv_buf << endl;

                if (command == "processes")
                {
                    ProcessManager processManager;
                    if (action == "show")
                    {
                        processManager.printProcesses();
                        ssize_t bytes_sent = send(client_fd, command.c_str(), command.size(), 0);
                        if (bytes_sent > 0)
                            cout << "Send:\t  " << command << endl; 
                        else
                        {
                            cerr << "Send:\t  Failed" << endl;
                        }
                    }
                    else if (action == "kill" && !object.empty())
                    {
                        /* code */
                    }
                    else
                    {
                        /* Тут має писати типу що в каталозі процес нема такої дії */
                    }
                    

                    
                    
                }
                else
                {
                    if (!OPENAI_API_KEY.empty())
                    {
                        string responce = chatgpt(recv_str);
                        ssize_t bytes_sent = send(client_fd, responce.c_str(), responce.size(), 0);
                        if (bytes_sent > 0)
                            cout << "Send:\t  " << responce << endl; 
                        else
                        {
                            cerr << "Send:\t  Failed" << endl;
                        }
                    }
                    else
                    {
                        string responce = "We cannot provide such information";
                        ssize_t bytes_sent = send(client_fd, responce.c_str(), responce.size(), 0);
                        if (bytes_sent > 0)
                            cout << "Send:\t  " << responce << endl; 
                        else
                        {
                            cerr << "Send:\t  Failed" << endl;
                        }
                    }
                    
                    
                }
            }
            else if (bytes_recv == 0)
            {
                cout << "Accept:\t  Client left" << endl;
                break;
            }
            else
            {
                continue;
            }
        }
    }
    return true;
}

// ##################################################

bool Server::bindServer()
{
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY; // inet_addr(server_ip.c_str())
    server_addr.sin_port = htons(server_port);
    return bind(server_fd, (sockaddr*)&server_addr, sizeof(server_addr)) == 0;
}

bool Server::listenServer()
{
    return listen(server_fd, 10) == 0;
}

bool Server::acceptServer()
{   
    client_addr_len = sizeof(client_addr);
    client_fd = accept(server_fd, (sockaddr*)&client_addr, &client_addr_len);
    return client_fd != -1;
}

// ##################################################


string Server::chatgpt(string message) {
    OpenAI oai;

    Conversation convo;
    string server_info =
    "You received a message from the C++ Client/Server application\n"
    "The server can:\n"
    "1) Return all currently running processes to the client\n"
    "2) Also provide an opportunity to complete them\n"
    "When the server cannot process the user's request, "
    "it forwards the message to you.\n"
    "You must give short and meaningful answers to the client";

    convo.AddUserData(server_info + message);

    if (oai.auth.SetKey(OPENAI_API_KEY)) {
        try {
            Response response = oai.ChatCompletion->create("gpt-3.5-turbo", convo);
            convo.Update(response);

            // Print the response
            // std::cout << "Response from OpenAI: " << convo.GetLastResponse() << std::endl;
        }
        catch (std::exception& e) {
            std::cerr << "Error: " << e.what() << std::endl;
        }
    }

    return convo.GetLastResponse();
}