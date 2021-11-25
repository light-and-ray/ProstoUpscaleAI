from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from Ui_MainWindow import Ui_MainWindow
import helper


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUi()


    def initUi(self):
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAction)

        self.setWindowTitle('ProstoUpscaleAi - alpha')

        photo = 'photo.jpg'
        self.ui.preview1.setup(photo)
        self.ui.preview2Holder.preview.setup(photo)
        self.ui.preview1.setSibling(self.ui.preview2Holder.preview)
        self.ui.preview2Holder.preview.setSibling(self.ui.preview1)

        self.ui.preview2Holder.ui.progressBar.setMaximum(100*100)
        self.ui.preview2Holder.ui.progressBar.setMinimum(0)
        self.ui.preview2Holder.ui.progressBar.setValue(0)
        self.ui.preview2Holder.ui.progressBar.hide()

        self.ui.convertButton.clicked.connect(self.renderPreview)

        self.show()


    def renderPreview(self):
        self.ui.preview2Holder.ui.progressBar.setValue(0)
        self.ui.preview2Holder.ui.progressBar.show()
        QApplication.processEvents()
        savePath = f'{helper.root()}/tmp'
        helper.mkdir(savePath)
        pathBefore = f'{savePath}/preview.jpg'
        pathAfter = f'{savePath}/preview-4x.png'
        self.ui.preview1.saveVisable(pathBefore)
        upscaleProgress = helper.dummyUpscaleGenerator(pathBefore, pathAfter)
        for per in upscaleProgress():
            self.ui.preview2Holder.ui.progressBar.setValue(int(per*100))
        self.ui.preview2Holder.preview.showUpscaled(pathAfter)
        self.ui.preview2Holder.ui.progressBar.setValue(100*100)
        self.ui.preview1.pic.setOnMove(lambda: self.ui.preview2Holder.ui.progressBar.hide())
        self.timer = QTimer()
        def onTimeout():
            print("onTimeout")
            self.ui.preview2Holder.ui.progressBar.hide()
            self.timer.stop()

        self.timer.timeout.connect(onTimeout)
        self.timer.start(1000)


app = QApplication([])
application = Window()
application.showMaximized()

sys.exit(app.exec())
