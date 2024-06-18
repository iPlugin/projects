#include "../includes/searcher.h"

using namespace std;


FileSearch::FileSearch(const fs::path& path){
    if (fs::exists(path) && fs::is_directory(path)){
        try {
            for (const auto& dir : fs::directory_iterator(path)){
                if (access(dir.path().c_str(), R_OK) == 0) { // Not sure i need it
                    dirs.push_back(dir);
                }
            }
        }
        catch (const fs::filesystem_error& e){
            cerr << "Error " << e.what() << endl;
        }
    }
    else{
        cerr << "Error: " << path << " is not a valid directory" << endl;
    }
    count_dirs = dirs.size();
}

string FileSearch::search(const string& filename){
    vector<thread> threads;
    vector<string> results(count_dirs);
    string return_result = "Not Found";

    for (int i = 0; i < count_dirs; i++) {
        threads.emplace_back([this, filename, i, &results]{
            results[i] = findFile(filename, i);
        });
    }

    for (thread& t : threads){
        t.join();
    }

    for (const string& result : results){
        if (result != "Not Found"){
            return_result = result;
        }
    }
    return return_result;
}

string FileSearch::findFile(const string& filename, int id_path){
    try{
        for (const auto& entry : fs::recursive_directory_iterator(dirs[id_path])){
            if (entry.is_regular_file() && entry.path().filename() == filename){
                return entry.path().string();
            }
        }
    }
    catch (filesystem::filesystem_error &e){
        // cerr << "Error" << endl;
    }
    return "Not Found";
}