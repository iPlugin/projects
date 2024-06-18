#include "client.h"
#include "../../include/packages.h"

Client::Client(QObject *parent)
    : QObject{parent}
{}

void Client::clientSocket() {
    clientFD = new QTcpSocket(this);
    if (clientFD) {
        emit messageReceived("[ SOCKET ]\t Socket created successfully");
    }
    else {
        emit messageReceived("[ SOCKET ]\t Socket wasn`t created");
    }
}

void Client::connectToServer(const QString ip, int port) {
    clientFD->connectToHost(ip, port);
    if (clientFD->waitForConnected(3000)) {
        emit messageReceived("[ CONNECT ]\t Connection was successfully");
    }
    else {
        emit messageReceived("[ CONNECT ]\t Connect was`t created");
        clientFD->close();
    }
}

void Client::send_msg_filename(const QString &msg)
{
    Message pkg;
    pkg.type = Message::FILE_SEARCH;
    QByteArray byteArray = msg.toUtf8();
    strncpy(pkg.msg.msg_file_search.filename, byteArray.constData(), sizeof(pkg.msg.msg_file_search.filename) - 1);
    pkg.msg.msg_file_search.filename[sizeof(pkg.msg.msg_file_search.filename) - 1] = '\0';
    clientFD->write(reinterpret_cast<char*>(&pkg), sizeof(pkg));
    // clientFD->waitForBytesWritten(1000);
}

std::string Client::recv_msg()
{
    while (clientFD->isOpen()) { // Продовжувати, поки з'єднання відкрите
        if (!clientFD->waitForReadyRead(-1)) { // Чекаємо на готовність для читання
            qDebug() << "Connection lost. Exiting loop."; // Виходимо з циклу, якщо з'єднання втрачено
            break;
        }

        Message pkg;
        // qDebug() << "Reading: " << clientFD->bytesAvailable();
        QByteArray byteArray = clientFD->readAll();
        memcpy(&pkg, byteArray.data(), sizeof(Message));
        std::string recvBuffer;

        if (pkg.type == Message::SERVER_INTRODUCED){
            recvBuffer = pkg.msg.msg_intro.intro;
            qDebug() << pkg.msg.msg_intro.intro;
            emit messageReceived(pkg.msg.msg_intro.intro);
        }
        else if (pkg.type == Message::PLEASE_WAIT){
            recvBuffer = pkg.msg.msg_plswait.plswait;
            qDebug() << pkg.msg.msg_plswait.plswait;
            emit messageReceived(pkg.msg.msg_plswait.plswait);
        }
        else if (pkg.type == Message::RESULT){ // Повідомлення про результат
            recvBuffer = pkg.msg.msg_result.result;
            qDebug() << pkg.msg.msg_result.result;
            emit messageReceived(pkg.msg.msg_result.result);
        }

        // Опрацьовуємо отримані дані або передаємо їх для обробки
        // emit messageReceived(QString::fromStdString(recvBuffer));
    }

    // Закриваємо з'єднання
    clientFD->close();
    return ""; // Повертаємо порожній рядок при завершенні роботи
}

