#include <iostream>
#include <thread>
#include <chrono>
using namespace std;

void cls(){
    system("clear");
}

void sleep(int sec){
    cout << "\nWait " << sec << " seconds ...";
    cout.flush(); // я не розумію чому але мушу зробити таке
    // типу цей cout треба розбуферизувати
    this_thread::sleep_for(chrono::seconds(sec));
}

int factorial(int num){
    if (num == 0) return 0;
    if (num == 1) return 1;
    return num * factorial(num-1);
}


void func_one(){
    cls();
    cout << "\n[1]\tCreate a two-dimensional array" << endl;
    
    int arr_rows;
    int arr_cols;
    cout << "\nEnter rows for array: "; cin >> arr_rows;
    cout << "Enter cols for array: "; cin >> arr_cols;

    int **arr = new int *[arr_rows];
    for (int i = 0; i < arr_rows; i++){
        arr[i] = new int [arr_cols];
    }

    for (int i = 0; i < arr_rows; i++){
        for (int j = 0; j < arr_cols; j++){
            arr[i][j] = rand() % 10;
        }
    }
    cout << endl;

    for (int i = 0; i < arr_rows; i++){
        cout << "\t| ";
        for (int j = 0; j < arr_cols; j++){
            cout << arr[i][j] << " ";
        }
        cout << "|" << endl;
    }
    
    for (int i = 0; i < arr_rows; i++){
        delete[] arr[i];
    }
    delete[] arr;

    sleep(8);
}

void func_two(){
    cls();
    cout << "\n[2]\tFactorial formula" << endl;

    int number;
    cout << "\nEnter your number: "; cin >> number;
    cout << "\n\tYour result: " << factorial(number) << endl;

    sleep(3);
}

void func_three(){
    cls();
    cout << "Func three: wait 3 sec" << endl;
    sleep(3);
}

void func_four(){
    cls();
    cout << "Func four: wait 3 sec" << endl;
    sleep(3);
}

void func_five(){
    cls();
    cout << "Func five: wait 3 sec" << endl;
    sleep(3);
}


void func_options(int &option){
    switch (option){
        case 1:
            func_one();
            break;
        case 2:
            func_two();
            break;
        case 3:
            func_three();
            break;
        case 4:
            func_four();
            break;
        case 5:
            func_five();
            break;
    }
}


int main(){
    int option;

    while (option != 6){
        cls();

        option = 0;

        cout << "\n[0]\tWelcome to the console program" << endl;

        cout << "\nChoose number: \n";
        cout << "[1] Create a two-dimensional array\n";
        cout << "[2] Factorial formula\n";
        // [3] Калькулятор
        // [4] Вгадай число
        cout << "[6] Exit, stop program\n";

        cout << "\nOption: ";
        cin >> option;

        if (option >= 1 && option < 6){
            func_options(option);
        }
    }

    cls();
    cout << "\n\tGoodBye!" << endl;

    return 0;
}