/*                                                  creator by iPlugin ©
 ██████╗███████╗██████╗ ██╗   ██╗███████╗██████╗    ██████╗██╗██████╗ ███████╗
██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗  ██╔════╝██║██╔══██╗██╔════╝
╚█████╗ █████╗  ██████╔╝╚██╗ ██╔╝█████╗  ██████╔╝  ╚█████╗ ██║██║  ██║█████╗  
 ╚═══██╗██╔══╝  ██╔══██╗ ╚████╔╝ ██╔══╝  ██╔══██╗   ╚═══██╗██║██║  ██║██╔══╝  
██████╔╝███████╗██║  ██║  ╚██╔╝  ███████╗██║  ██║  ██████╔╝██║██████╔╝███████╗
╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝  ╚═════╝ ╚═╝╚═════╝ ╚══════╝
*/

#include "../includes/server.h"


int main(int argc, char* argv[], char *envp[]) {
    srand(time(NULL));
    // checking for correctness
    if (!(check_args(argc, argv, envp, 3)))
        return 1;

    // SERVER
    Server server("logs/logServer.log");
    if (!(server.startServer(argv)))
        return 1;
    
    if (!(server.recvPacket()))
        return 1;

    return 0;
}