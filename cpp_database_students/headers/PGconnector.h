#ifndef PGCONNECTION9_H
#define PGCONNECTION_H

#pragma once
#include <pqxx/pqxx>
#include <iostream>

class PGconnector {
private:
    pqxx::connection connection;

public:
    PGconnector(const std::string& dbname, const std::string& user, const std::string& password, const std::string& host, const std::string& port);

    void add(const std::string& name, const std::string& surname, const std::string& group, const std::string& ticket);

    void rm(const int& id);

    void show();

};

#endif // PGCONNECTION_H