from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Ui_MainWindow import Ui_MainWindow
from upscaler import Upscaler
import helper


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUi()
        self.ui.convertButton.clicked.connect(self.renderPreview)
        self.upscaler = Upscaler()
        self.hideTimer = QTimer()
        self.backgroundTimer = QTimer()
        self.backgroundTimer.timeout.connect(self._background)
        self.backgroundTimer.start(50)


    def _background(self):
        per = self.upscaler.percents
        if per is not None:
            self.previewProgressBar.setValue(int(100 * per))
        if self.upscaler.complete() == True:
            self.onUpscaleComplete()

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
        self.preview1 = self.ui.preview1
        self.preview1.setup(photo)
        self.preview2 = self.ui.preview2Holder.preview
        self.preview2.setup(photo)
        self.preview1.setSibling(self.preview2)
        self.preview2.setSibling(self.preview1)

        self.previewProgressBar = self.ui.preview2Holder.ui.progressBar
        self.previewProgressBar.setMaximum(100*100)
        self.previewProgressBar.setMinimum(0)
        self.previewProgressBar.setValue(0)
        self.previewProgressBar.hide()

        self.show()


    def renderPreview(self):
        self.hideTimer.stop()
        self.previewProgressBar.setValue(0)
        self.previewProgressBar.show()
        QApplication.processEvents()
        savePath = f'{helper.root()}/tmp'
        helper.mkdir(savePath)
        self.pathBefore = f'{savePath}/preview.png'
        self.pathAfter = f'{savePath}/preview-4x.png'
        self.preview1.saveVisable(self.pathBefore)


        self.upscaler.run(self.pathBefore, self.pathAfter)

        def onMove():
            self.previewProgressBar.hide()
            self.upscaler.kill()
            self.hideTimer.stop()
        self.preview1.picture.setOnMove(onMove)


    def onHideTimeout(self):
        print("onHideTimeout")
        self.previewProgressBar.hide()
        self.upscaler.percents = None
        self.hideTimer.stop()

    def onUpscaleComplete(self):
        self.preview2.showUpscaled(self.pathAfter)
        print('onUpscaleComplete')
        self.hideTimer.timeout.connect(self.onHideTimeout)
        self.hideTimer.start(1000)
