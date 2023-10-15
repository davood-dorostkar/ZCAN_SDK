import platform
import sys
import os
from tester import *

if __name__ == "__main__":
    if platform.python_version() >= "3.8.0":
        os.add_dll_directory(os.getcwd())

    bus = [0xC, 0x19, 0x1A, 0x24, 0x2F, ZCAN_VIRTUAL_DEVICE]

    if len(sys.argv) == 1:
        print("\n=== To replay BLF file use: python main.py <sample.blf> ===")
        print("=== Running default operation ===\n")

        for i in bus:
            com = Tester(i)
            com.SampleSendReceiveOnBus()

        # com.SearchAllBuses()
        # dev_handle = com.OpenUsbCanII()
        # com.SampleSendReceiveOnBus()

    elif sys.argv[1] == "test":
        com = Tester(bus[0])
        com.Scenario3()

    else:
        file = sys.argv[1]
        com = Tester(bus[0])
        com.LoadBLF(file)
        com.SendCanFromBLC()

    com.End()
