from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Ui_FileCard import Ui_FileCard


class FileCard(QWidget):
    def __init__(self, parent):
        super(FileCard, self).__init__(parent)
        self.ui = Ui_FileCard()
        self.ui.setupUi(self)

    def mousePressEvent(self, event):
        print('pressed')
        self.ui.frame.setFocus()
