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


def run_app(window_id):
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QWindow
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QPushButton

    app = QApplication([])
    main_widget = QWidget()
    main_widget.setGeometry(0, 0, 1000, 800)
    layout = QVBoxLayout(main_widget)

    window = QWindow.fromWinId(window_id)
    window.setFlag(Qt.FramelessWindowHint, True)
    widget = QWidget.createWindowContainer(window)
    widget.setWindowFlags(Qt.FramelessWindowHint)
    layout.addWidget(widget)

    button = QPushButton('Close')
    button.clicked.connect(main_widget.close)
    layout.addWidget(button)

    main_widget.show()

    widget.update()

    app.exec()


from subprocess import Popen, PIPE, STDOUT
from openbrf import OpenBrf

if __name__ == '__main__':
    ##window_id = get_window_id('Calculator')
    ##window_id = 41943046
    ##window_id = 50331661
    ##window_id = 50331654

    #process = Popen(['./Testor'], stdout=PIPE, stderr=STDOUT)
    ##stdout, stderr = process.communicate()
    ###print(stdout)
    ##print(int(str(stderr).split(' ')[0][2:]))

    #for line in iter(process.stdout.readline, b''):
    #    print(">>>", line.rstrip())
    #    window_id = int(line.rstrip())
    #    break

    ##window_id = 46137350

    #openbrf = OpenBrf()
    #window_id = int(openbrf.getCurWindowPtr())
    
    window_id = 73400330
    if window_id:
        print(window_id)
        run_app(window_id)

