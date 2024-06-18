import QtQuick
import QtQuick.Window
import QtQuick.Controls

Window {
    property bool darkMode: false
    property bool openMenu: false

    id: winApp
    width: 800
    height: 540
    maximumWidth: 800
    minimumWidth: 800
    maximumHeight: 540
    minimumHeight: 540
    visible: true
    title: qsTr("FileServer")

    StackView {
        id: stackView
        anchors.fill: parent
        initialItem: p2_sockConnect


        Component {
            id: p1_main
            Page {
                background: Rectangle {
                    color: winApp.darkMode ? Qt.rgba(0.1294, 0.1451, 0.1608) : Qt.rgba(0.90196, 0.90588, 0.90980)
                }

                // Menu
                Button {
                    id: btnMenu

                    width: 24
                    height: 24

                    background: Image {
                        source: winApp.darkMode ? "qrc:iconsDark/assets/icons/dark/setting.png" : "qrc:iconsLight/assets/icons/light/setting.png"
                        fillMode: Image.PreserveAspectCrop
                    }

                    onClicked: menu.visible = menu.visible ? false : true
                }

                Column {
                    id: menu
                    visible: false

                    spacing: 10
                    width: 24
                    y: btnMenu.height + 10

                    Image {
                        id: imgSun
                        source: winApp.darkMode ? "qrc:iconsDark/assets/icons/dark/sun.png" : "qrc:iconsLight/assets/icons/light/sun.png"
                        width: 24
                        height: 24
                        MouseArea {
                            anchors.fill: parent
                            onClicked: winApp.darkMode = winApp.darkMode ? false : true
                        }
                    }

                    Image {
                        id: imgExit
                        source: winApp.darkMode ? "qrc:iconsDark/assets/icons/dark/exit.png" : "qrc:iconsLight/assets/icons/light/exit.png"
                        width: 24
                        height: 24
                        MouseArea {
                            anchors.fill: parent
                            onClicked: Qt.quit()
                        }
                    }
                }

                // Headers
                Label {
                    id: txtHead
                    text: "File Server"
                    font.family: "Ubuntu"
                    font.pixelSize: 30;
                    font.bold: true
                    color: winApp.darkMode ? Qt.rgba(0.95294, 0.43922, 0.21569) : Qt.rgba(0.1294, 0.1451, 0.1608)

                    anchors {
                        centerIn: parent
                        verticalCenterOffset: -40
                    }
                }

                Text {
                    id: txtInfo
                    text: "This server is designed to search\nfor a file on a remote host"
                    horizontalAlignment: Text.AlignHCenter
                    color: winApp.darkMode ? Qt.rgba(0.90196, 0.90588, 0.90980) : Qt.rgba(0.95294, 0.43922, 0.21569)

                    anchors {
                        centerIn: parent
                    }

                    font.family: "Ubuntu"
                    font.pixelSize: 15;
                    font.bold: true
                }

                Button {
                    id: btnStart

                    width: 150
                    height: 25

                    Text {
                        id: txtStart
                        text: "start"
                        font.family: "Ubuntu"
                        color: winApp.darkMode ? Qt.rgba(0.1294, 0.1451, 0.1608) : Qt.rgba(0.90196, 0.90588, 0.90980)
                        font.bold: true

                        horizontalAlignment: Text.AlignHCenter
                        anchors.centerIn: parent
                    }

                    anchors {
                        centerIn: parent
                        verticalCenterOffset: 40
                    }

                    background: Rectangle {
                        color: winApp.darkMode ? Qt.rgba(0.95294, 0.43922, 0.21569) : Qt.rgba(0.1294, 0.1451, 0.1608)
                        radius: 10
                    }
                    onClicked: stackView.push(p2_sockConnect)
                }
            }
        }
        Component {
            id: p2_sockConnect
            Page {
                background: Rectangle {
                    color: winApp.darkMode ? Qt.rgba(0.1294, 0.1451, 0.1608) : Qt.rgba(0.90196, 0.90588, 0.90980)
                }

                // Menu
                Button {
                    id: btnMenu

                    width: 24
                    height: 24

                    background: Image {
                        source: winApp.darkMode ? "qrc:iconsDark/assets/icons/dark/setting.png" : "qrc:iconsLight/assets/icons/light/setting.png"
                        fillMode: Image.PreserveAspectCrop
                    }

                    onClicked: menu.visible = menu.visible ? false : true
                }

                Column {
                    id: menu
                    visible: false

                    spacing: 10
                    width: 24
                    y: btnMenu.height + 10

                    Image {
                        id: imgSun
                        source: winApp.darkMode ? "qrc:iconsDark/assets/icons/dark/sun.png" : "qrc:iconsLight/assets/icons/light/sun.png"
                        width: 24
                        height: 24
                        MouseArea {
                            anchors.fill: parent
                            onClicked: winApp.darkMode = winApp.darkMode ? false : true
                        }
                    }

                    Image {
                        id: imgExit
                        source: winApp.darkMode ? "qrc:iconsDark/assets/icons/dark/exit.png" : "qrc:iconsLight/assets/icons/light/exit.png"
                        width: 24
                        height: 24
                        MouseArea {
                            anchors.fill: parent
                            onClicked: Qt.quit()
                        }
                    }
                }

                // Left side
                Column {
                    id: sideServer
                    spacing: 20
                    anchors {

                        left: parent.left
                        top: parent.top
                        topMargin: 30
                        bottom: parent.bottom
                    }
                    width: parent.width / 2

                    Label {
                        id: lblServerSide
                        text: "Server Side"
                        font.family: "Ubuntu"
                        font.pixelSize: 30;
                        font.bold: true
                        color: winApp.darkMode ? Qt.rgba(0.95294, 0.43922, 0.21569) : Qt.rgba(0.1294, 0.1451, 0.1608)

                        anchors.horizontalCenter: parent.horizontalCenter
                    }

                    Row {
                        spacing: 10
                        anchors.horizontalCenter: parent.horizontalCenter

                        Text {
                            text: "IP:"
                            font.bold: true
                            color: winApp.darkMode ? Qt.rgba(0.90196, 0.90588, 0.90980) : Qt.rgba(0.95294, 0.43922, 0.21569)
                        }

                        Text {
                            id: ipTxt
                            text: "127.0.0.1"
                            color: winApp.darkMode ? Qt.rgba(0.90196, 0.90588, 0.90980) : Qt.rgba(0.1294, 0.1451, 0.1608)
                            width: 150
                        }

                        Text {
                            text: "Port:"
                            font.bold: true
                            color: winApp.darkMode ? Qt.rgba(0.90196, 0.90588, 0.90980) : Qt.rgba(0.95294, 0.43922, 0.21569)
                        }
                        SpinBox {
                            id: s_portServer
                            from: 1
                            to: 65535
                            value: 1025
                            width: 100
                        }
                    }
////////////////////////////////////// SERVER
                    Button {
                        id: serverconnectButton
                        text: "Connect"
                        onClicked: {
                            if (server.serverSocket()) {
                                if (server.connectToServer(s_portServer.value)) {
                                    server.acceptServer()
                                }
                            }
                        }
                        anchors.horizontalCenter: parent.horizontalCenter
                    }

                    TextArea {
                        id: stextArea
                        text: ""
                        width: parent.width - 40
                        color: winApp.darkMode ? Qt.rgba(0.90196, 0.90588, 0.90980) : Qt.rgba(0.1294, 0.1451, 0.1608)
                        height: 150
                        placeholderText: "Output will be shown here..."
                        anchors.horizontalCenter: parent.horizontalCenter
                    }

                    // Connections {
                    //     target: server
                    //     function onMessageReceived(message) {
                    //         stextArea.text = message + "\n" + stextArea.text
                    //     }
                    // }
                }

                // Vertical line
                Rectangle {
                    width: 2
                    height: parent.height
                    color: "black"
                    x: parent.width / 2 - width / 2
                }

                // Right side
                Column {
                    id: sideClient
                    spacing: 20
                    anchors {
                        right: parent.right
                        top: parent.top
                        topMargin: 30
                        bottom: parent.bottom
                    }
                    width: parent.width / 2

                    Label {
                        id: lblClinetSide
                        text: "Client Side"
                        font.family: "Ubuntu"
                        font.pixelSize: 30;
                        font.bold: true
                        color: winApp.darkMode ? Qt.rgba(0.95294, 0.43922, 0.21569) : Qt.rgba(0.1294, 0.1451, 0.1608)

                        anchors.horizontalCenter: parent.horizontalCenter
                    }

                    Row {
                        spacing: 10
                        anchors.horizontalCenter: parent.horizontalCenter

                        Text {
                            text: "IP:"
                            font.bold: true
                            color: winApp.darkMode ? Qt.rgba(0.90196, 0.90588, 0.90980) : Qt.rgba(0.95294, 0.43922, 0.21569)
                        }

                        TextField {
                            id: c_ipInput
                            width: 150
                            height: 25
                            color: Qt.rgba(0.90196, 0.90588, 0.90980)
                            font.family: "Ubuntu"
                            placeholderText: "___.___.___.___"
                            // inputMethodHints: Qt.ImhDigitsOnly // not working :(
                        }

                        Text {
                            text: "Port:"
                            font.bold: true
                            color: winApp.darkMode ? Qt.rgba(0.90196, 0.90588, 0.90980) : Qt.rgba(0.95294, 0.43922, 0.21569)
                        }

                        SpinBox {
                            id: c_portInput
                            from: 1
                            to: 65535
                            value: 1025
                            width: 100
                        }
                    }

                    Row {
                        spacing: 10
                        anchors.horizontalCenter: parent.horizontalCenter
                        Text {
                            text: "File name"
                            font.bold: true
                            color: winApp.darkMode ? Qt.rgba(0.90196, 0.90588, 0.90980) : Qt.rgba(0.95294, 0.43922, 0.21569)
                        }

                        TextField {
                            id: filenameInput
                            placeholderText: "Filename"
                        }
                    }
////////////////////////////////////// CLIENT
                    Button {
                        id: clientconnectButton
                        text: "Connect"
                        onClicked: {
                            client.clientSocket()
                            client.connectToServer(c_ipInput.text, c_portInput.value)
                            client.send_msg_filename(filenameInput.text)
                            client.recv_msg()
                        }
                        anchors.horizontalCenter: parent.horizontalCenter
                    }

                    TextArea {
                        id: ctextArea
                        text: ""
                        width: parent.width - 40
                        color: winApp.darkMode ? Qt.rgba(0.90196, 0.90588, 0.90980) : Qt.rgba(0.1294, 0.1451, 0.1608)
                        height: 150
                        placeholderText: "Output will be shown here..."
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                    Connections {
                        target: client
                        function onMessageReceived(message) {
                            ctextArea.text = message + "\n" + ctextArea.text
                        }
                    }
                }
            }

            // Page {
                // title: "Page 2"
                // Colomn {
                    // id: clientInput
                    // anchors.centerIn: parent
                // }


                // Column {
                //     anchors.centerIn: parent

                //     Text {
                //         text: "This is Page 2"
                //         font.pointSize: 24
                //     }

                //     Button {
                //         text: "Go to Page 3"
                //         onClicked: stackView.push(page3)
                //     }

                //     Button {
                //         text: "Go back to Page 1"
                //         onClicked: stackView.pop()
                //     }
                // }
            // }
        }
    }
}






























