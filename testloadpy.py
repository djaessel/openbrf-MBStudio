import time
import threading
from ctypes import *

def main():
    lib = CDLL("./libopenBrf.so")
    
    x = threading.Thread(target=start_lib, args=(lib,))
    x.start()

    #y = threading.Thread(target=extra, args=(lib,))
    #y.start()
    
    extra(lib)


def start_lib(lib):
    args = (c_char_p * 1)()
    args[0] = b""
    lib.StartExternal(len(args), args)


def extra(lib):
    time.sleep(5)

    lib.SetModPath(b"/home/djaessel/.steam/debian-installation/steamapps/common/MountBlade Warband/Modules/NordInvasion/")

    print("GET READY")

    time.sleep(5)

    name = b"club"
    kind = 0
    res = lib.SelectItemByNameAndKind(name, kind)
    print("RESULT:", res)

    time.sleep(5)

    res = lib.SelectItemByNameAndKindFromCurFile(name, kind)
    print("RESULT:", res)


main()

