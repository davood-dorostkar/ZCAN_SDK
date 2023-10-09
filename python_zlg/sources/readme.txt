说明：
1、zlgcan.py为zlgcan python版本接口，目前支持CAN/CANFD接口操作。其中包含对USBCANFD-100U的自发自收测试DEMO。
2、demo/zlgcan_demo.py为基于tkinter实现的GUI例程,其实现了USBCAN(FD)系列产品的数据收发功能。
   其中，demo/output/zlgcan_demo.exe为zlgcan_demo.py用pyinstaller打包后生成的exe文件。
3、当前Demo已验证支持Python 3.6版本,zlgcan.py已验证支持Python2.7及3.6版本。

使用说明：
1、直接运行zlgcan.py或zlgcan_demo.py时，
   应按python位数选择对应的zlgcan库（32位python对应zlgcan_x86,64位python对应zlgcan_64），
   并将zlgcan库中的kerneldlls目录和zlgcan.dll拷贝到python安装根目录下，zlgcan.dll同时拷贝到当前目录下。
   
   原因：由于Python运行时，zlgcan.dll中的GetModuleFileName获取的当前目录指向了Python安装目录！
