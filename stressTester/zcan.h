#pragma once
#include <iostream>
#include <cstdint>
#include <stdlib.h>
#include "zlgcan.h"

class ZCAN
{
public:
	void* InitCan(DEVICE_HANDLE CAN);
	ZCAN_Transmit_Data MakeFrame(const BYTE* data, int size);
	void CheckAllBuses();
	UINT SendSampleMessage(CHANNEL_HANDLE chHandle);
	ZCAN_Transmit_Data* SendMessage(CHANNEL_HANDLE chHandle, const BYTE* data);
	ZCAN_Transmit_Data* SendMessage(CHANNEL_HANDLE chHandle, const BYTE* data, int size);
	ZCAN_Receive_Data* ReceiveCanMessage(CHANNEL_HANDLE chHandle);
	void TestSendReceiveOnBus(int bus);
	void SendReceiveOnBus(int bus, const BYTE* data);
	void SendReceiveOnBus(int bus, const BYTE* data, int size);
};



