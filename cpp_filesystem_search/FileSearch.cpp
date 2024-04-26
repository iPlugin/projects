#include "headers/FileSearch.h"

using namespace std;

// Забрати цю всю хуйню і передати структурою
void searchFile(const string& current_path, const string& filename, vector<string>& paths, atomic<bool>& stop_search, atomic<int>& count_files, atomic<int>& count_error, mutex& paths_mutex){
    for(const auto& file:filesystem::directory_iterator(current_path)){
        if(stop_search){
            return;
        }
        try{
            // це я собі спрощував життя + там і так багато папок status: private
            if (file.path() == "/sys" || file.path() == "/proc" || file.path() == "/dev") continue;
            if (filesystem::is_directory(file)){
                searchFile(file.path().string(), filename, paths, stop_search, count_files, count_error, paths_mutex);
            }
            else if (file.path().filename() == filename){
                lock_guard<mutex> lock(paths_mutex);
                paths.push_back(file.path().string());
                stop_search = true;
            }
            else{
                ++count_files;
            }
        } 
        catch (const filesystem::filesystem_error& ex){
            cerr << "Error №: " << ++count_error << " - " << file.path().string() << " - " << ex.what() << endl;
        }
    }
}
