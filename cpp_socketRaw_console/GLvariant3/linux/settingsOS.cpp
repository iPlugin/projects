#include "settingsOS.h"

bool settingIp(int &socketFD) {
    int one = 1;
    const int *val = &one;
    if (setsockopt(socketFD, IPPROTO_IP, IP_HDRINCL, val, sizeof(one)) >= 0) {
        return true;
    }
    return false;   
}