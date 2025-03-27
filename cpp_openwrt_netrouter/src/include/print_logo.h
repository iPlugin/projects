#ifndef PRINTLOGO_H
#define PRINTLOGO_H

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

class PrintLogo{
private:
    std::vector<std::string> paths;
    std::vector<std::string> logos;
    void printFromFile(const std::string& path) const;

public:
    PrintLogo(){}

    void addLogoByPath(const std::string& path);
    void printLogoByIndexFromPath(size_t index) const;

    void addLogoByString(const std::string& logo);
    void printLogoByIndexFromString(size_t index) const;
};

#endif // PRINTLOGO_H
