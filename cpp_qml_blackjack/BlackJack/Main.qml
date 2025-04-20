import QtQuick 2.15
import QtQuick.Controls 2.15
import Qt.labs.platform 1.1
import QtQuick.Window 2.15


pragma ComponentBehavior: Bound

ApplicationWindow {
    id: window
    visible: true
    minimumWidth: 800
    minimumHeight: 600
    maximumWidth: 800
    maximumHeight: 600
    title: "BlackJack"

    property int type_cards: 2
    property int type_tables: 2

    property int page_cards: 0
    property int page_tables: 0

    property int cardsOnTable: 2

    property int balance: 1000
    property int bet: 0

    Item {
        focus: true
        Keys.onPressed: (event) => {
            if (event.key === Qt.Key_Enter && window.page_cards != 0 && window.page_tables != 0) {
                stackView.push(secondPage);
            }
            else if (event.key === Qt.Key_Enter && window.page_cards === 0) {
                stackView.push(thirdPage);
            }
            else if (event.key === Qt.Key_Enter && window.page_tables === 0) {
                stackView.push(fourthPage);
            }
            else if (event.key === Qt.Key_Escape) {
                stackView.pop();
            }
        }
    }

    StackView {
        id: stackView
        anchors.fill: parent
        initialItem: main
    }

    Component {
        id: main
        Page {
            Image {
                id: main_bckImg
                source: "resources/images/promo.jpg"
                anchors.fill: parent
                fillMode: Image.PreserveAspectCrop
            }
            Text {
                text: "Click enter for start game ..."
                font.family: "Arial Black"
                font.pixelSize: 20
                font.bold: true
                color: "#DAA520"
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: 160
            }

            Image {
                id: chip
                source: "resources/images/chip.png"
                width: 50
                height: 50
                visible: window.bet === 0 && window.balance <= 5
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: -100
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        window.balance = 1000
                    }
                }
            }

            Row {
                id: main_cards
                anchors.horizontalCenter: parent.left
                anchors.horizontalCenterOffset: 100
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: 160
                spacing: 20  // Відстань між кнопками
                Image {
                    id: main_card_left
                    source: "resources/images/left.png"
                    width: 30
                    height: 70
                    fillMode: Image.PreserveAspectFit
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            window.page_cards = (window.page_cards + 1) % (window.type_cards + 1); // +1 Add Icon
                        }
                    }
                }
                Image {
                    id: main_cards_center
                    source: {
                        if (window.page_cards === 0) {
                            return "resources/images/plus.png";
                        }
                        else {
                            return "resources/cards/" + window.page_cards + "_13_1.png";
                        }
                    }
                    width: 30
                    height: 70
                    fillMode: Image.PreserveAspectFit
                }
                Image {
                    id: main_card_right
                    source: "resources/images/right.png"
                    width: 30
                    height: 70
                    fillMode: Image.PreserveAspectFit
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            window.page_cards = (window.page_cards + 1) % (window.type_cards + 1); // +1 Add Icon
                        }
                    }
                }
            }

            Row {
                id: main_tables
                anchors.horizontalCenter: parent.right
                anchors.horizontalCenterOffset: -100
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: 160
                spacing: 20

                Image {
                    id: main_tables_left
                    source: "resources/images/left.png"
                    width: 30
                    height: 70
                    fillMode: Image.PreserveAspectFit
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            window.page_tables = (window.page_tables + 1) % (window.type_tables + 1); // +1 Add Icon
                        }
                    }
                }

                Image {
                    id: main_tables_center
                    source: {
                        if (window.page_tables === 0) {
                            return "resources/images/plus.png";
                        }
                        else {
                            return "resources/tables/" + window.page_tables + "_table.png";
                        }
                    }
                    width: 60
                    height: 70
                    fillMode: Image.PreserveAspectFit
                }

                Image {
                    id: main_tables_right
                    source: "resources/images/right.png"
                    width: 30
                    height: 70
                    fillMode: Image.PreserveAspectFit
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            window.page_tables = (window.page_tables + 1) % (window.type_tables + 1); // +1 Add Icon
                        }
                    }
                }
            }
        }
    }

    Component {
        id: secondPage
        Page {
            Image {
                id: bckImg
                source: "resources/tables/" + window.page_tables + "_table.png"
                anchors.fill: parent
                fillMode: Image.PreserveAspectCrop
            }

            Text {
                text: "Balance: " + window.balance + "$ | Bet: " + window.bet
                font.pixelSize: 20
                font.bold: true
                anchors.bottom: parent.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                color: "black"
            }

            Image {
                id: back
                source: "resources/images/back.png"
                width: 50
                height: 50
                visible: window.bet === 0 && window.balance <= 5
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.margins: 10
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        stackView.pop();
                        draw.visible = false
                        win.visible = false
                        lose.visible = false

                        chip10.visible = true
                        chip25.visible = true
                        chip50.visible = true
                        chip100.visible = true

                        dealer_cards_1.visible = false
                        dealer_cards_1.source = "resources/cards/" + window.page_cards + "_0_0.png"
                        dealer_cards_2.visible = false
                        dealer_cards_2.source = "resources/cards/" + window.page_cards + "_0_0.png"
                        dealer_cards_3.visible = false
                        dealer_cards_3.source = "resources/cards/" + window.page_cards + "_0_0.png"

                        yours_cards_1.visible = false
                        yours_cards_1.source = "resources/cards/" + window.page_cards + "_0_0.png"
                        yours_cards_2.visible = false
                        yours_cards_2.source = "resources/cards/" + window.page_cards + "_0_0.png"
                        yours_cards_3.visible = false
                        yours_cards_3.source = "resources/cards/" + window.page_cards + "_0_0.png"
                        yours_cards_4.visible = false
                        yours_cards_4.source = "resources/cards/" + window.page_cards + "_0_0.png"
                        yours_cards_5.visible = false
                        yours_cards_5.source = "resources/cards/" + window.page_cards + "_0_0.png"
                        window.cardsOnTable = 2

                        cardManager.clearGeneratedCards()
                    }
                }
            }

            Image {
                id: stand
                source: "resources/images/stand.png"
                width: 50
                height: 50
                visible: false
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.margins: 50
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        dealer_cards_2.source = cardManager.generate_dealer_card(window.page_cards);
                        hit.visible = false
                        stand.visible = false
                        restart.visible = true
                        if (cardManager.sum_dealer_card() < 17) {
                            dealer_cards_3.visible = true;
                            dealer_cards_3.source = cardManager.generate_dealer_card(window.page_cards);
                            start_dealer_cards_3.start();
                        }

                        if (cardManager.sum_dealer_card() <= 21 && cardManager.sum_your_card() <= 21) {
                            if (cardManager.sum_dealer_card() === cardManager.sum_your_card()) {
                                draw.visible = true
                                window.balance += window.bet
                                window.bet = 0
                            }
                            else if (cardManager.sum_dealer_card() > cardManager.sum_your_card()) {
                                lose.visible = true
                                window.bet = 0
                            }
                            else if (cardManager.sum_dealer_card() < cardManager.sum_your_card()) {
                                win.visible = true
                                window.balance += window.bet * 2
                                window.bet = 0
                            }
                        }
                        else {
                            if (cardManager.sum_dealer_card() > 21 && cardManager.sum_your_card() > 21) {
                                draw.visible = true
                                window.balance += window.bet
                                window.bet = 0
                            }
                            else if (cardManager.sum_dealer_card() > 21 && cardManager.sum_your_card() < 21) {
                                win.visible = true
                                window.balance += window.bet * 2
                                window.bet = 0
                            }
                            else if (cardManager.sum_dealer_card() < 21 && cardManager.sum_your_card() > 21) {
                                lose.visible = true
                                window.bet = 0
                            }
                        }
                    }
                }
            }

            Image {
                id: hit
                source: "resources/images/hit.png"
                width: 50
                height: 50
                visible: false
                anchors.right: stand.right
                anchors.bottom: stand.top
                anchors.bottomMargin: 20
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        window.cardsOnTable += 1
                        if (window.cardsOnTable === 3){
                            yours_cards_3.visible = true
                            start_yours_cards_3.start()
                        }
                        else if (window.cardsOnTable === 4){
                            yours_cards_4.visible = true
                            start_yours_cards_4.start()
                        }
                        else if (window.cardsOnTable === 5){
                            yours_cards_5.visible = true
                            start_yours_cards_5.start()
                            hit.visible = false
                        }
                    }
                }
            }

            Image {
                id: play
                source: "resources/images/joker.png"
                width: 50
                height: 50
                visible: false
                anchors.right: return_chip.right
                anchors.bottom: return_chip.top
                anchors.bottomMargin: 20
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        dealer_cards_1.visible = true;
                        start_dealer_cards_1.start();
                        hit.visible = true;
                        stand.visible = true;
                        chip10.visible = false;
                        chip25.visible = false;
                        chip50.visible = false;
                        chip100.visible = false;
                        play.visible = false;
                        return_chip.visible = false;
                    }
                }
            }

            Image {
                id: return_chip
                source: "resources/images/return.png"
                width: 50
                height: 50
                visible: false
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.margins: 50
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        play.visible = false
                        return_chip.visible = false
                        window.balance += window.bet
                        window.bet = 0
                    }
                }
            }

            Image {
                id: restart
                source: "resources/images/return.png"
                width: 50
                height: 50
                visible: false
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        draw.visible = false
                        win.visible = false
                        lose.visible = false

                        chip10.visible = true
                        chip25.visible = true
                        chip50.visible = true
                        chip100.visible = true

                        dealer_cards_1.visible = false
                        dealer_cards_1.source = "resources/cards/" + window.page_cards + "_0_0.png"
                        dealer_cards_1.x = window.width
                        dealer_cards_2.visible = false
                        dealer_cards_2.source = "resources/cards/" + window.page_cards + "_0_0.png"
                        dealer_cards_2.x = window.width
                        dealer_cards_3.visible = false
                        dealer_cards_3.source = "resources/cards/" + window.page_cards + "_0_0.png"
                        dealer_cards_3.x = window.width

                        yours_cards_1.visible = false
                        yours_cards_1.source = "resources/cards/" + window.page_cards + "_0_0.png"
                        yours_cards_1.x = window.width
                        yours_cards_2.visible = false
                        yours_cards_2.source = "resources/cards/" + window.page_cards + "_0_0.png"
                        yours_cards_2.x = window.width
                        yours_cards_3.visible = false
                        yours_cards_3.source = "resources/cards/" + window.page_cards + "_0_0.png"
                        yours_cards_3.x = window.width
                        yours_cards_4.visible = false
                        yours_cards_4.source = "resources/cards/" + window.page_cards + "_0_0.png"
                        yours_cards_4.x = window.width
                        yours_cards_5.visible = false
                        yours_cards_5.source = "resources/cards/" + window.page_cards + "_0_0.png"
                        yours_cards_5.x = window.width
                        window.cardsOnTable = 2

                        cardManager.clearGeneratedCards()
                        restart.visible = false
                    }
                }
            }

            Image {
                id: draw
                source: "resources/images/draw.png"
                width: 140
                height: 75
                visible: false
                anchors.left: restart.right
                anchors.verticalCenter: parent.verticalCenter
            }
            Image {
                id: lose
                source: "resources/images/lose.png"
                width: 140
                height: 75
                visible: false
                anchors.left: restart.right
                anchors.verticalCenter: parent.verticalCenter
            }
            Image {
                id: win
                source: "resources/images/win.png"
                width: 140
                height: 75
                visible: false
                anchors.left: restart.right
                anchors.verticalCenter: parent.verticalCenter
            }

            Image {
                id: chip10
                source: "resources/images/10-chip.png"
                width: 50
                height: 50
                visible: true
                anchors.left: parent.left
                anchors.bottom: parent.bottom
                anchors.margins: 10
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        if (window.balance >= 10){
                            window.bet += 10
                            window.balance -= 10
                            play.visible = true
                            return_chip.visible = true
                        }
                    }
                }
            }

            Image {
                id: chip25
                source: "resources/images/25-chip.png"
                width: 50
                height: 50
                visible: true
                anchors.right: chip10.right
                anchors.bottom: chip10.top
                anchors.bottomMargin: 10
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        if (window.balance >= 25){
                            window.bet += 25
                            window.balance -= 25
                            play.visible = true
                            return_chip.visible = true
                        }
                    }
                }
            }

            Image {
                id: chip50
                source: "resources/images/50-chip.png"
                width: 50
                height: 50
                visible: true
                anchors.right: chip25.right
                anchors.bottom: chip25.top
                anchors.bottomMargin: 10
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        if (window.balance >= 50){
                            window.bet += 50
                            window.balance -= 50
                            play.visible = true
                            return_chip.visible = true
                        }
                    }
                }
            }

            Image {
                id: chip100
                source: "resources/images/100-chip.png"
                width: 50
                height: 50
                visible: true
                anchors.right: chip50.right
                anchors.bottom: chip50.top
                anchors.bottomMargin: 10
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        if (window.balance >= 100){
                            window.bet += 100
                            window.balance -= 100
                            play.visible = true
                            return_chip.visible = true
                        }
                    }
                }
            }


            Item {
                id: dealer_cards
                width: window.width
                height: window.height

                Image {
                    id: dealer_cards_1
                    source: "resources/cards/" + window.page_cards + "_0_0.png"
                    x: window.width
                    y: window.height / 2 - height - 100
                    width: 70
                    height: 120
                    visible: false

                    PropertyAnimation {
                        id: start_dealer_cards_1
                        target: dealer_cards_1
                        properties: "x"
                        duration: 200
                        to: window.width / 2 - 35
                        onFinished: {
                            dealer_cards_1.source = cardManager.generate_dealer_card(window.page_cards);
                            dealer_cards_2.visible = true;
                            start_dealer_cards_2.start();
                        }
                    }
                }

                Image {
                    id: dealer_cards_2
                    source: "resources/cards/" + window.page_cards + "_0_0.png"
                    x: window.width
                    y: window.height / 2 - height - 100
                    width: 70
                    height: 120
                    visible: false

                    PropertyAnimation {
                        id: start_dealer_cards_2
                        target: dealer_cards_2
                        properties: "x"
                        duration: 200
                        to: window.width / 2 - 15
                        onFinished: {
                            yours_cards_1.visible = true;
                            start_yours_cards_1.start();
                        }
                    }
                }

                Image {
                    id: dealer_cards_3
                    source: "resources/cards/" + window.page_cards + "_0_0.png"
                    x: window.width
                    y: window.height / 2 - height - 100
                    width: 70
                    height: 120
                    visible: false

                    PropertyAnimation {
                        id: start_dealer_cards_3
                        target: dealer_cards_3
                        properties: "x"
                        duration: 200
                        to: window.width / 2 + 5

                    }
                }
            }

            Item {
                id: yours_cards
                width: window.width
                height: window.height

                Image {
                    id: yours_cards_1
                    source: "resources/cards/" + window.page_cards + "_0_0.png"
                    x: -width
                    y: window.height / 2 - height + 250
                    width: 70
                    height: 120
                    visible: false

                    PropertyAnimation {
                        id: start_yours_cards_1
                        target: yours_cards_1
                        properties: "x"
                        duration: 200
                        to: window.width / 2 - 35
                        onFinished: {
                            yours_cards_1.source = cardManager.generate_your_card(window.page_cards);
                            yours_cards_2.visible = true;
                            start_yours_cards_2.start();
                        }
                    }
                }

                // Друга карта з правого боку
                Image {
                    id: yours_cards_2
                    source: "resources/cards/" + window.page_cards + "_0_0.png"
                    x: window.width
                    y: window.height / 2 - height + 250
                    width: 70
                    height: 120
                    visible: false

                    PropertyAnimation {
                        id: start_yours_cards_2
                        target: yours_cards_2
                        properties: "x"
                        duration: 200
                        to: window.width / 2 - 15
                        onFinished: {
                            yours_cards_2.source = cardManager.generate_your_card(window.page_cards);
                        }
                    }
                }
                Image {
                    id: yours_cards_3
                    source: "resources/cards/" + window.page_cards + "_0_0.png"
                    x: window.width  // початкове розташування за межами правого краю
                    y: window.height / 2 - height + 250
                    width: 70
                    height: 120
                    visible: false

                    PropertyAnimation {
                        id: start_yours_cards_3
                        target: yours_cards_3
                        properties: "x"
                        duration: 200
                        to: window.width / 2 + 5
                        onFinished: {
                            yours_cards_3.source = cardManager.generate_your_card(window.page_cards);
                        }
                    }
                }
                Image {
                    id: yours_cards_4
                    source: "resources/cards/" + window.page_cards + "_0_0.png"
                    x: window.width  // початкове розташування за межами правого краю
                    y: window.height / 2 - height + 250
                    width: 70
                    height: 120
                    visible: false

                    PropertyAnimation {
                        id: start_yours_cards_4
                        target: yours_cards_4
                        properties: "x"
                        duration: 200
                        to: window.width / 2 + 25  // кінцеве положення карти по горизонталі
                        onFinished: {
                            yours_cards_4.source = cardManager.generate_your_card(window.page_cards);
                        }
                    }
                }
                Image {
                    id: yours_cards_5
                    source: "resources/cards/" + window.page_cards + "_0_0.png"
                    x: window.width  // початкове розташування за межами правого краю
                    y: window.height / 2 - height + 250
                    width: 70
                    height: 120
                    visible: false

                    PropertyAnimation {
                        id: start_yours_cards_5
                        target: yours_cards_5
                        properties: "x"
                        duration: 200
                        to: window.width / 2 + 45  // кінцеве положення карти по горизонталі
                        onFinished: {
                            yours_cards_5.source = cardManager.generate_your_card(window.page_cards);
                        }
                    }
                }
            }
        }
    }

    Component {
        id: thirdPage
        Page {
            Text {
                text: "Welcome add new card. Will be soon. Click Esc"
                font.family: "Arial Black"
                font.pixelSize: 20
                font.bold: true
                color: "#DAA520"
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: 160
            }
        }
    }

    Component {
        id: fourthPage
        Page {
            Image {
                id: main_bckImg
                source: "resources/images/promo.jpg"
                anchors.fill: parent
                fillMode: Image.PreserveAspectCrop
            }

            Text {
                text: "Download new table (*.png)"
                font.family: "Arial Black"
                font.pixelSize: 20
                font.bold: true
                color: "#DAA520"
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: -120
            }

            Image {
                id: back
                source: "resources/images/back.png"
                width: 50
                height: 50
                visible: true
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.margins: 10
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        stackView.pop();
                    }
                }
            }

            FileDialog {
                id: fileDialog
                title: "Choose a picture"
                nameFilters: ["Images (*.png)"]
                onAccepted: {
                    mainImage.source = fileDialog.file
                    cardManager.saveImageToResource(fileDialog.file, type_tables)
                    type_tables++
                }
            }

            Image {
                id: mainImage
                width: 160
                height: 120
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: 175
                fillMode: Image.PreserveAspectFit
            }

            Button {
                text: "Choose a picture"
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: -75
                onClicked: fileDialog.open()
            }
        }
    }



}
