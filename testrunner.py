import time
from openbrf import OpenBrf


openbrf = OpenBrf()
openbrf.setModPath(b"/home/djaessel/.steam/debian-installation/steamapps/common/MountBlade Warband/Modules/Native/")
openbrf.selectItemMesh(b"military_hammer")
wid = openbrf.getCurWindowPtr()
print(wid)
#openbrf.closeApp()

print("I am done.")
