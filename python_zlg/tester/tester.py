import time
import random
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
        data = [0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7]
        super().TransmitCan(self.chn_handle, 0, 0x100, data, 8)
        # super().TransmitCan(self.chn_handle, 1, 0x12345678, data, 8)

        time.sleep(0.1)
        super().zcanlib.ClearBuffer(self.chn_handle)
        time.sleep(0.1)
        super().ReceiveAndPrintCan(self.chn_handle)

    def SendCanFromBLC(self, interval=0.1):
        for msg in self.BLFMsgs:
            super().TransmitCan(
                chn_handle=self.chn_handle,
                stdorext=msg.is_extended_id,
                id=msg.arbitration_id,
                data=msg.data,
                len=msg.dlc,
            )
            time.sleep(interval)

    def RampUpCPU(self):
        # TODO: must be implemented
        rampUpRequest = [0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7]
        # TODO: must be implemented
        rampUpResponseOK = [0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7]
        super().TransmitCan(self.chn_handle, 0, 0x100, rampUpRequest, 8)

        time.sleep(0.1)
        super().zcanlib.ClearBuffer(self.chn_handle)
        time.sleep(0.1)
        msgs = super().ReceiveCan(self.chn_handle)
        for msg in msgs:
            if msg.frame.data == rampUpResponseOK:
                return True
            else:
                return False

    def RampDownCPU(self):
        # TODO: must be implemented
        rampDownRequest = [0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7]
        # TODO: must be implemented
        rampDownResponseOK = [0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7]
        super().TransmitCan(self.chn_handle, 0, 0x100, rampDownRequest, 8)

        time.sleep(0.1)
        super().zcanlib.ClearBuffer(self.chn_handle)
        time.sleep(0.1)
        msgs = super().ReceiveCan(self.chn_handle)
        for msg in msgs:
            if msg.frame.data == rampDownResponseOK:
                return True
            else:
                return False

    # TODO: must be implemented
    def CanTransferNormalPackets(self):
        pass

    # TODO: must be implemented
    def IsCPULoadNormal(self):
        pass

    # TODO: must be implemented
    def ElasticityCheck(self):
        print("ELASTICITY CHECK:")
        if not self.CanTransferNormalPackets():
            print("Failed! Cannot transfer regular packets")
            return
        if not self.IsCPULoadNormal():
            print("Failed! CPU load unnormal")
            return

    def Scenario1(self):
        print("\nTESTING SCENARIO 1\n=================")
        msg = [0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7]
        dt = 0.010
        start = time.time()
        duration = 20
        print("RAMP LOAD ...")
        while dt >= 0.001:
            print(f"dt: {dt}")
            for _ in range(200):
                super().TransmitCan(self.chn_handle, 0, 0x100, msg, 8)
                time.sleep(dt)
            dt -= 0.001
        print("CONTINUOUS LOAD ...")
        while time.time() - start < duration:
            super().TransmitCan(self.chn_handle, 0, 0x100, msg, 8)
        print("Test duration: ", time.time() - start)

    def Scenario2(self):
        print("\nTESTING SCENARIO 2\n=================")
        msgs = []
        for _ in range(100):
            msg = [random.randint(0, 255) for _ in range(8)]
            msgs.append(msg)

        dt = 0.01
        start = time.time()
        duration = 10
        print("CYCLIC LOAD ...")
        while time.time() - start < duration:
            for msg in msgs:
                super().TransmitCan(self.chn_handle, 0, 0x100, msg, 8)
                time.sleep(dt)
        print("Test duration: ", time.time() - start)

    def Scenario3(self):
        print("\nTESTING SCENARIO 3\n=================")
        msgs = []
        for _ in range(100):
            msg = [random.randint(0, 255) for _ in range(8)]
            msgs.append(msg)

        dt = 0.01
        start = time.time()
        duration = 10
        print("RAMP CYCLIC LOAD ...")
        while dt >= 0.001:
            print(f"dt: {dt}")
            for msg in msgs:
                super().TransmitCan(self.chn_handle, 0, 0x100, msg, 8)
                time.sleep(dt)
            dt -= 0.001
        print("CONTINUOUS CYCLIC LOAD ...")
        while time.time() - start < duration:
            super().TransmitCan(self.chn_handle, 0, 0x100, msg, 8)
            time.sleep(dt)
        print("Test duration: ", time.time() - start)
