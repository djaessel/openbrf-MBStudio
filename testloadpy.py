from ctypes import *
lib = CDLL("./libopenBrf.so")

def checkx():
    for func_name in dir(lib):
        print(func_name)

args = (c_char_p * 1)()
args[0] = b"test"

lib.StartExternal(len(args), args)
#checkx()
