from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Ui_PreviewWidgetWithProgressBar import Ui_PreviewWidgetWithProgressBar

class PreviewWidgetWithProgressBar(QWidget):
    def __init__(self, parent):
        super(PreviewWidgetWithProgressBar, self).__init__(parent)
        self.ui = Ui_PreviewWidgetWithProgressBar()
        self.ui.setupUi(self)
        self.preview = self.ui.preview
