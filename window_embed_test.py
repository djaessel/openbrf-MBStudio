import sys, os, shutil
from PySide6.QtCore import (
    Qt, QProcess, QTimer,
    )
from PySide6.QtGui import (
    QWindow,
    )
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QMessageBox,
    )


################################################################################################################################
# Taken from:                                                                                                                  #
# https://stackoverflow.com/questions/65816656/how-to-detect-when-a-foreign-window-embedded-with-qwidget-createwindowcontainer #
################################################################################################################################

class Window(QWidget):
    def __init__(self, program, arguments):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.external = QProcess(self)
        self.external.start(program, arguments)
        self.wmctrl = QProcess()
        self.wmctrl.setProgram('wmctrl')
        self.wmctrl.setArguments(['-lpx'])
        self.wmctrl.readyReadStandardOutput.connect(self.handleReadStdOut)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(25)
        self.timer.timeout.connect(self.wmctrl.start)
        self.timer.start()
        self._tries = 0

    def closeEvent(self, event):
        for process in self.external, self.wmctrl:
            process.terminate()
            process.waitForFinished(2000)

    def embedWindow(self, wid):
        window = QWindow.fromWinId(wid)
        window.requestActivate()
        widget = QWidget.createWindowContainer(window, self, Qt.FramelessWindowHint)
        self.layout().addWidget(widget)

    def handleReadStdOut(self):
        pid = self.external.processId()
        if pid > 0:
            windows = {}
            for line in bytes(self.wmctrl.readAll()).decode().splitlines():
                columns = line.split(maxsplit=5)
                # print(columns)
                # wid, desktop, pid, wmclass, client, title
                windows[int(columns[2])] = int(columns[0], 16)
            if pid in windows:
                self.embedWindow(windows[pid])
                # this is where the magic happens...
                self.external.finished.connect(self.close)
            elif self._tries < 100:
                self._tries += 1
                self.timer.start()
            else:
                QMessageBox.warning(self, 'Error', 'Could not find WID for PID: %s' % pid)
        else:
            QMessageBox.warning(self, 'Error', 'Could not find PID for: %r' % self.external.program())

if __name__ == '__main__':

    if len(sys.argv) > 1:
        if shutil.which(sys.argv[1]):
            app = QApplication(sys.argv)
            window = Window(sys.argv[1], sys.argv[2:])
            window.setGeometry(100, 100, 800, 600)
            window.show()
            sys.exit(app.exec())
        else:
            print('could not find program: %r' % sys.argv[1])
    else:
        print('usage: python %s <external-program-name> [args]' %
              os.path.basename(__file__))
