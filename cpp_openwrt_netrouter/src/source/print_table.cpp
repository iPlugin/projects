#include "print_table.h"

PrintTable::PrintTable(const std::vector<std::string>& headers)
    : headers(headers), column_widths(headers.size()){
    for (size_t i = 0; i < headers.size(); ++i){
        column_widths[i] = headers[i].length();
    }
}

PrintTable::~PrintTable(){}

void PrintTable::updateColumnWidths(const std::vector<std::string>& row){
    for (size_t i = 0; i < row.size(); ++i){
        column_widths[i] = std::max(column_widths[i], row[i].length());
    }
}

void PrintTable::addRow(const std::vector<std::string>& row){
    if (row.size() != headers.size()){
        throw std::invalid_argument("Row size does not match number of headers");
    }
    rows.push_back(row);
    updateColumnWidths(row);
}

void PrintTable::printSeparator() const{
    std::cout << '+';
    for (const auto& width : column_widths){
        std::cout << std::string(width + 2, '-') << '+';
    }
    std::cout << '\n';
}

void PrintTable::printRow(const std::vector<std::string>& row) const{
    std::cout << '|';
    for (size_t i = 0; i < row.size(); ++i){
        std::cout << ' ' << std::left << std::setw(column_widths[i]) << row[i] << " |";
    }
    std::cout << '\n';
}

void PrintTable::showTable() const{
    printSeparator();
    printRow(headers);
    printSeparator();
    for (const auto& row : rows){
        printRow(row);
    }
    printSeparator();
}