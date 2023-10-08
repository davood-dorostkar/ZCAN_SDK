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
    BYTE sampleData[8] = { 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8 };
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
    CHECK_FALSE(INVALID_DEVICE_HANDLE == CAN);
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

TEST(connectivity, 06_close_device)
{
    CHECK_EQUAL(STATUS_OK ,ZCAN_CloseDevice(CAN));
}

TEST_GROUP(sdk_send_receive)
{
    DEVICE_HANDLE CAN;
    CHANNEL_HANDLE chHandle;
    ZCAN zcan;
    int deviceID = 12;
    BYTE sampleData[8] = { 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8 };
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

TEST(sdk_send_receive, 01_make_frame)
{
    ZCAN_Transmit_Data frame = zcan.MakeFrame(sampleData, 8);
    CHECK_EQUAL(frame.frame.can_dlc, 8);
    MEMCMP_EQUAL(sampleData, frame.frame.data, 8);
}

TEST(sdk_send_receive, 02_send_sample)
{
    uint8_t baudStatus = ZCAN_SetValue(CAN, "0/baud_rate", "500000");
    chHandle = CAN;
    ZCAN_StartCAN(chHandle);
    CHECK_EQUAL(8, zcan.SendSampleMessage(chHandle));
}

TEST(sdk_send_receive, 03_transmit)
{
    uint8_t baudStatus = ZCAN_SetValue(CAN, "0/baud_rate", "500000");
    chHandle = CAN;
    ZCAN_StartCAN(chHandle);
    ZCAN_Transmit_Data frame = zcan.MakeFrame(sampleData, 8);
    CHECK_EQUAL(8, ZCAN_Transmit(chHandle, &frame, 8));
}

IGNORE_TEST(sdk_send_receive, 04_receive)
{
    uint8_t baudStatus = ZCAN_SetValue(CAN, "0/baud_rate", "1000000");
    chHandle = CAN;
    ZCAN_StartCAN(chHandle);
    ZCAN_Transmit_Data frame = zcan.MakeFrame(sampleData, 8);
    ZCAN_Transmit(chHandle, &frame, 8);
    ZCAN_Receive_Data receiveFrame;
    CHECK_EQUAL(STATUS_OK, ZCAN_Receive(chHandle, &receiveFrame, 8, 100));
}

TEST_GROUP(custom_transmission)
{
    DEVICE_HANDLE CAN;
    CHANNEL_HANDLE chHandle;
    ZCAN zcan;
    int deviceID = 12;
    BYTE sampleData[8] = { 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8 };
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

TEST(custom_transmission, 01_send_custom_packet)
{
    ZCAN_SetValue(CAN, "0/baud_rate", "500000");
    CHANNEL_HANDLE chHandle = zcan.InitCan(CAN);
    ZCAN_StartCAN(chHandle);
    BYTE customData[7] = { 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7 };
    CHECK_EQUAL(7, zcan.SendMessage(CAN, customData, 7));
}