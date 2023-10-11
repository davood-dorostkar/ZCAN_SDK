from zlgcan import *
import time
import platform
import threading
import os
import cantools
from can.io import BLFReader
import matplotlib.pyplot as plt
import datetime
import sys


class COM:
    BLFMsgs = []
    db = cantools.db.Database
    zcanlib = ZCAN()

    def __init__(self):
        pass

    def LoadBLF(self, filename):
        log = BLFReader(filename)
        for msg in log:
            self.BLFMsgs.append(msg)
            break
        print("BLF file loaded")

    def LoadDBC(self, filename):
        self.db = cantools.db.load_file(filename)

    def OpenUsbCanII(self):
        dhandle = self.zcanlib.OpenDevice(ZCAN_USBCAN2, 0, 0)
        if dhandle == INVALID_DEVICE_HANDLE:
            print("failed to open device")
            exit(0)
        print("device handle: " + dhandle)
        return dhandle

    def OpenUsbCanOnBus(self, bus):
        dhandle = self.zcanlib.OpenDevice(bus, 0, 0)
        if dhandle == INVALID_DEVICE_HANDLE:
            print("bus open failed: " + str(bus))
            return INVALID_DEVICE_HANDLE
        print("opened device handle: " + str(hex(dhandle)))
        return dhandle

    def SearchAllBuses(self):
        for i in range(1, 48):
            if i == 46 or i == 45:
                continue
            self.OpenUsbCanOnBus(i)

    def OpenChannel(self, dev_handle, channel):
        chn_init_cfg = ZCAN_CHANNEL_INIT_CONFIG()
        chn_init_cfg.can_type = ZCAN_TYPE_CAN
        chn_init_cfg.config.can.acc_mode = 0
        chn_init_cfg.config.can.acc_mask = 0xFFFFFFFF
        chn_init_cfg.config.can.timing0 = 0
        chn_init_cfg.config.can.timing1 = 28
        chn_handle = self.zcanlib.InitCAN(dev_handle, channel, chn_init_cfg)
        if chn_handle is None:
            return None
        self.zcanlib.StartCAN(chn_handle)
        return chn_handle

    def TransmitCan(self, chn_handle, stdorext, id, data, len):
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
        ret = self.zcanlib.Transmit(chn_handle, msgs, transmit_num)

    def ReceiveCan(self, chn_handle):
        rcv_num = self.zcanlib.GetReceiveNum(chn_handle, ZCAN_TYPE_CAN)
        if rcv_num:
            print("Receive CAN message number: %d" % rcv_num)
            rcv_msg, rcv_num = self.zcanlib.Receive(chn_handle, rcv_num)
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

    def SampleSendReceiveOnBus(self, bus):
        dev_handle = self.OpenUsbCanOnBus(bus)
        if dev_handle == INVALID_DEVICE_HANDLE:
            return
        chn0_handle = self.OpenChannel(dev_handle, 0)

        data = [0, 1, 2, 3, 4, 5, 6, 0xFF]
        self.TransmitCan(chn0_handle, 0, 0x100, data, 6)
        self.TransmitCan(chn0_handle, 1, 0x12345678, data, 8)
        data[0] = data[0] + 1
        time.sleep(0.1)

        self.zcanlib.ClearBuffer(chn0_handle)
        time.sleep(1)
        self.ReceiveCan(chn0_handle)

        self.zcanlib.ResetCAN(chn0_handle)
        self.zcanlib.CloseDevice(dev_handle)
        print("Finish")

    def SendCanFromBLC(self, bus):
        dev_handle = self.OpenUsbCanOnBus(bus)
        if dev_handle == INVALID_DEVICE_HANDLE:
            return
        chn0_handle = self.OpenChannel(dev_handle, 0)

        for msg in self.BLFMsgs:
            self.TransmitCan(
                chn_handle=chn0_handle,
                stdorext=msg.is_extended_id,
                id=msg.arbitration_id,
                data=msg.data,
                len=msg.dlc,
            )
            time.sleep(0.1)

        self.zcanlib.ResetCAN(chn0_handle)
        self.zcanlib.CloseDevice(dev_handle)
        print("Finish")


if __name__ == "__main__":
    if platform.python_version() >= "3.8.0":
        os.add_dll_directory(os.getcwd())

    com = COM()
    bus = 0xC
    # bus = 0x19
    # bus = 0x1A
    # bus = 0x24
    # bus = 0xDF
    # bus = ZCAN_VIRTUAL_DEVICE

    if len(sys.argv) != 2:
        print("To replay BLF file: python main.py <sample.blf>\n")
        print("Running default operation\n")

        # com.SearchAllBuses()
        # dev_handle = com.OpenUsbCanII()
        # com.SampleSendReceiveOnBus(bus)

    else:
        file = sys.argv[1]
        com.LoadBLF(file)
        com.SendCanFromBLC(bus)
