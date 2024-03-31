import os
import time
import signal

process = None

def get_window_id(name):
    import Xlib.display

    d = Xlib.display.Display()
    r = d.screen().root

    window_ids = r.get_full_property(
        d.intern_atom('_NET_CLIENT_LIST'), Xlib.X.AnyPropertyType
    ).value

    for window_id in window_ids:
        window = d.create_resource_object('window', window_id)
        if window.get_wm_name() == name:
            return window_id

def close_openbrf():
    print("Close openBrf")
    if process != None:
        process.send_signal(signal.SIGINT)
        #process.wait()
    with open("piper.txt", "w") as f:
        f.write("exit")


def select_club():
    with open("piper.txt", "w") as f:
        f.write("select:mesh:club")


def run_app(window_id):
    from PySide6.QtCore import Qt, QUrl
    from PySide6.QtGui import QWindow, QColor, QSurfaceFormat
    from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QApplication, QPushButton
    from PySide6.QtQuickWidgets import QQuickWidget

    app = QApplication([])
    main_widget = QWidget()
    main_widget.setGeometry(0, 0, 1000, 800)
    main_widget.setStyleSheet("background-color: 'grey'")
    layout = QVBoxLayout()
    layout2 = QVBoxLayout()
    layout3 = QHBoxLayout(main_widget)

    window = QWindow.fromWinId(window_id)
    window.setFlag(Qt.FramelessWindowHint, True)
    widget = QWidget.createWindowContainer(window)
    widget.setWindowFlags(Qt.FramelessWindowHint)
    layout.addWidget(widget)

    format = QSurfaceFormat()
    format.setAlphaBufferSize(8)
    qmlWindow = QQuickWidget()
    qmlWindow.setFormat(format)
    qmlWindow.setWindowFlags(Qt.FramelessWindowHint)
    qmlWindow.setAttribute(Qt.WA_AlwaysStackOnTop);
    qmlWindow.setAttribute(Qt.WA_TranslucentBackground)
    qmlWindow.setClearColor(QColor(Qt.transparent))
    qmlWindow.setResizeMode(QQuickWidget.SizeRootObjectToView)
    qmlWindow.setSource(QUrl.fromLocalFile("main.qml"))


    button1 = QPushButton('Select club')
    button1.clicked.connect(select_club)

    button2 = QPushButton('Close')
    button2.clicked.connect(close_openbrf)
    button2.clicked.connect(main_widget.close)
    layout2.addWidget(button2)

    layout2.addWidget(button1)
    layout2.addWidget(qmlWindow)

    layout3.addLayout(layout)
    layout3.addLayout(layout2)

    main_widget.show()

    # glitch fix
    time.sleep(1)
    main_widget.setGeometry(0, 0, 1100, 900)

    app.exec()


from subprocess import Popen, PIPE, STDOUT
from openbrf import OpenBrf

if __name__ == '__main__':
    ##window_id = get_window_id('Calculator')

    #process = Popen(['./Testor'], stdout=PIPE, stderr=STDOUT)
    ##stdout, stderr = process.communicate()
    ###print(stdout)
    ##print(int(str(stderr).split(' ')[0][2:]))

    process = Popen(['python3', 'testrunner.py'], stdout=PIPE, stderr=STDOUT)

    window_id = None
    #for line in iter(process.stdout.readline, b''):
    #    print(">>>", line.rstrip())
    #    try:
    #        window_id = int(line.rstrip())
    #        break
    #    except:
    #        pass

    while not os.access("piper.txt", os.R_OK):
        time.sleep(1)
    
    try:
        with open("piper.txt") as f:
            window_id = int(f.read())
    except:
        window_id = None

    #openbrf = OpenBrf()
    #window_id = int(openbrf.getCurWindowPtr())
    
    if window_id:
        run_app(window_id)

