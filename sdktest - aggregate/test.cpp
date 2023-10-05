#include <iostream>
#include "CppUTest/TestHarness.h"
#include "zlgcan.h"
#include "zcan.h"

TEST_GROUP(connectivity)
{
    DEVICE_HANDLE CAN;
    CHANNEL_HANDLE chHandle;
    Zcan zcan;
    void setup()
    {
        CAN = ZCAN_OpenDevice(ZCAN_USBCAN1, 0, 0);
    }
    void teardown()
    {
        CAN = INVALID_DEVICE_HANDLE;
        chHandle = INVALID_CHANNEL_HANDLE;
    }
};

TEST(connectivity, 01_can_open_device)
{
    CHECK_FALSE(INVALID_DEVICE_HANDLE==CAN);
}

TEST(connectivity, 02_check_online)
{
    uint8_t status = ZCAN_IsDeviceOnLine(CAN);
    CHECK_EQUAL(STATUS_ONLINE, status);
}

TEST(connectivity, 03_can_set_baudrate)
{
    uint8_t baudStatus = ZCAN_SetValue(CAN, "0/baud_rate", "1000000");
    CHECK_EQUAL(STATUS_OK, baudStatus);
}

TEST(connectivity, 04_can_init_device)
{
    uint8_t baudStatus = ZCAN_SetValue(CAN, "0/baud_rate", "1000000");
    CHANNEL_HANDLE channelHandle = zcan.InitCan(CAN);
    CHECK_EQUAL((void*)1, channelHandle);
}

TEST(connectivity, 05_can_start_can)
{
    uint8_t baudStatus = ZCAN_SetValue(CAN, "0/baud_rate", "1000000");
    chHandle = (void*)1;
    CHECK_EQUAL(STATUS_OK, ZCAN_StartCAN(chHandle));
}

TEST(connectivity, 06_can_transmit)
{
    uint8_t baudStatus = ZCAN_SetValue(CAN, "0/baud_rate", "1000000");
    chHandle = (void*)1;
    ZCAN_StartCAN(chHandle);
    ZCAN_Transmit_Data* frame = zcan.SendCanMessage(chHandle);
    CHECK_EQUAL(1, ZCAN_Transmit(chHandle, frame, 1));
}

TEST(connectivity, 07_can_receive)
{
    uint8_t baudStatus = ZCAN_SetValue(CAN, "0/baud_rate", "1000000");
    chHandle = (void*)1;
    ZCAN_StartCAN(chHandle);
    ZCAN_Transmit_Data* frame = zcan.SendCanMessage(chHandle);
    ZCAN_Transmit(chHandle, frame, 1);
    ZCAN_Receive_Data receiveFrame;
    CHECK_EQUAL(1, ZCAN_Receive(chHandle, &receiveFrame, 8));
}

TEST(connectivity, 08_can_close_device)
{
    CHECK_EQUAL(1 ,ZCAN_CloseDevice(CAN));
}