#ifndef PROCESSMANAGER_H
#define PROCESSMANAGER_H

#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <dirent.h>
#include <unistd.h>
#include <algorithm>

struct ProcessInfo {
    int pid;
    std::string name;
    std::string state;
    int ppid;
};

class ProcessManager {
public:
    ProcessManager() = default;

    std::vector<ProcessInfo> getProcesses() const;
    void printProcesses() const;
};

#endif // PROCESSMANAGER_H
