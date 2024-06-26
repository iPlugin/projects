#include "client.h"

int main()
{
    Client client;

    if (!client.run())
        std::cout << "Client: Finished own work" << std::endl;

    return 0;
}