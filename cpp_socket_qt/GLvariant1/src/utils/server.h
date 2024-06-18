#ifndef SERVER_H
#define SERVER_H

#include <QObject>
#include <QDebug>
#include <QTcpServer>
#include <QTcpSocket>

class Server : public QObject
{
    Q_OBJECT
public:
    explicit Server(QObject *parent = nullptr);
    Q_INVOKABLE void serverSocket();
    Q_INVOKABLE void connectToServer(int port);
    Q_INVOKABLE void send_msg_filename(const QString &msg);
    Q_INVOKABLE std::string recv_msg();
signals:
    void messageReceived(const QString &message);
private:
    QTcpServer *serverFD;
    QTcpSocket *clientFD;
};

#endif // SERVER_H
