#include "audio.h"
// #include <stdexcept>
#include <iostream>
#include <chrono>

bool playMusic(std::atomic<bool>* stopMusic) {
    SDL_Init(SDL_INIT_AUDIO) < 0;

    if (Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 4096) < 0) {
        SDL_Quit();
    }

    Mix_Music* bgm = Mix_LoadMUS("audio/audio_file.mp3");
    if (bgm == nullptr) {
        Mix_CloseAudio();
        SDL_Quit();
    }

    Mix_PlayMusic(bgm, -1);

    auto start_time = std::chrono::steady_clock::now();
    while (!(*stopMusic)) {
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }

    auto end_time = start_time + std::chrono::seconds(20);
    while (std::chrono::steady_clock::now() < end_time) {
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }

    Mix_FadeOutMusic(500);
    while (Mix_FadingMusic() != MIX_NO_FADING) {
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }

    Mix_HaltMusic();
    Mix_FreeMusic(bgm);
    Mix_CloseAudio();
    SDL_Quit();

    return true;
}
