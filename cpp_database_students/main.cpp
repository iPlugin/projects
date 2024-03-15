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



    // CppTable table(5);
    // table.add_row("ID Name Surname Group Ticket");
    // table.add_row("1 Andriy Dutka 12PZ 123123");
    // table.add_row("2 Tania Ruzhman 43TR 321321");
    // table.add_row("3 Misha Trach 22KI 123456");
    // table.print_table();
    return 0;
}

/*

Пофіксити клас class_table він має отримувати
result result = txn.exec(query); і нормально
його обробляти

PGconnector::show()
main -> PGconnector - class_table -> main

Створити config file для 
- dbname
- user
- password
- host
- port


*/
// ! написати функцію fill_word