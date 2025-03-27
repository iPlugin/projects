#include "logger_net.h"


Logger::Logger(const std::string& filename)
    : log_file(filename, std::ios::app){}

Logger::~Logger(){
    if (log_file.is_open()){
        log_file.close();
    }
}

void Logger::log(const std::string& message, LogLevel level){
    std::string level_str;
    switch (level){
        case INFO:
            level_str = "[ INFO ] ";
            break;
        case WARNING:
            level_str = "[WARNING] ";
            break;
        case ERROR:
            level_str = "[ ERROR ] ";
            break;
    }

    std::string log_entry = getCurrentTime() + " " + level_str + "\t" + message;
    if (log_file.is_open()){
        log_file << log_entry << std::endl;
        log_file.flush();
    }
}

std::string Logger::getCurrentTime(){
    std::time_t now = std::time(nullptr);
    char buf[20];
    std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", std::localtime(&now));
    return std::string(buf);
}
