#ifndef PRINTTABLE_H
#define PRINTTABLE_H

#include <iostream>
#include <iomanip>
#include <vector>
#include <string>

class PrintTable{
private:
    std::vector<std::string> headers;
    std::vector<std::vector<std::string>> rows;
    std::vector<size_t> column_widths;

    void updateColumnWidths(const std::vector<std::string>& row);
    void printSeparator() const;
    void printRow(const std::vector<std::string>& row) const;

public:
    PrintTable(const std::vector<std::string>& headers);
    ~PrintTable();
    
    void addRow(const std::vector<std::string>& row);
    void showTable() const;
};

#endif // PRINTTABLE_H
