#include <iostream>

#include "print_logo.h"
#include "trace_route.h"
#include "ascii_art.h"

using namespace std;

void printResult(PrintLogo& printer, Answer& result){
    if (result.isError){
        cout << "| The program ended with an error!" << endl;
    }
    else{
        cout << "| Total execution time: " << result.time << endl;
    }
}

int main(int argc, char* argv[]){
    PrintLogo printer;
    printer.addLogoByString(art_traceroute);
    // printer.addLogoByString(art_result); # | 🅁 🄴 🅂 🅄 🄻 🅃
    // printer.addLogoByString(art_usage); # | 🅄 🅂 🄰 🄶 🄴
    printer.printLogoByIndexFromString(0); // traceroute.txt

    Answer result;
    switch (argc){
        case 2: {
            TraceRoute traceroute(argv[1]);
            result = traceroute.start();
            printResult(printer, result);
            break;
        }
        case 3: {
            TraceRoute traceroute(argv[1], argv[2]);
            result = traceroute.start();
            printResult(printer, result);
            break;
        }
        default: {
            cerr << "| Usage:" << endl;
            cerr << "|  $ " << argv[0] << " [ FQDN ]" << endl;
            cerr << "|  $ " << argv[0] << " [ FQDN ] [ YOUR_NICKNAME ]" << endl;
            break;
        }
    }

    return 0;
}
