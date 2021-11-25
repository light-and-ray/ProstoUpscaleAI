import time
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
        self.ui.convertButton.clicked.connect(self.upscalePreview)
        self.upscaler = Upscaler()
        self.hideTimer = QTimer()
        self.backgroundTimer = QTimer()
        self.backgroundTimer.timeout.connect(self._background)
        self.backgroundTimer.start(50)
        self._needUpscalePreview_var = True


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


    def upscalePreview(self):
        self._needUpscalePreview_var = False
        self.hideTimer.stop()
        self.previewProgressBar.setValue(0)
        self.previewProgressBar.show()
        QApplication.processEvents()
        helper.mkdir(helper.tmp)
        self.pathBefore = f'{helper.tmp}/preview.png'
        self.pathAfter = f'{helper.tmp}/preview-4x.jpg'
        self.preview1.saveVisable(self.pathBefore)

        self.upscaler.run(self.pathBefore, self.pathAfter)

        def onMove():
            self.previewProgressBar.hide()
            self.upscaler.kill()
            self.hideTimer.stop()
            self._needUpscalePreview_var = True
        self.preview1.picture.setOnMoveCallback(onMove)


    def onHideProgressBarTimeout(self):
        print("onHideTimeout")
        self.previewProgressBar.hide()
        self.upscaler.percents = None
        self.hideTimer.stop()


    def onUpscalePreviewComplete(self):
        self.preview2.showUpscaled(self.pathAfter)
        print('onUpscalePreviewComplete')
        self.hideTimer.timeout.connect(self.onHideProgressBarTimeout)
        self.hideTimer.start(1000)

    def _needUpscalePreview(self):
        return self._needUpscalePreview_var


    TIMEOUT_BEFORE_UPSCALE = 900

    def _background(self):
        per = self.upscaler.percents
        if per is not None:
            self.previewProgressBar.setValue(int(100 * per))
        if self.upscaler.complete() == True:
            self.onUpscalePreviewComplete()

        if self._needUpscalePreview():
            timeDiff = helper.currentTime() - self.preview1.picture.lastMove()
            if timeDiff >= self.TIMEOUT_BEFORE_UPSCALE:
                self.upscalePreview()
