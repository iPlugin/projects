#ifndef CARDMANAGER_H
#define CARDMANAGER_H

#include <QObject>
#include <QString>
#include <unordered_set>
#include <cstdlib>
#include <ctime>

class CardManager : public QObject {
    Q_OBJECT

public:
    explicit CardManager(QObject *parent = nullptr);

    Q_INVOKABLE QString generate_dealer_card(int page_cards);
    Q_INVOKABLE QString generate_your_card(int page_cards);
    Q_INVOKABLE int sum_dealer_card();
    Q_INVOKABLE int sum_your_card();
    Q_INVOKABLE void clearGeneratedCards();
    Q_INVOKABLE bool saveImageToResource(const QString &filePath, int typeTables);

private:
    std::unordered_set<std::string> generated_dealer_cards;
    std::unordered_set<std::string> generated_your_cards;

    int generateRandomNumber(int min, int max);
};

#endif // CARDMANAGER_H
