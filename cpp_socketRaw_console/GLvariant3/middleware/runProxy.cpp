/*                                          creator by iPlugin ©
██████╗ ██████╗  █████╗ ██╗  ██╗██╗   ██╗   ██████╗██╗██████╗ ███████╗
██╔══██╗██╔══██╗██╔══██╗╚██╗██╔╝╚██╗ ██╔╝  ██╔════╝██║██╔══██╗██╔════╝
██████╔╝██████╔╝██║  ██║ ╚███╔╝  ╚████╔╝   ╚█████╗ ██║██║  ██║█████╗
██╔═══╝ ██╔══██╗██║  ██║ ██╔██╗   ╚██╔╝     ╚═══██╗██║██║  ██║██╔══╝
██║     ██║  ██║╚█████╔╝██╔╝╚██╗   ██║     ██████╔╝██║██████╔╝███████╗
╚═╝     ╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝   ╚═╝     ╚═════╝ ╚═╝╚═════╝ ╚══════╝
*/

#include "../includes/proxy.h"


int main(int argc, char* argv[], char *envp[]){
    srand(time(NULL));
    // checking for correctness
    if (!(check_args(argc, argv, envp, 5)))
        return 1;

    // PROXY
    Proxy proxy("logs/logProxy.log");
    if (!(proxy.startProxy(argv)))
        return 1;
    
    if (!(proxy.recvPacket()))
        return 1;

    return 0;
}