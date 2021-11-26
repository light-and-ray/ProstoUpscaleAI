from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Ui_MainWindow import Ui_MainWindow
from upscaler import Upscaler
import helper


class MainWindow(QMainWindow):
    TIMEOUT_BEFORE_UPSCALE = 900
    DEFAULT_PICTURE = 'photo_1000.jpg'

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUi()
        self.ui.convertButton.clicked.connect(self._upscalePreview)
        self.upscaler = Upscaler()
        self.hideTimer = QTimer()
        self.backgroundTimer = QTimer()
        self.backgroundTimer.timeout.connect(self._background)
        self.backgroundTimer.start(50)
        self._needUpscalePreview_var = True
        self.setAcceptDrops(True)


    def initUi(self):
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAction)

        self.preview1 = self.ui.preview1
        self.preview2 = self.ui.preview2Holder.preview
        self.preview1.setup(self.DEFAULT_PICTURE)
        self.preview2.setup(self.DEFAULT_PICTURE)
        self.preview1.setSibling(self.preview2)
        self.preview2.setSibling(self.preview1)

        self.previewProgressBar = self.ui.preview2Holder.ui.progressBar
        self.previewProgressBar.setMaximum(100*100)
        self.previewProgressBar.setMinimum(0)
        self.previewProgressBar.setValue(0)
        self.previewProgressBar.hide()

        self.addImagesButton = self.ui.addImagesButton

        self.show()


    def setPicture(self, path):
        self._picture = path
        self.preview1.setPicture(self._picture)
        self.preview2.setPicture(self._picture)
        self._needUpscalePreview_var = True
        self.preview2.upscaled.hide()
        self.updateTitle(helper.filenameByPath(path))

    def updateTitle(self, text):
        self.setWindowTitle(f'{text} - ProstoUpscaleAi - alpha')

    def setOnDrop(self, func):
        self._onDrop = func

    def _upscalePreview(self):
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
            self.preview2.hideBlackout()

        self.preview1.picture.setOnMoveCallback(onMove)


    def _onHideProgressBarTimeout(self):
        print("onHideTimeout")
        self.previewProgressBar.hide()
        self.upscaler.percents = None
        self.hideTimer.stop()


    def _onUpscalePreviewComplete(self):
        self.preview2.showUpscaled(self.pathAfter)
        print('onUpscalePreviewComplete')
        self.hideTimer.timeout.connect(self._onHideProgressBarTimeout)
        self.hideTimer.start(1000)
        # self._onHideProgressBarTimeout()
        self.preview2.hideBlackout()

    def _needUpscalePreview(self):
        return self._needUpscalePreview_var


    def _background(self):
        per = self.upscaler.percents
        if per is not None:
            self.previewProgressBar.setValue(int(100 * per))

        if self.upscaler.showBlackout is not None:
            if self.upscaler.showBlackout:
                self.preview2.showBlackout()
            else:
                self.preview2.hideBlackout()
            self.upscaler.showBlackout = None

        if self.upscaler.complete():
            self._onUpscalePreviewComplete()

        if self._needUpscalePreview():
            timeDiff = helper.currentTime() - self.preview1.picture.lastMove()
            if timeDiff >= self.TIMEOUT_BEFORE_UPSCALE:
                self._upscalePreview()

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        self._onDrop(event)

