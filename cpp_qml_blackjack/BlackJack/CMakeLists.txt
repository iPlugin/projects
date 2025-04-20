cmake_minimum_required(VERSION 3.16)

project(BlackJack VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 6.5 REQUIRED COMPONENTS Quick)

qt_standard_project_setup(REQUIRES 6.5)

qt_add_executable(appBlackJack
    main.cpp
)

qt_add_qml_module(appBlackJack
    URI BlackJack
    VERSION 1.0
    QML_FILES
        Main.qml
    SOURCES
        cardmanager.h cardmanager.cpp
    RESOURCES
        resources/cards/1_0_0.png

        resources/cards/1_1_1.png
        resources/cards/1_1_2.png
        resources/cards/1_1_3.png
        resources/cards/1_1_4.png

        resources/cards/1_2_1.png
        resources/cards/1_2_2.png
        resources/cards/1_2_3.png
        resources/cards/1_2_4.png

        resources/cards/1_3_1.png
        resources/cards/1_3_2.png
        resources/cards/1_3_3.png
        resources/cards/1_3_4.png

        resources/cards/1_4_1.png
        resources/cards/1_4_2.png
        resources/cards/1_4_3.png
        resources/cards/1_4_4.png

        resources/cards/1_5_1.png
        resources/cards/1_5_2.png
        resources/cards/1_5_3.png
        resources/cards/1_5_4.png

        resources/cards/1_6_1.png
        resources/cards/1_6_2.png
        resources/cards/1_6_3.png
        resources/cards/1_6_4.png

        resources/cards/1_7_1.png
        resources/cards/1_7_2.png
        resources/cards/1_7_3.png
        resources/cards/1_7_4.png

        resources/cards/1_8_1.png
        resources/cards/1_8_2.png
        resources/cards/1_8_3.png
        resources/cards/1_8_4.png

        resources/cards/1_9_1.png
        resources/cards/1_9_2.png
        resources/cards/1_9_3.png
        resources/cards/1_9_4.png

        resources/cards/1_10_1.png
        resources/cards/1_10_2.png
        resources/cards/1_10_3.png
        resources/cards/1_10_4.png

        resources/cards/1_11_1.png
        resources/cards/1_11_2.png
        resources/cards/1_11_3.png
        resources/cards/1_11_4.png

        resources/cards/1_12_1.png
        resources/cards/1_12_2.png
        resources/cards/1_12_3.png
        resources/cards/1_12_4.png

        resources/cards/1_13_1.png
        resources/cards/1_13_2.png
        resources/cards/1_13_3.png
        resources/cards/1_13_4.png

        resources/cards/2_0_0.png

        resources/cards/2_1_1.png
        resources/cards/2_1_2.png
        resources/cards/2_1_3.png
        resources/cards/2_1_4.png

        resources/cards/2_2_1.png
        resources/cards/2_2_2.png
        resources/cards/2_2_3.png
        resources/cards/2_2_4.png

        resources/cards/2_3_1.png
        resources/cards/2_3_2.png
        resources/cards/2_3_3.png
        resources/cards/2_3_4.png

        resources/cards/2_4_1.png
        resources/cards/2_4_2.png
        resources/cards/2_4_3.png
        resources/cards/2_4_4.png

        resources/cards/2_5_1.png
        resources/cards/2_5_2.png
        resources/cards/2_5_3.png
        resources/cards/2_5_4.png

        resources/cards/2_6_1.png
        resources/cards/2_6_2.png
        resources/cards/2_6_3.png
        resources/cards/2_6_4.png

        resources/cards/2_7_1.png
        resources/cards/2_7_2.png
        resources/cards/2_7_3.png
        resources/cards/2_7_4.png

        resources/cards/2_8_1.png
        resources/cards/2_8_2.png
        resources/cards/2_8_3.png
        resources/cards/2_8_4.png

        resources/cards/2_9_1.png
        resources/cards/2_9_2.png
        resources/cards/2_9_3.png
        resources/cards/2_9_4.png

        resources/cards/2_10_1.png
        resources/cards/2_10_2.png
        resources/cards/2_10_3.png
        resources/cards/2_10_4.png

        resources/cards/2_11_1.png
        resources/cards/2_11_2.png
        resources/cards/2_11_3.png
        resources/cards/2_11_4.png

        resources/cards/2_12_1.png
        resources/cards/2_12_2.png
        resources/cards/2_12_3.png
        resources/cards/2_12_4.png

        resources/cards/2_13_1.png
        resources/cards/2_13_2.png
        resources/cards/2_13_3.png
        resources/cards/2_13_4.png

        resources/images/promo.jpg
        resources/images/plus.png
        resources/images/left.png
        resources/images/right.png
        resources/images/play-round.png

        resources/images/chip.png
        resources/images/10-chip.png
        resources/images/25-chip.png
        resources/images/50-chip.png
        resources/images/100-chip.png
        resources/images/hit.png
        resources/images/stand.png
        resources/images/return.png
        resources/images/joker.png
        resources/images/draw.png
        resources/images/lose.png
        resources/images/win.png
        resources/images/back.png

        resources/tables/1_table.png
        resources/tables/2_table.png
)

# Qt for iOS sets MACOSX_BUNDLE_GUI_IDENTIFIER automatically since Qt 6.1.
# If you are developing for iOS or macOS you should consider setting an
# explicit, fixed bundle identifier manually though.
set_target_properties(appBlackJack PROPERTIES
#    MACOSX_BUNDLE_GUI_IDENTIFIER com.example.appBlackJack
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
)

target_link_libraries(appBlackJack
    PRIVATE
        Qt6::Quick
)

include(GNUInstallDirs)
install(TARGETS appBlackJack
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
