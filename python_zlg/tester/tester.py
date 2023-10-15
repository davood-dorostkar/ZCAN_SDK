import time
from zlgcan import *
from com import COM, DEVICE_LIST


class Tester(COM):
    dev_handle = INVALID_DEVICE_HANDLE
    chn_handle = INVALID_CHANNEL_HANDLE

    def __init__(self, bus, channel=0) -> None:
        self.dev_handle = super().OpenUsbCanOnBus(bus)
        if self.dev_handle == INVALID_DEVICE_HANDLE:
            return
        self.chn_handle = super().OpenChannel(self.dev_handle, channel)

    def End(self):
        super().zcanlib.ResetCAN(self.chn_handle)
        super().zcanlib.CloseDevice(self.dev_handle)
        print("Finish")

    def SampleSendReceiveOnBus(self):
        data = [0xF, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7]
        super().TransmitCan(self.chn_handle, 0, 0x100, data, 6)
        super().TransmitCan(self.chn_handle, 1, 0x12345678, data, 8)

        time.sleep(0.1)
        super().zcanlib.ClearBuffer(self.chn_handle)
        time.sleep(0.1)
        super().ReceiveCan(self.chn_handle)

        self.End()

    def SendCanFromBLC(self):
        for msg in self.BLFMsgs:
            self.TransmitCan(
                chn_handle=self.chn_handle,
                stdorext=msg.is_extended_id,
                id=msg.arbitration_id,
                data=msg.data,
                len=msg.dlc,
            )
            time.sleep(0.1)

        self.End()
