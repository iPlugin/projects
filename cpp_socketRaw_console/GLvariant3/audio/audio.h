#ifndef AUDIO_H
#define AUDIO_H

#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>
#include <thread>
#include <atomic>

// 01:06 ━━━━⬤─────── 04:05  Era - Ameno
bool playMusic(std::atomic<bool>* stopMusic);

#endif // AUDIO_H 