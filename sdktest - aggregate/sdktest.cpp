#include <iostream>
#include <CppUTest/CommandLineTestRunner.h>
#include "zlgcan.h"
#include "zcan.h"

int main(int argc, char** argv)
{
    Zcan* CAN = new Zcan;
    //CAN->CheckAllBuses();
    CAN->TestSendReceiveOnBus(12);
    CAN->TestSendReceiveOnBus(25);
    CAN->TestSendReceiveOnBus(26);
    //CommandLineTestRunner::RunAllTests(argc, argv);
    return 0;
}

