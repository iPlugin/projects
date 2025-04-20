#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "cardmanager.h"


int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    CardManager cardManager;

    QQmlApplicationEngine engine;
    engine.rootContext()->setContextProperty("cardManager", &cardManager);

    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreationFailed,
        &app,
        []() { QCoreApplication::exit(-1); },
        Qt::QueuedConnection);

    engine.loadFromModule("BlackJack", "Main");

    return app.exec();
}
