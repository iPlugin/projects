#include "../../include/process/ProcessManager.h"

std::vector<ProcessInfo> ProcessManager::getProcesses() const {
    std::vector<ProcessInfo> processes;
    DIR* procDir = opendir("/proc");
    if (!procDir) {
        std::cerr << "Could not open /proc directory" << std::endl;
        return processes;
    }

    struct dirent* entry;
    while ((entry = readdir(procDir)) != nullptr) {
        if (entry->d_type == DT_DIR) {
            std::string dirName = entry->d_name;
            if (std::all_of(dirName.begin(), dirName.end(), ::isdigit)) {
                int pid = std::stoi(dirName);
                std::string statFilePath = "/proc/" + dirName + "/stat";
                std::ifstream statFile(statFilePath);
                if (statFile.is_open()) {
                    ProcessInfo process;
                    std::string line;
                    std::getline(statFile, line);
                    std::istringstream iss(line);
                    iss >> process.pid;
                    iss >> process.name;
                    iss >> process.state;
                    iss >> process.ppid;

                    processes.push_back(process);
                }
            }
        }
    }
    closedir(procDir);
    return processes;
}

void ProcessManager::printProcesses() const {
    std::vector<ProcessInfo> processes = getProcesses();
    for (const auto& process : processes) {
        std::cout << "PID: " << process.pid << ", Name: " << process.name 
                  << ", State: " << process.state << ", PPID: " << process.ppid << std::endl;
    }
}
