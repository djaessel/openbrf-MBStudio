import time
import threading
from ctypes import *

def main():
    lib = CDLL("./libopenBrf.so")
    
    x = threading.Thread(target=start_lib, args=(lib,))
    x.start()

    extra(lib)


def start_lib(lib):
    args = (c_char_p * 1)()
    args[0] = b""
    lib.StartExternal(len(args), args)


def extra(lib):
    time.sleep(5)

    lib.SetModPath(b"/home/djaessel/.steam/debian-installation/steamapps/common/MountBlade Warband/Modules/Native/")

    print("GET READY")

    time.sleep(5)
    res = lib.SelectItemByNameAndKind(b"club", 0)
    #print("RESULT:", res)

    time.sleep(5)
    res = lib.SelectItemByNameAndKind(b"sledgehammer", 0)
    #print("RESULT:", res)

    time.sleep(5)
    res = lib.SelectItemByNameAndKind(b"military_hammer", 0)
    #print("RESULT:", res)

    time.sleep(5)
    lib.CloseApp()

main()

