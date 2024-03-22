import sys
import time
import threading
from openbrf import OpenBrf
from signal import signal, SIGINT, SIGTERM


openbrf = None
x = None

def handlerContrlC(signal_received, frame):
    if openbrf != None:
        openbrf.closeApp()

    if x != None:
        x.join()

    print('SIGINT or CTRL-C detected. Exiting gracefully')
    #time.sleep(5)
    #sys.exit(0)


def handlerTerminate(signal_received, frame):
    if openbrf != None:
        openbrf.closeApp()

    print('SIGTERM Exiting gracefully')
    #time.sleep(5)
    #sys.exit(0)


def check_commands(openBrf):
    while True:
        time.sleep(5)
        changed = False
        with open("piper.txt", "r") as f:
            txt = f.read()
            if txt.startswith("select:mesh:"):
                openbrf.selectItemMesh(txt.split(':')[2].encode('ascii'))
                changed = True
            elif txt == "exit":
                openbBrf.closeApp()
                sys.exit()

        if changed:
            time.sleep(1)
            with open("piper.txt", "w") as f:
                f.write("")


if __name__ == '__main__':
    signal(SIGINT, handlerContrlC)
    signal(SIGTERM, handlerTerminate)

    openbrf = OpenBrf()
    

    openbrf.setModPath(b"/home/djaessel/.steam/debian-installation/steamapps/common/MountBlade Warband/Modules/Native/")
    
    wid = openbrf.getCurWindowPtr()
    print(wid)

    x = threading.Thread(target=check_commands, args=(openbrf,))
    x.start()

