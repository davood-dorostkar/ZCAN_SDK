import platform
import sys
import os
from tester import *

if __name__ == "__main__":
    if platform.python_version() >= "3.8.0":
        os.add_dll_directory(os.getcwd())

    bus = [0xC, 0x19, 0x1A, 0x24, 0x2F, ZCAN_VIRTUAL_DEVICE]

    if len(sys.argv) == 2 and sys.argv[1] == "test":
        com = Tester(bus[0])
        sequences = [
            com.RampUpCPU,
            com.Scenario1,
            com.Scenario2,
            com.Scenario3,
            com.RampDownCPU,
            com.ElasticityCheck,
            com.RobustnessCheck,
        ]

        for step in sequences:
            try:
                if not step():
                    print(f"{step.__name__} failed")
                    break
                else:
                    print(f"{step.__name__} successful")
            except Exception as e:
                print(f"Exception in {step.__name__}: {str(e)}")
                break
        com.End()

    elif len(sys.argv) == 3:
        com = Tester(bus[0])
        if sys.argv[1] == "f":
            file = sys.argv[2]
            com.LoadBLF(file)
            # com.SendCanFromBLC()
            com.PrintBLF()
            com.End()

        elif sys.argv[1] == "loop":
            if sys.argv[2] == "send":
                com.LoopbackSend(0.5)
            elif sys.argv[2] == "get":
                com.LoopbackReceive()

    else:
        print("\n=== To replay BLF file use: python main.py <sample.blf> ===")
        print("=== Running default operation ===\n")

        # com.SearchAllBuses()
        for i in bus:
            com = Tester(i)
            com.SampleSendReceive()
            com.End()
