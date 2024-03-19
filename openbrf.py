import time
import load_openbrf_lib as openBrfLib




def SetModPath(lib, *argv):
    time.sleep(5)
    print("Changing mod path...")
    print(">", argv[0][0])
    lib.SetModPath(argv[0][0])
    #lib.SetModPath(b"/home/djaessel/.steam/debian-installation/steamapps/common/MountBlade Warband/Modules/Native/")


def SelectItemMesh(lib, *argv):
    time.sleep(5)
    print("Selecting", str(argv[0][0]), "...")
    res = lib.SelectItemByNameAndKind(argv[0][0], 0)
    #res = lib.SelectItemByNameAndKind(b"military_hammer", 0)
    #print("RESULT:", res)


def CloseApp(lib, *argv):
    print("Closing app...")
    time.sleep(5)
    lib.CloseApp()




class OpenBrf():
    opened = False


    def __init__(self):
        if not OpenBrf.opened:
            OpenBrf.opened = True
            openBrfLib.run()

    def setModPath(self, modPath : str):
        if OpenBrf.opened:
            openBrfLib.callFunc(SetModPath, modPath)


    def selectItemMesh(self, meshName : str):
        if OpenBrf.opened:
            openBrfLib.callFunc(SelectItemMesh, meshName)


    def closeApp(self):
        if OpenBrf.opened:
            openBrfLib.callFunc(CloseApp)
            OpenBrf.opened = False


