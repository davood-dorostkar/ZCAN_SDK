from pickletools import bytes1
from zlgcan import *
import cantools
from can.io import BLFReader
import time

DEVICE_LIST = [
    ZCAN_PCI5121,
    ZCAN_PCI9810,
    ZCAN_USBCAN1,
    ZCAN_USBCAN2,
    ZCAN_PCI9820,
    ZCAN_CAN232,
    ZCAN_PCI5110,
    ZCAN_CANLITE,
    ZCAN_ISA9620,
    ZCAN_ISA5420,
    ZCAN_PC104CAN,
    ZCAN_CANETUDP,
    ZCAN_CANETE,
    ZCAN_DNP9810,
    ZCAN_PCI9840,
    ZCAN_PC104CAN2,
    ZCAN_PCI9820I,
    ZCAN_CANETTCP,
    ZCAN_PCIE_9220,
    ZCAN_PCI5010U,
    ZCAN_USBCAN_E_U,
    ZCAN_USBCAN_2E_U,
    ZCAN_PCI5020U,
    ZCAN_EG20T_CAN,
    ZCAN_PCIE9221,
    ZCAN_WIFICAN_TCP,
    ZCAN_WIFICAN_UDP,
    ZCAN_PCIe9120,
    ZCAN_PCIe9110,
    ZCAN_PCIe9140,
    ZCAN_USBCAN_4E_U,
    ZCAN_CANDTU_200UR,
    ZCAN_CANDTU_MINI,
    ZCAN_USBCAN_8E_U,
    ZCAN_CANREPLAY,
    ZCAN_CANDTU_NET,
    ZCAN_CANDTU_100UR,
    ZCAN_PCIE_CANFD_100U,
    ZCAN_PCIE_CANFD_200U,
    ZCAN_PCIE_CANFD_400U,
    ZCAN_USBCANFD_200U,
    ZCAN_USBCANFD_100U,
    ZCAN_USBCANFD_MINI,
    ZCAN_CANFDCOM_100IE,
    ZCAN_CANSCOPE,
    ZCAN_CLOUD,
    ZCAN_CANDTU_NET_400,
    ZCAN_VIRTUAL_DEVICE,
]


class COM:
    BLFMsgs = []
    db = cantools.db.Database
    zcanlib = ZCAN()

    def __init__(self):
        pass

    def LoadBLF(self, filename):
        self.BLFMsgs = BLFReader(filename)
        print("BLF file loaded")
        return
        # alternative
        log = BLFReader(filename)
        for msg in log:
            self.BLFMsgs.append(msg)
            break

    def LoadDBC(self, filename):
        self.db = cantools.db.load_file(filename)

    def PrintBLFItem(self, msg):
        print(
            f"Tstamp: {msg.timestamp}",
            f"\tID: {msg.arbitration_id}",
            f"\tExtended: {msg.is_extended_id}",
            f"\tRemote Frame: {msg.is_remote_frame}",
            f"\tRX: {msg.is_rx}",
            f"\tDLC: {msg.dlc}",
            f" \tData: {'x'.join([f'{b:02X}' for b in msg.data])}",
            f"\tChannel: {msg.channel}",
        )

    def PrintAllBLF(self):
        for msg in self.BLFMsgs:
            self.PrintBLFItem(msg)

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
        for i in DEVICE_LIST:
            if i != ZCAN_CANSCOPE and i != ZCAN_CLOUD:
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

    def TransmitCan(self, chn_handle, stdorext, id, data, length):
        transmit_num = (length + 7) // 8  # Calculate the number of frames needed
        msgs = (ZCAN_Transmit_Data * transmit_num)()
        for i in range(transmit_num):
            msgs[i].transmit_type = 0
            msgs[i].frame.eff = 0
            if stdorext:
                msgs[i].frame.eff = 1
            msgs[i].frame.rtr = 0
            msgs[i].frame.can_id = id
            if length > 8:
                msgs[i].frame.can_dlc = 8
            else:
                msgs[i].frame.can_dlc = length
            for j in range(msgs[i].frame.can_dlc):
                msgs[i].frame.data[j] = data[i * 8 + j]
            length -= 8
        ret = self.zcanlib.Transmit(chn_handle, msgs, transmit_num)

    def ReceiveAndPrintCan(self, chn_handle):
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

    class Message:
        def __init__(self, frame_data):
            self.frame = COM.Frame(frame_data)

    class Frame:
        def __init__(self, data):
            self.data = data

    def ReceiveCan(self, chn_handle):
        rcv_num = self.zcanlib.GetReceiveNum(chn_handle, ZCAN_TYPE_CAN)
        # TODO: just for testing
        rcv_msg = [COM.Message([0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7])]
        return rcv_msg, rcv_num
        if rcv_num:
            rcv_msg, rcv_num = self.zcanlib.Receive(chn_handle, rcv_num)
        return rcv_msg, rcv_num
