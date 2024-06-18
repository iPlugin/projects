#ifndef CLIENT_H
#define CLIENT_H

#include <QObject>
#include <QTcpSocket>
#include <QDebug>
#include <cstring>
#include "../../include/packages.h"

class Client : public QObject
{
    Q_OBJECT
public:
    explicit Client(QObject *parent = nullptr);
    Q_INVOKABLE void clientSocket();
    Q_INVOKABLE void connectToServer(const QString ip, int port);
    Q_INVOKABLE void send_msg_filename(const QString &msg);
    Q_INVOKABLE std::string recv_msg();
signals:
    void messageReceived(const QString &message);
private:
    QTcpSocket *clientFD;
};

#endif // CLIENT_H
