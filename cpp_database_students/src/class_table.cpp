#include "../headers/class_table.h"

std::string CppTable::fill_word(std::string word, const int &max_column){
    while (word.length() != max_column - 2){
        word += " ";
    }
    return word;
}

void CppTable::result_columns_size(pqxx::result &result){
    // Columns Size
    for (int i = 0; i < columns; i++){
        for (const auto& row : result){
            std::string word = row[columns_names[i]].as<std::string>();    
            if (word.length() + 2 > columns_size[i]){
                columns_size[i] = word.length() + 2;
            }
        }
    }
}

std::string CppTable::create_line(){
    // Print table - create line
    std::string line = "";
    for (int i = 0; i < columns; i++){
        line += "+";
        for (int j = 0; j < columns_size[i]; j++){
            line += "-";
        }
    } line += "+";
    return line;
}



void CppTable::print_table(pqxx::result &result){
    
    // Columns Size
    result_columns_size(result);

    // Print table - create line
    std::string line = create_line();

    // ! Fix it!
    // // Print table - headres
    // std::cout << line << std::endl;
    // std::cout << "| ";
    // for (int i = 0; i < columns_names->size(); i++){
    //     std::cout << fill_word(columns_names[i], columns_size[i]) << " ";
    // } std::cout << "\n" << line << std::endl;
    

    // Print table - values
    for (auto row : result){
        std::cout 
        << "| " << fill_word(row["id"].as<std::string>(), columns_size[0])
        << " | " << fill_word(row["name"].as<std::string>(), columns_size[1])
        << " | " << fill_word(row["surname"].as<std::string>(), columns_size[2])
        << " | " << fill_word(row["group_name"].as<std::string>(), columns_size[3])
        << " | " << fill_word(row["ticket"].as<std::string>(), columns_size[4])
        << " |" << std::endl;
    } std::cout << line << std::endl;

}