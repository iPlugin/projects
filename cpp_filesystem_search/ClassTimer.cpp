#include "headers/ClassTimer.h"

using namespace std;


Timer::Timer(){
    start = chrono::high_resolution_clock::now();
}

Timer::~Timer(){
    end = chrono::high_resolution_clock::now();
    chrono::duration<float> duration = end - start;
    cout << "| Duration: " << duration.count() << "s" << endl;
    cout << "=====================" << endl;
}