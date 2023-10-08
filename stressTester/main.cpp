#include <iostream>
#include <CppUTest/CommandLineTestRunner.h>
#include "zlgcan.h"
#include "zcan.h"

int main(int argc, char** argv)
{
    ZCAN* CAN = new ZCAN;

    CAN->CheckAllBuses();

    //CAN->TestSendReceiveOnBus(12);
    //CAN->TestSendReceiveOnBus(25);
    //CAN->TestSendReceiveOnBus(26);

    //BYTE data[] = {0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8};
    //CAN->SendReceiveOnBus(12, data);
    //CAN->SendReceiveOnBus(12, data, 8);
    //CommandLineTestRunner::RunAllTests(argc, argv);
    return 0;
}