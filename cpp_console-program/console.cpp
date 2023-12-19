/*
g++ console.cpp -o main
./main
*/

#include <iostream>
#include <thread>
#include <chrono>
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

void func_ext(bool &active){
    active = false;
}

void show_menu(){    
    char opt_menu;
    bool active = true;


    do{
        clr_tml();
        cout << TAB << "-- PROGRAM CONSOLE --" << NEW;
        cout << NEW << TAB << "Select option:" << NEW;
        cout << "[1] Calculator" << NEW << "[2] Fibonacci" << NEW;
        cout << "[3] Calculator" << NEW << "[4] Calculator" << NEW;
        cout << "[5] Calculator" << NEW << "[7] Exit" << NEW;
        cout << NEW << "Option: ";
        cin >> opt_menu;

        switch (opt_menu){
        case '1':
            func_calc();
            break;
        case '2':
            func_fbnc();
            break;
        case '7':
            func_ext(active);
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