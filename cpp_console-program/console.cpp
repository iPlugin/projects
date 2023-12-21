/*
g++ console.cpp -o main
./main
*/

#include <iostream>
#include <thread>
#include <chrono>
#include <ctime>
#define DEBUG
using namespace std;

const char NEW = '\n';
const char TAB = '\t';

void clr_tml(){
    system("clear");
}

void ext_but(){
    cout << NEW << "Waiting 10 sec... " << NEW;
    this_thread::sleep_for(std::chrono::seconds(10));
}

void func_calc(){
    clr_tml();

    int a, b;
    char opt_math;

    cout << TAB << "-- CALCULATOR --" << NEW;
    cout << NEW << TAB << "Enter number A, B and oporate" << NEW;
    cout << "A: "; cin >> a;
    cout << "B: "; cin >> b;
    cout << "Opt: "; cin >> opt_math;

    switch (opt_math){
    case '+':
        cout << NEW << TAB << "Result = " << a + b << NEW;
        break;
    case '-':
        cout << NEW << TAB << "Result = " << a - b << NEW;
        break;
    case '*':
        cout << NEW << TAB << "Result = " << a * b << NEW;
        break;
    case '/':
        cout << NEW << TAB << "Result = " << (float)a / b << NEW;
        break;
    
    default:
        cout << NEW << TAB << "[Error] Not found this command!" << NEW;
        break;
    }

    ext_but();
}

int func_fbnc_help(int a){
    if (a == 0)
        return 0;
    if (a == 1)
        return 1;
    return a * func_fbnc_help(a - 1);
}

void func_fbnc(){
    clr_tml();

    int a;

    cout << TAB << "-- Fibonacci --" << NEW;
    cout << NEW << TAB << "Enter number" << NEW;
    cout << "Number: "; cin >> a;
    int result = func_fbnc_help(a);
    cout << NEW << TAB << "Result = " << result << NEW;

    ext_but();
}

void func_game(){
    clr_tml();

    srand(time(NULL));
    int a, b = rand() %20;

    cout << TAB << "-- Game \"Guess number\" --" << NEW;
    cout << NEW << TAB << "I have a secret number 1-20" << NEW;
    
    do{
        cout << "Number: "; cin >> a;
        if (a == b){
            cout << NEW << TAB << "Yes! You are winner!" << NEW << NEW ;
        }
        else if (a > 20){
            cout << "Diapason 1-20" << NEW << NEW;
        }
        else if (a > b){
            cout << "My number is less" << NEW << NEW;
        }
        else{
            cout << "My number is greater" << NEW << NEW;
        }

    } while (a != b);

    ext_but();
}


void show_menu(){    
    char opt_menu;
    bool active = true;

    do{
        clr_tml();
        cout << TAB << "-- PROGRAM CONSOLE --" << NEW;
        cout << NEW << TAB << "Select option:" << NEW;
        cout << "[1] Calculator" << NEW << "[2] Fibonacci" << NEW;
        cout << "[3] Game" << NEW << "[4] Empty" << NEW;
        cout << "[5] Empty" << NEW << "[6] Empty" << NEW;
        cout << "[7] Empty" << NEW << "[8] Exit" << NEW;
        cout << NEW << "Option: ";
        cin >> opt_menu;

        switch (opt_menu){
        case '1':
            func_calc();
            break;
        case '2':
            func_fbnc();
            break;
        case '3':
            func_game();
            break;
        case '8':
            active = false;
            clr_tml();
            break;
        
        default:
            cout << NEW << TAB << "Not found this command!" << NEW;
            ext_but();
        }
        
    }while (active);   
}


int main(){
    setlocale(LC_ALL, "ua");

    clr_tml();

    show_menu();



    return 0;
}
