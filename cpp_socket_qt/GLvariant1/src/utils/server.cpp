#include "server.h"
#include "../../include/packages.h"

Server::Server(QObject *parent)
    : QObject{parent} {}


void Server::serverSocket()
{
    serverFD = new QTcpServer(this);
    connect(serverFD, SIGNAL(connectToServer()), this, SLOT(connectToServer()));
}

void Server::connectToServer(int port) {
    if (serverFD->listen(QHostAddress::Any, port)) {
        qDebug() << "Server started!";
    }
    else {
        qDebug() << "Server cound not start!";
    }

    clientFD = serverFD->nextPendingConnection();
    clientFD->write("Hello\r\n");
    clientFD->flush();

    clientFD->waitForBytesWritten(3000);
}
