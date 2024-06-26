#include "client.h"

using namespace std;

Client::Client()
{
    client_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (client_fd != -1)
    {
        cout << "Socket: Create socket" << endl; 
    }
    else
    {
        cerr << "Socket: Failed to create socket: " << strerror(errno) << endl;
    }
}

Client::~Client()
{
    close(client_fd);
}

bool Client::run()
{
    if (connectServer())
    {
        cout << "Connect: Connection successfully" << endl;
    }
    else
    {
        cerr << "Connect: Connection error" << endl;
        return false;
    }
    
    string send_buf = "Hello";
    ssize_t bytes_sent = send(client_fd, send_buf.c_str(), send_buf.size(), 0);
    if (bytes_sent > 0)
        cout << "Send: " << send_buf << endl; 
    else
    {
        cerr << "Send: Failed" << endl;
    }

    while (true)
    {
        char recv_buf[1024];
        ssize_t bytes_recv = recv(client_fd, recv_buf, sizeof(recv_buf), 0);
        if (bytes_recv > 0)
        {
            recv_buf[bytes_recv] = '\0';
            string recv_str(recv_buf);
            cout << "Recv:\t  " << recv_buf << endl;
            break;
        }
        else if (bytes_recv == 0)
        {
            cout << "Server:\t  Disconnect" << endl;
            break;
        }
        else
        {
            continue;
        }
    }


    send_buf = "Звідки беруться діти?";
    bytes_sent = send(client_fd, send_buf.c_str(), send_buf.size(), 0);
    if (bytes_sent > 0)
        cout << "Send: " << send_buf << endl; 
    else
    {
        cerr << "Send: Failed" << endl;
    }

    while (true)
    {
        char recv_buf[1024];
        ssize_t bytes_recv = recv(client_fd, recv_buf, sizeof(recv_buf), 0);
        if (bytes_recv > 0)
        {
            recv_buf[bytes_recv] = '\0';
            string recv_str(recv_buf);
            cout << "Recv:\t  " << recv_buf << endl;
        }
        else if (bytes_recv == 0)
        {
            cout << "Server:\t  Disconnect" << endl;
            break;
        }
        else
        {
            continue;
        }
    }

    return true;
}

bool Client::connectServer()
{
    server_addr.sin_family = AF_INET;
    inet_pton(AF_INET, server_ip.c_str(), &server_addr.sin_addr.s_addr);
    server_addr.sin_port = htons(server_port);
    return connect(client_fd, (sockaddr*)&server_addr, sizeof(server_addr)) == 0;
}