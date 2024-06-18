#ifndef FILESEARCH_H
#define FILESEARCH_H


#include <filesystem>
#include <vector>
#include <thread>
#include <chrono>
#include <iostream>
#include <unistd.h>

namespace fs = std::filesystem;


class FileSearch{
private:
    std::vector<fs::path> dirs;
    int count_dirs;

    std::string findFile(const std::string& filename, int id_path);

public:
    FileSearch(const fs::path& path);

    std::string search(const std::string& filename);
};


#endif // FILESEARCH_H
