#include "zcan.h"

void* Zcan::InitCan(DEVICE_HANDLE CAN)
{
	ZCAN_CHANNEL_INIT_CONFIG cfg;
	memset(&cfg, 0, sizeof(cfg));
	cfg.can_type = TYPE_CAN;//CANFD | TYPE_CANFD
	cfg.can.filter = 0;
	cfg.can.mode = 0; //0: normal mode,1: listen-only mode 
	cfg.can.acc_code = 0;
	cfg.can.acc_mask = 0xffffffff;
	CHANNEL_HANDLE chHandle = ZCAN_InitCAN(CAN, 0, &cfg);
	return chHandle;
}

ZCAN_Transmit_Data* Zcan::SendCanMessage(CHANNEL_HANDLE chHandle)
{
	ZCAN_Transmit_Data frame; 
	memset(&frame, 0,sizeof(frame)); 
	frame.frame.can_id =MAKE_CAN_ID(0x100, 1, 0, 0); 
	frame.frame.can_dlc = 8;
	BYTE data[] = { 1, 2, 3, 4, 5, 6, 7, 8 };
	memcpy(frame.frame.data, data, sizeof(data)); 
    UINT sent = ZCAN_Transmit(chHandle, &frame, 8);
    std::cout << sent << std::endl;
	return &frame;
}

ZCAN_Receive_Data* Zcan::ReceiveCanMessage(CHANNEL_HANDLE chHandle)
{
    int nChnl = (unsigned int)chHandle & 0x000000FF;
    ZCAN_Receive_Data data[100] = {};
    int count = ZCAN_GetReceiveNum(chHandle, 0); // 0 CAN , 1 CANFD
    int rcount = ZCAN_Receive(chHandle, data, 100, 10);
    for (int i = 0; i < rcount; ++i)
    {
        std::cout << "CHNL: " << std::dec << nChnl <<
            "recv can id: 0x" << std::hex << data[i].frame.can_id << std::endl;
    }
    return data;
}

void Zcan::CheckAllBuses()
{
    for (int i = 1; i < 78; i++)
    {
        DEVICE_HANDLE dhandle = ZCAN_OpenDevice(i, 0, 0);
        if (INVALID_DEVICE_HANDLE != dhandle)
        {
            std::cout << "\nopened: " << dhandle << std::endl;
        }
        else continue;
        if (ZCAN_SetValue(dhandle, "0/baud_rate", "500000") != STATUS_OK)
        {
            std::cout << "failed to set baud rate" << std::endl;
        }

        CHANNEL_HANDLE chHandle = InitCan(dhandle);
        if (INVALID_CHANNEL_HANDLE == chHandle)
        {
            std::cout << "failed to init channel" << std::endl;
            continue;
        }

        if (ZCAN_StartCAN(chHandle) != STATUS_OK)
        {
            std::cout << "failed to start channel" << std::endl;
            continue;
        }
        ZCAN_Transmit_Data* frame = SendCanMessage(dhandle);

        if (ZCAN_Transmit(chHandle, frame, 1) != 1)
        {
            std::cout << "failed to transmit" << std::endl;
            continue;
        }
        ZCAN_CloseDevice(dhandle);
    }
}
