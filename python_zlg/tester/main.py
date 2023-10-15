import platform
import sys
import os
from tester import *

if __name__ == "__main__":
    if platform.python_version() >= "3.8.0":
        os.add_dll_directory(os.getcwd())

    bus = [0xC, 0x19, 0x1A, 0x24, 0xDF, ZCAN_VIRTUAL_DEVICE]
    com = Tester(bus[0])

    if len(sys.argv) != 2:
        print("\nTo replay BLF file use: python main.py <sample.blf>")
        print("Running default operation")

        # com.SearchAllBuses()
        # dev_handle = com.OpenUsbCanII()
        com.SampleSendReceiveOnBus()

    else:
        file = sys.argv[1]
        com.LoadBLF(file)
        com.SendCanFromBLC()
