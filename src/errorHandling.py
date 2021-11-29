from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import helper, config


class _ErrorHandling:
    def __init__(self):
        self._lastHandleTime = 0
        self._unhandled = []
        self._lastCount = 0

    def add(self, text):
        self._unhandled.append(text)

    def handle(self):
        for error in self._unhandled:
            print(f'ERROR: {error}')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(error))
            msg.setWindowTitle("Error")
            msg.exec_()
            self._unhandled.remove(error)

instance = _ErrorHandling()
