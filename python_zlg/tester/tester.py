import time
import random

from matplotlib.pyplot import flag
from zlgcan import *
from com import COM, DEVICE_LIST


class Tester(COM):
    dev_handle = INVALID_DEVICE_HANDLE
    chn_handle = INVALID_CHANNEL_HANDLE
    packetsLog = {}

    def __init__(self, bus, channel=0) -> None:
        self.dev_handle = super().OpenUsbCanOnBus(bus)
        if self.dev_handle == INVALID_DEVICE_HANDLE:
            return
        self.chn_handle = super().OpenChannel(self.dev_handle, channel)

    def End(self):
        super().zcanlib.ResetCAN(self.chn_handle)
        super().zcanlib.CloseDevice(self.dev_handle)
        print("Finish")

    def SampleSendReceive(self):
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
        msgs, _ = super().ReceiveCan(self.chn_handle)
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
        msgs, _ = super().ReceiveCan(self.chn_handle)
        for msg in msgs:
            if msg.frame.data == rampDownResponseOK:
                return True
            else:
                return False

    # TODO: must be implemented
    def CanTransferNormalPackets(self):
        return True

    # TODO: must be implemented
    def IsCPULoadNormal(self):
        return True

    # TODO: must be implemented
    def ElasticityCheck(self):
        print("\nELASTICITY CHECK:\n=================")
        if not self.CanTransferNormalPackets():
            print("Failed! Cannot transfer regular packets")
            return False
        if not self.IsCPULoadNormal():
            print("Failed! CPU load unnormal")
            return False
        return True

    def DroppedPacketsExist(self):
        droppedFlag = False
        for key, value in self.packetsLog.items():
            if value[0] == value[1]:
                continue
            else:
                print(
                    f"Packets dropped in {key};\tsent: {value[0]};\treceived: {value[1]}"
                )
                droppedFlag = True
        return True if droppedFlag else False

    def RobustnessCheck(self):
        print("\nROBUSTNESS CHECK:\n=================")
        if self.DroppedPacketsExist():
            return False
        return True

    def RampSingleLoad(self, dt, dtEnd, step, count, msg):
        print("RAMP LOAD ...")
        tx = rx = 0
        while dt >= dtEnd:
            print(f"dt: {dt}")
            for _ in range(count):
                super().TransmitCan(self.chn_handle, 0, 0x100, msg, 8)
                tx += 1
                super().zcanlib.ClearBuffer(self.chn_handle)
                _, rcv = super().ReceiveCan(self.chn_handle)
                rx += rcv
                time.sleep(dt)
            dt -= step
        return tx, rx

    def ContinuouseSingleLoad(self, start, duration, msg):
        print("CONTINUOUS LOAD ...")
        tx = rx = 0
        while time.time() - start < duration:
            super().TransmitCan(self.chn_handle, 0, 0x100, msg, 8)
            tx += 1
            super().zcanlib.ClearBuffer(self.chn_handle)
            _, rcv = super().ReceiveCan(self.chn_handle)
            rx += rcv
        return tx, rx

    def Scenario1(self):
        print("\nTESTING SCENARIO 1\n=================")
        msg = [0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7]
        start = time.time()
        result = (0, 0)
        result1 = self.RampSingleLoad(0.01, 0.001, 0.001, 200, msg)
        result2 = self.ContinuouseSingleLoad(start, 20, msg)
        results = [result1, result2]
        result = tuple(sum(x) for x in zip(*results))
        self.packetsLog["Scenario1"] = result
        print("Test duration: ", time.time() - start)
        return True

    def MakeRandomMsgs(self, num):
        msgs = []
        for _ in range(num):
            msg = [random.randint(0, 255) for _ in range(8)]
            msgs.append(msg)
        return msgs

    def CyclicLoad(self, start, duration, dt, msgs):
        print("CYCLIC LOAD ...")
        tx = rx = 0
        while time.time() - start < duration:
            for msg in msgs:
                super().TransmitCan(self.chn_handle, 0, 0x100, msg, 8)
                tx += 1
                super().zcanlib.ClearBuffer(self.chn_handle)
                _, rcv = super().ReceiveCan(self.chn_handle)
                rx += rcv
                time.sleep(dt)
        return tx, rx

    def Scenario2(self):
        print("\nTESTING SCENARIO 2\n=================")
        msgs = self.MakeRandomMsgs(100)
        start = time.time()
        result = self.CyclicLoad(start, 10, 0.01, msgs)
        self.packetsLog["Scenario2"] = result
        print("Test duration: ", time.time() - start)
        return True

    def RampCyclicLoad(self, dt, dtEnd, step, msgs):
        print("RAMP CYCLIC LOAD ...")
        tx = rx = 0
        while dt >= dtEnd:
            print(f"dt: {dt}")
            for msg in msgs:
                super().TransmitCan(self.chn_handle, 0, 0x100, msg, 8)
                tx += 1
                super().zcanlib.ClearBuffer(self.chn_handle)
                _, rcv = super().ReceiveCan(self.chn_handle)
                rx += rcv
                time.sleep(dt)
            dt -= step
        return tx, rx

    def ContinouseCyclicLoad(self, start, duration, dt, msgs):
        print("CONTINUOUS CYCLIC LOAD ...")
        tx = rx = 0
        while time.time() - start < duration:
            for msg in msgs:
                super().TransmitCan(self.chn_handle, 0, 0x100, msg, 8)
                tx += 1
                super().zcanlib.ClearBuffer(self.chn_handle)
                _, rcv = super().ReceiveCan(self.chn_handle)
                rx += rcv
                time.sleep(dt)
        return tx, rx

    def Scenario3(self):
        print("\nTESTING SCENARIO 3\n=================")
        msgs = self.MakeRandomMsgs(100)
        start = time.time()
        result1 = self.RampCyclicLoad(0.01, 0.001, 0.001, msgs)
        result2 = self.ContinouseCyclicLoad(start, 10, 0.01, msgs)
        results = [result1, result2]
        result = tuple(sum(x) for x in zip(*results))
        self.packetsLog["Scenario3"] = result
        print("Test duration: ", time.time() - start)
        return True
