#pragma once
#include <iostream>
#include <cstdint>
#include <stdlib.h>
#include "zlgcan.h"

class Zcan
{
public:
	void* InitCan(DEVICE_HANDLE CAN);
	ZCAN_Transmit_Data* SendCanMessage(CHANNEL_HANDLE chHandle);
	void CheckAllBuses();
	ZCAN_Receive_Data* ReceiveCanMessage(CHANNEL_HANDLE chHandle);
	void TestSendReceiveOnBus(int bus);
};

