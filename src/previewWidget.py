from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from previewItem import PreviewItem
# from previewWidgetWithProgressBar import PreviewWidgetWithProgressBar


class PreviewWidget(QGraphicsView):
    def __init__(self, parent):
        super(PreviewWidget, self).__init__(parent=parent)

    # def __init__(self, path, scale, parent):
    #     super(PreviewWidget, self).__init__(parent=parent)
    #     self.setup(path, scale)

    def setup(self, path, scale):
        self.SCALE = scale
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.setMinimumSize(300, 300)

        self.scene = QGraphicsScene(parent=self)
        self.setSceneRectFromSize()


        pix = QPixmap(path)
        pix = pix.scaledToWidth(pix.width() * self.SCALE, Qt.SmoothTransformation)


        self.pic = PreviewItem()
        self.updatePicBorder()
        self.pic.setPixmap(pix)
        self.pic.setX(-pix.width() // 2)
        self.pic.setY(-pix.height() // 2)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        # установить смещение изображения от начала координат сцены
        # self.pic.setOffset(-pix.width()//2, -pix.height()//2)

        # self.text = QGraphicsTextItem()
        # self.text.setPlainText('Hello QGraphicsPixmapItem')
        # self.text.setDefaultTextColor(QColor('#91091e'))        # для установки цвета текста
        # # setPos - для установки положения текстовых примитивов относительно начала координат сцены
        # self.text.setPos(130, 230)

        self.scene.addItem(self.pic)
        # self.scene.addItem(self.text)
        self.setScene(self.scene)


    def setSibling(self, sibling):
        if isinstance(sibling, PreviewWidget):
            self.pic.setSibling(sibling.pic)
        else:
        #if isinstance(sibling, PreviewWidgetWithProgressBar):
            self.pic.setSibling(sibling.ui.graphicsView.pic)

    def updatePicBorder(self):
        self.pic.setBorder(self.width(), self.height())
        # print(f'updatePicBorder: x = {self.x()}, y = {self.y()}, width = {self.width()}, height = {self.height()}')
        # print(f'{self.sizePolicy()}, {self.sizeAdjustPolicy()}, {self.minimumSize()}')

    def setSceneRectFromSize(self):
        self.scene.setSceneRect(0, 0, self.width(), self.height())


    def resizeEvent(self, event):
        self.setSceneRectFromSize()
        self.updatePicBorder()
        return super(PreviewWidget, self).resizeEvent(event)

    def boundingRect(self):
        return QRectF(-10, -10, 50, 50)

    def wheelEvent(self, event):
        pass
