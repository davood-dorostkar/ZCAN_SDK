#include <iostream>
#include <CppUTest/CommandLineTestRunner.h>
#include "zlgcan.h"
#include "zcan.h"

int main(int argc, char** argv)
{
    Zcan* CAN = new Zcan;
    //CAN->CheckAllBuses();
    DEVICE_HANDLE dhandle = ZCAN_OpenDevice(12, 0, 0);
    CHANNEL_HANDLE chHandle = CAN->InitCan(dhandle);
    ZCAN_Transmit_Data* packet =  CAN->SendCanMessage(chHandle);
    ZCAN_Receive_Data* receive = CAN->ReceiveCanMessage(chHandle);
    std::cout << receive->frame.data << std::endl;
    //CommandLineTestRunner::RunAllTests(argc, argv);
    return 0;
}

