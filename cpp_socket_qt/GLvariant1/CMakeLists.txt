cmake_minimum_required(VERSION 3.16)

project(socket_qml VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTORCC ON)

find_package(Qt6 6.4 REQUIRED COMPONENTS Quick Network)

qt_standard_project_setup()

qt_add_executable(appsocket_qml
    src/main.cpp
)

qt_add_qml_module(appsocket_qml
    URI socket_qml
    VERSION 1.0
    QML_FILES
        qml/Main.qml
    RESOURCES res/resources.qrc
        assets/icons/light/exit.png
        assets/icons/light/setting.png
        assets/icons/light/sun.png
        assets/icons/dark/exit.png
        assets/icons/dark/setting.png
        assets/icons/dark/sun.png
    SOURCES
        src/utils/server.h src/utils/server.cpp
        src/utils/client.h src/utils/client.cpp
    SOURCES include/packages.h
)

# Qt for iOS sets MACOSX_BUNDLE_GUI_IDENTIFIER automatically since Qt 6.1.
# If you are developing for iOS or macOS you should consider setting an
# explicit, fixed bundle identifier manually though.
set_target_properties(appsocket_qml PROPERTIES
#    MACOSX_BUNDLE_GUI_IDENTIFIER com.example.appsocket_qml
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
)

target_link_libraries(appsocket_qml
    PRIVATE Qt6::Quick
    Qt6::Network
)

include(GNUInstallDirs)
install(TARGETS appsocket_qml
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
