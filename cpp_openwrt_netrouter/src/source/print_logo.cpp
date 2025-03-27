#include "print_logo.h"

void PrintLogo::printFromFile(const std::string& path) const{
    std::ifstream file(path);
    if (!file){
        throw std::invalid_argument("Error: Unable to open file");
    }

    std::string line;
    while (std::getline(file, line)){
        std::cout << line << std::endl;
    }
}

void PrintLogo::addLogoByPath(const std::string& path) {
    paths.push_back(path);
}

void PrintLogo::printLogoByIndexFromPath(size_t index) const {
    if (index >= paths.size()){
        throw std::invalid_argument("Error: Index out of range");
    }
    printFromFile(paths[index]);
}

void PrintLogo::addLogoByString(const std::string& logo) {
    logos.push_back(logo);
}

void PrintLogo::printLogoByIndexFromString(size_t index) const {
    if (index >= logos.size()) {
        throw std::invalid_argument("Error: Index out of range (string)");
    }
    std::cout << logos[index] << std::endl;
}