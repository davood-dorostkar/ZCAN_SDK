import sys
import os
import shutil
exe_dir = os.path.split(sys.executable)[0]
dst_dll_dir = exe_dir + "\\kerneldlls"
src_dll_dir = os.getcwd() + "\\kerneldlls"
print("target dll dir: %s" % dst_dll_dir)
if os.path.exists(src_dll_dir):
    if os.path.exists(dst_dll_dir):
        print("target kerneldlls exist then remove!")
        shutil.rmtree(dst_dll_dir)
    shutil.copytree(src_dll_dir, dst_dll_dir)
    print("copy ok!!!")
else:
    print("source kerneldlls no exist!")
input("input any char exit!")