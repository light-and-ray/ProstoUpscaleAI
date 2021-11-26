from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Ui_MainWindow import Ui_MainWindow
from upscaler import Upscaler
import helper, config


class MainWindow(QMainWindow):
#public:
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUi()

        self._upscaler = Upscaler()
        self._hideTimer = QTimer()
        self._backgroundTimer = QTimer()
        self._backgroundTimer.timeout.connect(self._background)
        self._backgroundTimer.start(50)
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
        self.preview1.setup(config.DEFAULT_PICTURE)
        self.preview2.setup(config.DEFAULT_PICTURE)
        self.preview1.setSibling(self.preview2)
        self.preview2.setSibling(self.preview1)

        self.previewProgressBar = self.ui.preview2Holder.ui.progressBar
        self.previewProgressBar.setMaximum(100*100)
        self.previewProgressBar.setMinimum(0)
        self.previewProgressBar.setValue(0)
        self.previewProgressBar.hide()

        self.addImagesButton = self.ui.addImagesButton
        self.convertButton = self.ui.convertButton

        self.show()


    def setPicture(self, path):
        self._picture = path
        self.preview1.setPicture(self._picture)
        self.preview2.setPicture(self._picture)
        self._needUpscalePreview_var = True
        self.preview2.upscaled.hide()
        self.updateTitle(helper.filenameByPath(path))
        self._upscaler.kill()

    def updateTitle(self, text):
        self.setWindowTitle(f'{text} - ProstoUpscaleAi - alpha')

    def setOnDrop(self, func):
        self._onDrop = func

#private:

    def _upscalePreview(self):
        self._needUpscalePreview_var = False
        self._hideTimer.stop()
        self.previewProgressBar.setValue(0)
        self.previewProgressBar.show()
        QApplication.processEvents()
        helper.mkdir(config.tmp)
        self.savePath = f'{config.tmp}/preview.png'
        self.upscaledPath = f'{config.tmp}/preview-4x.jpg'
        self.preview1.save(self.savePath)

        self._upscaler.run(self.savePath, self.upscaledPath)

        def onMove():
            self.previewProgressBar.hide()
            self._upscaler.kill()
            self._hideTimer.stop()
            self._needUpscalePreview_var = True
            self.preview2.hideBlackout()

        self.preview1.picture.setOnMoveCallback(onMove)


    def _onHideProgressBarTimeout(self):
        print("onHideTimeout")
        self.previewProgressBar.hide()
        self._upscaler.percents = None
        self._hideTimer.stop()


    def _onUpscalePreviewComplete(self):
        self.preview2.showUpscaled(self.upscaledPath)
        print('onUpscalePreviewComplete')
        self._hideTimer.timeout.connect(self._onHideProgressBarTimeout)
        self._hideTimer.start(1000)
        self.preview2.hideBlackout()

    def _needUpscalePreview(self):
        return self._needUpscalePreview_var


    def _background(self):
        per = self._upscaler.percents
        if per is not None:
            self.previewProgressBar.setValue(int(100 * per))

        if self._upscaler.showBlackout is not None:
            if self._upscaler.showBlackout:
                self.preview2.showBlackout()
            else:
                self.preview2.hideBlackout()
            self._upscaler.showBlackout = None

        if self._upscaler.complete():
            self._onUpscalePreviewComplete()

        if self._needUpscalePreview():
            timeDiff = helper.currentTime() - self.preview1.picture.getLastMove()
            if timeDiff >= config.TIMEOUT_BEFORE_UPSCALE:
                self._upscalePreview()

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        self._onDrop(event)

    def closeEvent(self, event: QCloseEvent):
        self._upscaler.kill()
        event.accept()

