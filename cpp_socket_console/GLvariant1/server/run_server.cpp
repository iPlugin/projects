/*

    ███████╗██╗██╗     ███████╗   ██████╗███████╗██████╗ ██╗   ██╗███████╗██████╗
    ██╔════╝██║██║     ██╔════╝  ██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
    █████╗  ██║██║     █████╗    ╚█████╗ █████╗  ██████╔╝╚██╗ ██╔╝█████╗  ██████╔╝
    ██╔══╝  ██║██║     ██╔══╝     ╚═══██╗██╔══╝  ██╔══██╗ ╚████╔╝ ██╔══╝  ██╔══██╗
    ██║     ██║███████╗███████╗  ██████╔╝███████╗██║  ██║  ╚██╔╝  ███████╗██║  ██║
    ╚═╝     ╚═╝╚══════╝╚══════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

                                                        Create by iPlugin © 
               ██████████
              ████████████
              ██        ██              MIT License
              ██▄▄▄▄▄▄▄▄▄█              
              ██▀███ ███▀█              Copyright (c) 2024 iPlugin
█             ▀█        █▀              
 █              ██                      Permission is hereby granted, free of 
██                  █                   charge, to any person obtaining a copy
█▄            ████ ██  ████             of this software and associated
 ▄███████████████  ██  ██████           documentation files (the "Software"), to
    █████████████  ██  █████████        deal in the Software without restriction,
             ████  ██ █████  ███        including without limitation the rights to
              ███  ██ █████  ███        use, copy, modify, merge, publish,
              ███     █████████         distribute, sublicense, and/or sell copies
              ██     ████████▀          of the Software, and to permit persons to
                ██████████              whom the Software is furnished to do so,
                ██████████              subject to the following conditions:
                 ████████               
                  ██████████▄▄          The above copyright notice and this
                    █████████▀          permission notice shall be included in all
                     ████  ███          copies or substantial portions of the
                    ▄████▄  ██          Software.
                    ██████   ▀
                    ▀▄▄▄▄▀

*/

#include "../includes/server.h"
#include <charconv> // Потрібно для std::from_chars

int main(int argc, char* argv[]){
    Server server("logs/logServer.log");             //  ▄   ▄
                                                 //  ▄█▄ █▀█▀█ ▄█▄
    if(!server.parseArgs(argc, argv)){           // ▀▀████▄█▄████▀▀
        return 1;                                    //  ▀█▀█▀
    } // тут не має бути

    if (!server.serverSocket()){ // тут не має бути
        return 1;
    }

    // int port = stoi(argv[1]);
    // int port = std::from_chars();
    int port;
    auto [ptr, ec] = std::from_chars(argv[1], argv[1] + std::strlen(argv[1]), port);
    if (!server.connectToServer(port)){ // тут не має бути
        return 1;
    }

    if (!server.listenServer()){ // тут не має бути
        return 1;
    }
    
    if (!server.acceptServer()){ // тут не має бути
        return 1;
    }

// Part 2
    // Get filename
    string responce = server.recvMessage();
    if (responce.empty()){return 1;}


    Message pkg;
    
    // Send Intro to client
    extern string intro;
    pkg.type = Message::Type::INTRO;
    strcpy(pkg.msg.server_introduced.intro, intro.c_str());
    if (!server.sendMessage(pkg)){return 1;}


    thread threads_result([&server, &responce](){server.sendResult(server,responce);});
    thread status_work([&server](){server.notification(server);});

    threads_result.join();
    status_work.join();

    return 0;
}                 


//                        ▐███████▌
//                        ▐░░░░░░░▌
//                  ▄▀▀▀█ ▐░▀▀▄▀▀░▌ █▀▀▀▄
//                  ▌▌▌▌▐ ▄▌░▄▄▄░▐▄ ▌▐▐▐▐