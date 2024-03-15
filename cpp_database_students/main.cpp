#include "headers/PGconnector.h"
using namespace std;

int main(){
    // Connect to Database
    const string dbname = "db_students";
    const string user = "postgres";
    const string password = "25051958";
    const string host = "localhost";
    const string port = "5432";

    PGconnector connector(dbname, user, password, host, port);

    // int id = 9;
    // string name = "Andriy";
    // string surname = "Dutka";
    // string group = "PZ-12";
    // string ticket = "172539";

    // connector.add(name, surname, group, ticket);
    // connector.rm(id);
    connector.show();

    return 0;
}

/*
! Проблема з виводом headers
Створити config

*/
// ! написати функцію fill_word