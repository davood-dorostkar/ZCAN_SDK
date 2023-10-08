#include <iostream>
#include "CppUTest/TestHarness.h"
#include "zlgcan.h"
#include "zcan.h"

TEST_GROUP(connectivity)
{
    DEVICE_HANDLE CAN;
    CHANNEL_HANDLE chHandle;
    ZCAN zcan;
    int deviceID = 12;
    void setup()
    {
        CAN = ZCAN_OpenDevice(deviceID, 0, 0);
    }
    void teardown()
    {
        ZCAN_CloseDevice(CAN); 
        CAN = INVALID_DEVICE_HANDLE;
        chHandle = INVALID_CHANNEL_HANDLE;
    }
};

TEST(connectivity, 01_open_device)
{
    CHECK_FALSE(INVALID_DEVICE_HANDLE==CAN);
}

IGNORE_TEST(connectivity, 02_check_online)
{
    uint8_t status = ZCAN_IsDeviceOnLine(CAN);
    CHECK_EQUAL(STATUS_ONLINE, status);
}

IGNORE_TEST(connectivity, 03_set_baudrate)
{
    uint8_t baudStatus = ZCAN_SetValue(CAN, "0/baud_rate", "500000");
    CHECK_EQUAL(STATUS_OK, baudStatus);
}

TEST(connectivity, 04_init_device)
{
    uint8_t baudStatus = ZCAN_SetValue(CAN, "0/baud_rate", "500000");
    CHANNEL_HANDLE channelHandle = zcan.InitCan(CAN);
    CHECK_EQUAL(CAN, channelHandle);
}

TEST(connectivity, 05_start_can)
{
    uint8_t baudStatus = ZCAN_SetValue(CAN, "0/baud_rate", "500000");
    chHandle = CAN;
    CHECK_EQUAL(STATUS_OK, ZCAN_StartCAN(chHandle));
}

TEST(connectivity, 06_make_frame)
{
    BYTE data[] = { 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8 };
    ZCAN_Transmit_Data frame = zcan.MakeFrame(data, 8);
    CHECK_EQUAL(frame.frame.can_dlc, 8);
    MEMCMP_EQUAL(data, frame.frame.data, 8);
}

TEST(connectivity, 07_send_sample)
{
    uint8_t baudStatus = ZCAN_SetValue(CAN, "0/baud_rate", "500000");
    chHandle = CAN;
    ZCAN_StartCAN(chHandle);
    UINT num = zcan.SendSampleMessage(chHandle);
    //CHECK_EQUAL(8, zcan.SendSampleMessage(chHandle));
}

//IGNORE_TEST(connectivity, 06_transmit)
//{
//    uint8_t baudStatus = ZCAN_SetValue(CAN, "0/baud_rate", "500000");
//    chHandle = CAN;
//    ZCAN_StartCAN(chHandle);
//    ZCAN_Transmit_Data* frame = zcan.SendSampleMessage(chHandle);
//    CHECK_EQUAL(1, ZCAN_Transmit(chHandle, frame, 1));
//}
//
//IGNORE_TEST(connectivity, 07_receive)
//{
//    uint8_t baudStatus = ZCAN_SetValue(CAN, "0/baud_rate", "1000000");
//    chHandle = (void*)1;
//    ZCAN_StartCAN(chHandle);
//    ZCAN_Transmit_Data* frame = zcan.SendSampleMessage(chHandle);
//    ZCAN_Transmit(chHandle, frame, 1);
//    ZCAN_Receive_Data receiveFrame;
//    CHECK_EQUAL(1, ZCAN_Receive(chHandle, &receiveFrame, 8));
//}
//
//IGNORE_TEST(connectivity, 08_close_device)
//{
//    CHECK_EQUAL(1 ,ZCAN_CloseDevice(CAN));
//}