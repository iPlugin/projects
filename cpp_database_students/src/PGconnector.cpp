#include "../headers/PGconnector.h"
#include "../headers/class_table.h"

PGconnector::PGconnector(const std::string& dbname, const std::string& user, const std::string& password, const std::string& host, const std::string& port)
    : connection("dbname=" + dbname + " user=" + user + " password=" + password + " host=" + host + " port=" + port) {
    if (!connection.is_open()) {
        std::cerr << "Failed to connect to PostgreSQL" << std::endl;
    }
}

void PGconnector::add(const std::string& name, const std::string& surname, const std::string& group, const std::string& ticket) {
    try {
        pqxx::work txn(connection);
        std::string query = "insert into students (name, surname, group_name, ticket) values ('" + name + "', '" + surname + "', '" + group + "', '" + ticket + "')";

        txn.exec(query);
        txn.commit();

    } catch (const std::exception& e) {
        std::cerr << "Error executing SQL query: " << e.what() << std::endl;
    }
}

void PGconnector::rm(const int& id){
    try {
        pqxx::work txn(connection);
        std::string query = "delete from students where id = " + std::to_string(id);

        txn.exec(query);
        txn.commit();

    } catch (const std::exception& e) {
        std::cerr << "Error executing SQL query: " << e.what() << std::endl;
    }
}

void PGconnector::show(){
    try {
        pqxx::work txn(connection);
        std::string query = "select * from students";
        pqxx::result result = txn.exec(query);

        CppTable table;
        table.print_table(result);       

    } catch (const std::exception& e) {
        std::cerr << "Error executing SQL query: " << e.what() << std::endl;
    }
}