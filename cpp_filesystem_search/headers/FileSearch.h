#pragma once

#include <iostream>
#include <filesystem>
#include <vector>
#include <string>
#include <mutex>
#include <atomic>


void searchFile(const std::string& current_path, const std::string& target_filename,
    std::vector<std::string>& paths, std::atomic<bool>& stop_search, std::atomic<int>& count_files,
    std::atomic<int>& count_error, std::mutex& paths_mutex);