#ifndef CLASS_TABLE_H
#define CLASS_TABLE_H

#pragma once
#include <iostream>
#include <pqxx/pqxx>

class CppTable{
private:
    int max_row = 0;
    int columns = 5;
    int columns_size[5] = {0, 0, 0, 0, 0};
    std::string columns_names[5] =
        {"id", "name", "surname", "group_name", "ticket"};
    
    std::string fill_word(std::string word, const int &max_row);

    void result_columns_size(pqxx::result &result);

    std::string create_line();

public:
    void print_table(pqxx::result &result);
};

#endif