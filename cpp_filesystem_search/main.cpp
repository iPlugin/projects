#include "headers/FileSearch.h"
#include "headers/ClassTimer.h"

#include <iostream>
#include <vector>
#include <thread>
#include <mutex>
#include <atomic>

using namespace std;


int main() {
    Timer time;

    string filename = "name";
    string path = "/";

    vector<string> paths;
    mutex paths_mutex;
    atomic<int> count_files(0);
    atomic<int> count_error(0);
    atomic<bool> stop_search(false);

    thread search_threads[8];

    for (int i = 0; i < 8; ++i){
        search_threads[i] = thread(searchFile, path, filename, ref(paths),
        ref(stop_search), ref(count_files), ref(count_error), ref(paths_mutex));
    }

    for (int i = 0; i < 8; ++i){
        search_threads[i].join();
    }

    lock_guard<mutex> lock(paths_mutex);
    cout << "\n=====================" << endl;
    for (const auto& path : paths){
        cout << "| Path: " << path << endl;
    }

    return 0;
}
