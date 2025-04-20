#include "cardmanager.h"
#include <QDebug>
#include <charconv>
#include <QFile>
#include <QDir>
#include <QUrl>


CardManager::CardManager(QObject *parent) : QObject(parent) {
    std::srand(std::time(nullptr));
}

int CardManager::generateRandomNumber(int min, int max) {
    return min + std::rand() % ((max + 1) - min);
}

QString CardManager::generate_dealer_card(int page_cards) {
    std::string cardPath;

    do {
        int cardNumber = generateRandomNumber(1, 13);
        int suitNumber = generateRandomNumber(1, 4);

        cardPath = "resources/cards/" + std::to_string(page_cards) +
                   "_" + std::to_string(cardNumber) +
                   "_" + std::to_string(suitNumber) + ".png";
    } while (generated_dealer_cards.find(cardPath) != generated_dealer_cards.end());

    generated_dealer_cards.insert(cardPath);

    return QString::fromStdString(cardPath);
}

QString CardManager::generate_your_card(int page_cards) {
    std::string cardPath;

    do {
        int cardNumber = generateRandomNumber(1, 13);
        int suitNumber = generateRandomNumber(1, 4);

        cardPath = "resources/cards/" + std::to_string(page_cards) +
                   "_" + std::to_string(cardNumber) +
                   "_" + std::to_string(suitNumber) + ".png";
    } while (generated_your_cards.find(cardPath) != generated_your_cards.end());

    generated_your_cards.insert(cardPath);

    return QString::fromStdString(cardPath);
}


int CardManager::sum_dealer_card() {
    int result = 0;
    bool t = false;

    for (const auto& path : generated_dealer_cards) {
        size_t startPos = path.find('_');
        size_t endPos = path.find('_', startPos + 1);

        if (startPos != std::string::npos && endPos != std::string::npos) {
            int cardValue;
            auto result_conv = std::from_chars(path.data() + startPos + 1, path.data() + endPos, cardValue);

            if (result_conv.ec == std::errc()) {

                if (cardValue == 1) {
                    t = true;
                    result += 11;
                } else if (cardValue >= 2 && cardValue <= 10) {
                    result += cardValue;
                } else if (cardValue >= 11 && cardValue <= 13) {
                    result += 10;
                }
            } else {
                qDebug() << "Помилка перетворення в число.";
            }
        }
    }

    if (t && result > 21) {
        result -= 10;
    }

    qDebug() << "Загальний результат дилера карт:" << result;
    return result;
}

int CardManager::sum_your_card() {
    int result = 0;
    bool t = false;

    for (const auto& path : generated_your_cards) {
        size_t startPos = path.find('_');
        size_t endPos = path.find('_', startPos + 1);

        if (startPos != std::string::npos && endPos != std::string::npos) {
            int cardValue;
            auto result_conv = std::from_chars(path.data() + startPos + 1, path.data() + endPos, cardValue);

            if (result_conv.ec == std::errc()) {

                if (cardValue == 1) {
                    t = true;
                    result += 11;
                } else if (cardValue >= 2 && cardValue <= 10) {
                    result += cardValue;
                } else if (cardValue >= 11 && cardValue <= 13) {
                    result += 10;
                }
            }
            else {
                qDebug() << "Помилка перетворення в число.";
            }
        }
    }

    if (t && result > 21) {
        result -= 10;
    }

    qDebug() << "Загальний результат твоїх карт:" << result;
    return result;
}

void CardManager::clearGeneratedCards() {
    generated_dealer_cards.clear();
    generated_your_cards.clear();
}


bool CardManager::saveImageToResource(const QString &fileUrl, int typeTables) {
    QString filePath = QUrl(fileUrl).toLocalFile();

    if (filePath.isEmpty()) {
        qDebug() << "Помилка: Шлях до файлу порожній.";
        return false;
    }

    QString destDirectory = "resources/tables/";
    QString destFileName = QString("%1_table.png").arg(typeTables + 1);
    QString destPath = destDirectory + destFileName;

    QDir dir;
    if (!dir.exists(destDirectory)) {
        if (!dir.mkpath(destDirectory)) {
            qDebug() << "Не вдалося створити директорію" << destDirectory;
            return false;
        }
    }

    if (QFile::copy(filePath, destPath)) {
        qDebug() << "Файл збережено успішно як" << destPath;
        return true;
    } else {
        qDebug() << "Помилка копіювання файлу з" << filePath << "до" << destPath;
        return false;
    }
}
