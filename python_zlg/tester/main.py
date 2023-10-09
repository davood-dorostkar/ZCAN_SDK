from zlgcan import *
import time
import platform
import threading

zcanlib = ZCAN()


def open_usbcanII():
    dhandle = zcanlib.OpenDevice(ZCAN_USBCAN2, 0, 0)
    if dhandle == INVALID_DEVICE_HANDLE:
        print("failed to open device")
        exit(0)
    print("device handle: " + dhandle)
    return dhandle


def open_usbcan_on_bus(bus):
    dhandle = zcanlib.OpenDevice(bus, 0, 0)
    if dhandle == INVALID_DEVICE_HANDLE:
        return
    print("device handle: " + str(hex(dhandle)))
    return dhandle


def search_all_buses():
    for i in range(1, 48):
        if i == 46 or i == 45:
            continue
        open_usbcan_on_bus(i)


def open_channel(dev_handle, channel):
    chn_init_cfg = ZCAN_CHANNEL_INIT_CONFIG()
    chn_init_cfg.can_type = ZCAN_TYPE_CAN
    chn_init_cfg.config.can.acc_mode = 0
    chn_init_cfg.config.can.acc_mask = 0xFFFFFFFF
    chn_init_cfg.config.can.timing0 = 0
    chn_init_cfg.config.can.timing1 = 28
    chn_handle = zcanlib.InitCAN(dev_handle, channel, chn_init_cfg)
    if chn_handle is None:
        return None
    zcanlib.StartCAN(chn_handle)
    return chn_handle


def transmit_can(chn_handle, stdorext, id, data, len):
    transmit_num = 1
    msgs = (ZCAN_Transmit_Data * transmit_num)()
    for i in range(transmit_num):
        msgs[i].transmit_type = 0
        msgs[i].frame.eff = 0
        if stdorext:
            msgs[i].frame.eff = 1
        msgs[i].frame.rtr = 0
        msgs[i].frame.can_id = id
        msgs[i].frame.can_dlc = len
        for j in range(msgs[i].frame.can_dlc):
            msgs[i].frame.data[j] = data[j]
    ret = zcanlib.Transmit(chn_handle, msgs, transmit_num)


def receive_can(chn_handle):
    rcv_num = zcanlib.GetReceiveNum(chn_handle, ZCAN_TYPE_CAN)
    if rcv_num:
        print("Receive CAN message number: %d" % rcv_num)
        rcv_msg, rcv_num = zcanlib.Receive(chn_handle, rcv_num)
        for i in range(rcv_num):
            print(
                "[%d]:ts:%d, id:0x%x, dlc:%d, eff:%d, rtr:%d, data:%s"
                % (
                    i,
                    rcv_msg[i],
                    rcv_msg[i].timestamp,
                    rcv_msg[i].frame.can_id,
                    rcv_msg[i].frame.dlc,
                    rcv_msg[i].frame.eff,
                    rcv_msg[i].frame.rtr,
                    "".join(
                        hex(
                            rcv_msg[i].frame.data[j][2:] + " "
                            for j in range(rcv_msg[i].frame.can_dlc)
                        )
                    ),
                )
            )


def sample_send_receive_on_bus(bus):
    dev_handle = open_usbcan_on_bus(bus)
    chn0_handle = open_channel(dev_handle, 0)

    data = [0, 1, 2, 3, 4, 5, 6, 0xFF]
    for i in range(2):
        transmit_can(chn0_handle, 0, 0x100, data, 6)
        transmit_can(chn0_handle, 1, 0x12345678, data, 8)
        data[0] = data[0] + 1
        time.sleep(0.1)

    zcanlib.ClearBuffer(chn0_handle)
    time.sleep(1)
    receive_can(chn0_handle)

    zcanlib.ResetCAN(chn0_handle)
    zcanlib.CloseDevice(dev_handle)
    print("Finish")


if __name__ == "__main__":
    if platform.python_version() >= "3.8.0":
        import os

        os.add_dll_directory(os.getcwd())
    # search_all_buses()
    # dev_handle = open_usbcanII()
    sample_send_receive_on_bus(0xC0000)
    sample_send_receive_on_bus(0x190000)
    sample_send_receive_on_bus(0x1A0000)
    sample_send_receive_on_bus(0x240000)
    sample_send_receive_on_bus(0x2F0000)
