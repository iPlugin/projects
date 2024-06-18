#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "utils/server.h"
#include "utils/client.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;

    Server server;
    engine.rootContext()->setContextProperty("server", &server);
    Client client;
    engine.rootContext()->setContextProperty("client", &client);

    const QUrl url(QStringLiteral("qrc:/socket_qml/qml/Main.qml"));
    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreationFailed,
        &app,
        []() { QCoreApplication::exit(-1); },
        Qt::QueuedConnection);
    engine.load(url);

    return app.exec();
}
