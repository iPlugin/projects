#include "server.h"

int main()
{
    Server server;

    if (!server.run())
        std::cout << "Server: Finished own work" << std::endl;

    return 0;
}