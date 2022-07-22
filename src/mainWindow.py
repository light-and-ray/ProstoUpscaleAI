from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Ui_MainWindow import Ui_MainWindow
from upscaler import Upscaler, UpscaleOptions
import helper, config


class MainWindow(QMainWindow):
#public:
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUi()

        self._upscaler = Upscaler(None) #on finish
        self._hideTimer = QTimer()

        self._needUpscalePreview_var = True
        self.setAcceptDrops(True)
        self._picture = None
        self._pictureOptions = None

        self._onCloseCallbacks = []
        self.addOnCloseCallback(self._upscaler.kill)
        self.addOnCloseCallback(lambda: helper.execCmd(f'rm -d "{config.tmp}"'))

        self._isPreviewFrameHidden = False


    def initUi(self):
        self.preview1 = self.ui.preview1
        self.preview2 = self.ui.preview2Holder.preview
        self.preview1.setSibling(self.preview2)
        self.preview2.setSibling(self.preview1)

        self.previewProgressBar = self.ui.preview2Holder.ui.progressBar
        self.previewProgressBar.setMaximum(100*100)
        self.previewProgressBar.setMinimum(0)
        self.previewProgressBar.setValue(0)
        self.previewProgressBar.hide()

        self.addImagesButton = self.ui.addImagesButton
        self.convertAllButton = self.ui.convertAllButton
        self.savingOptionsButton = self.ui.savingOptionsButton
        self.scrollLayout = self.ui.scrollLayout
        self.expandListButton = self.ui.expandListButton
        self.previewFrame = self.ui.previewFrame
        self.scrollArea = self.ui.scrollArea

        self.show()


    def setPicture(self, path, options):
        self._picture = path
        self._pictureOptions = options
        self.preview1.setPicture(self._picture)
        self.preview2.setPicture(self._picture)
        self._needUpscalePreview_var = True
        self.preview2.upscaled.hide()
        if path is not None:
            self.updateTitle(helper.filenameByPath(path))
        else:
            self.updateTitle(None)
        self._upscaler.kill()


    def setXY(self, x, y):
        self.preview1.setXY(x, y)
        self.preview2.setXY(x, y)


    def updateTitle(self, text):
        if text is not None:
            self.setWindowTitle(f'{text} - ProstoUpscaleAi - alpha')
        else:
            self.setWindowTitle(f'ProstoUpscaleAi - alpha')


    def setOnDrop(self, func):
        self._onDrop = func

    def setOnPaste(self, func):
        self._onPaste = func

    def addCard(self, card):
        self.scrollLayout.addWidget(card)

    def removeCard(self, card):
        self.scrollLayout.removeWidget(card)
        card.close()


    def scrollToButtom(self):
        QApplication.processEvents()
        value = self.ui.scrollArea.verticalScrollBar().maximum()
        self.ui.scrollArea.verticalScrollBar().setValue(value)


    def addOnCloseCallback(self, func):
        self._onCloseCallbacks.append(func)


    def hidePreviewFrame(self):
        self.previewFrame.hide()
        self._isPreviewFrameHidden = True

    def showPreviewFrame(self):
        self.previewFrame.show()
        self._isPreviewFrameHidden = False


#private:

    def _upscalePreview(self):
        self._needUpscalePreview_var = False
        self._hideTimer.stop()
        self.previewProgressBar.setValue(0)
        self.previewProgressBar.show()
        QApplication.processEvents()
        #иногда, если png:
        # image /home/neon/workspace/ProstoUpscaleAI/ProstoUpscaleAI/tmp/preview.png has alpha channel !
        #  /home/neon/workspace/ProstoUpscaleAI/ProstoUpscaleAI/tmp/preview.png will output
        # /home/neon/workspace/ProstoUpscaleAI/ProstoUpscaleAI/tmp/preview-4x.jpg.png
        self.savePath = f'{config.tmp}/preview.jpg'
        self.upscaledPath = f'{config.tmp}/preview-4x.jpg'
        self.preview1.save(self.savePath)

        self._upscaler.run(self._pictureOptions, self.savePath, self.upscaledPath)

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
        self._upscaler.setPercents(None)
        self._hideTimer.stop()


    def _onUpscalePreviewComplete(self):
        self.preview2.showUpscaled(self.upscaledPath)
        print('onUpscalePreviewComplete')
        helper.reconnect(self._hideTimer.timeout, self._onHideProgressBarTimeout)
        self._hideTimer.start(1000)
        self.preview2.hideBlackout()

    def _needUpscalePreview(self):
        return self._needUpscalePreview_var\
            and self.preview1.imagePath is not None\
            and not self._isPreviewFrameHidden


    def _background(self):
        per = self._upscaler.getPercents()
        if per is not None:
            self.previewProgressBar.setValue(int(100 * per))

            if self._upscaler.complete():
                self._onUpscalePreviewComplete()

        if self._upscaler.inProcess is not None:
            if self._upscaler.inProcess:
                self.preview2.showBlackout()
            else:
                self.preview2.hideBlackout()
            self._upscaler.inProcess = None


        if self._needUpscalePreview():
            timeDiff = helper.currentTime() - self.preview1.picture.getLastMove()
            if timeDiff >= config.TIMEOUT_BEFORE_UPSCALE:
                self._upscalePreview()

    def dragEnterEvent(self, event : QDragEnterEvent):
        event.accept()

    def dropEvent(self, event : QDropEvent):
        self._onDrop(event)

    def keyPressEvent(self, event : QKeyEvent):
        super(MainWindow, self).keyPressEvent(event)
        if event.key() == Qt.Key_V and event.modifiers() == Qt.ControlModifier:
            text = QApplication.clipboard().text()
            print('Ctrl+V:', text)
            self._onPaste(text)

    def closeEvent(self, event: QCloseEvent):
        for onClose in self._onCloseCallbacks:
            onClose()
        event.accept()

