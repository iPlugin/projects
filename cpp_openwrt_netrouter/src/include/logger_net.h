#ifndef LOGGER_H
#define LOGGER_H

#include <iostream>
#include <fstream>
#include <string>
#include <ctime>


class Logger{
    public:
    enum LogLevel{
        INFO,
        WARNING,
        ERROR
    };
    
    Logger(const std::string& filename);
    ~Logger();
    
    void log(const std::string& message, LogLevel level);
    
    private:
    std::ofstream log_file;
    std::string getCurrentTime();
};

#endif // LOGGER_H