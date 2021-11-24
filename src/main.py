from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from Ui_MainWindow import Ui_MainWindow


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAction)

        self.setWindowTitle('ProstoUpscaleAi - alpha')

        self.ui.preview1.setup('photo.jpg', 4)
        self.ui.preview2Holder.preview.setup('photo_4x.jpg', 1)
        self.ui.preview1.setSibling(self.ui.preview2Holder.preview)
        self.ui.preview2Holder.preview.setSibling(self.ui.preview1)


        self.show()



app = QApplication([])
application = Window()
application.showMaximized()

sys.exit(app.exec())
