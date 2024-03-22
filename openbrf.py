import time
import load_openbrf_lib as openBrfLib




def IsCurHWndShown(lib, argv) -> bool:
    return lib.IsCurHWndShown()


def GetCurWindowPtr(lib, argv) -> int:
    return lib.GetCurWindowPtr()


def SetModPath(lib, argv):
    time.sleep(1)
    print("Changing mod path...")
    print(">", argv[0])
    lib.SetModPath(argv[0])


# unused?
def SelectItemMesh(lib, argv) -> bool:
    time.sleep(2)
    print("Selecting", argv[0], "...")
    res = lib.SelectItemByNameAndKind(argv[0], 0)
    return res


def SelectItemByNameAndKind(lib, argv) -> bool:
    time.sleep(2)
    print("Selecting", argv[0], "|", argv[1], "...")
    res = lib.SelectItemByNameAndKind(argv[0], argv[1])
    return res


def SelectItemByNameAndKindFromCurFile(lib, argv) -> bool:
    time.sleep(2)
    print("Selecting", argv[0], "|", argv[1], "...")
    res = lib.SelectItemByNameAndKindFromCurFile(argv[0], argv[1])
    return res


def SelectIndexOfKind(lib, argv):
    time.sleep(1)
    print("Selecting kind", argv[0], "by index", argv[1], "...")
    lib.SelectIndexOfKind(argv[0], argv[1])


def SelectCurKindMany(lib, argv):
    time.sleep(1)
    print("Selecting cur kind from index", argv[0], "to", argv[1], "...")
    lib.SelectCurKindMany(argv[0], argv[1])


#
# TODO: add missing functions
#
# bool AddMeshToXViewModel(char* meshName, int bone = 0, int skeleton = 0, int carryPosition = -1/*, bool isAtOrigin = true*/, bool mirror = false, char* material = NULL, uint vertColor = 0)
# void ShowTroop3DPreview(bool forceUpdate = false)
# void RemoveMeshFromXViewModel(char* meshName)
# void ClearTempMeshesTroop3DPreview()
# 
# Below just if needed:
# void AddCurSelectedMeshsAllDataToMod(char* modName)



def CloseApp(lib, argv):
    print("Closing app...")
    time.sleep(1)
    lib.CloseApp()




class OpenBrf():
    opened = False


    def __init__(self):
        if not OpenBrf.opened:
            OpenBrf.opened = True
            openBrfLib.run()


    def isCurHWndShown(self):
        if OpenBrf.opened:
            return openBrfLib.callFunc(IsCurHWndShown)
        return False


    def getCurWindowPtr(self):
        if OpenBrf.opened: #and self.isCurHWndShown():
            return openBrfLib.callFunc(GetCurWindowPtr)
        print("ERROR")
        return 0


    def setModPath(self, modPath : str):
        if OpenBrf.opened:
            openBrfLib.callFunc(SetModPath, modPath)


    def selectItemMesh(self, meshName : str, kind : int = 0):
        if OpenBrf.opened:
            openBrfLib.callFunc(SelectItemByNameAndKind, meshName, kind)


    def selectItemByNameAndKindFromCurFile(self, meshName : str, kind : int = 0):
        if OpenBrf.opened:
            openBrfLib.callFunc(SelectItemByNameAndKindFromCurFile, meshName, kind)


    def selectIndexOfKind(self, kind : int, index : int):
        if OpenBrf.opened:
            openBrfLib.callFunc(SelectIndexOfKind, kind, index)


    def selectCurKindMany(self, startIndex : int, endIndex : int):
        if OpenBrf.opened:
            openBrfLib.callFunc(SelectCurKindMany, startIndex, endIndex)


    def closeApp(self):
        if OpenBrf.opened:
            openBrfLib.callFunc(CloseApp)
            openBrfLib.closer()
            OpenBrf.opened = False


