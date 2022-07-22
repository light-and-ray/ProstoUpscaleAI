from fileCard import FileCard
from mainWindow import MainWindow


class FileCardsList:
#public:
    def __init__(self, mainWindow: MainWindow):
        self._cards : list[FileCard] = []
        self._mainWindow = mainWindow
        self._onStart = None
        self._onCancel = None
        self._onComplete = None
        self._onRemove = None
        self._selected = None
        self._mainWindow.expandListButton.clicked.connect(self._expand)


    def add(self, imagePath):
        index = len(self._cards)
        card = FileCard(self._mainWindow.ui.scrollAreaWidgetContents, imagePath, index)
        card.setOnStart(self._onStart)
        card.setOnCancel(self._onCancel)
        card.setOnComplete(self._onComplete)

        card.setOnRemove(self.remove)
        card.setOnSelect(self.select)
        self._cards.append(card)
        self._mainWindow.addCard(card)

        return index


    def select(self, index, reselect = False):
        if self._selected is not None:
            if not reselect:
                if self._selected == index:
                    return
                self._cards[self._selected].setUnselectedColor()

        card = self._cards[index]
        card.setSelectedColor()
        self._selected = index
        self._mainWindow.setPicture(card.getImagePath(), card.getUpscaleOptions())

        if card.lastXY is not None:
            self._mainWindow.setXY(*card.lastXY)


    def remove(self, index):
        print('remove', index)
        if self._onRemove is not None:
            self._onRemove(index)
        card = self._cards[index]
        self._mainWindow.removeCard(card)
        self._cards.remove(card)

        for i in range (index, len(self._cards)):
            self._cards[i].setIndex(i)

        if self._selected is not None:
            if len(self._cards) == 0:
                self._selected = None
            elif self._selected >= index:
                self._selected -= 1
                if self._selected < 0:
                    self._selected = 0

        if self._selected is not None:
            self.select(self._selected, True)
        else:
            self._mainWindow.setPicture(None, None)


    def setOnStart(self, func):
        self._onStart = func

    def setOnCancel(self, func):
        self._onCancel = func

    def setOnComplete(self, func):
        self._onComplete = func

    def setOnRemove(self, func):
        self._onRemove = func


    def getSelectedCard(self) -> FileCard:
        return self._cards[self._selected]

    def at(self, index) -> FileCard:
        return self._cards[index]


#private:

    def _expand(self):
        self._mainWindow.expandListButton.clicked.disconnect()
        self._mainWindow.expandListButton.clicked.connect(self._squeeze)
        self._mainWindow.expandListButton.setText("Squeeze List")
        self._mainWindow.hidePreviewFrame()


    def _squeeze(self):
        self._mainWindow.expandListButton.clicked.disconnect()
        self._mainWindow.expandListButton.clicked.connect(self._expand)
        self._mainWindow.expandListButton.setText("Expand List")
        self._mainWindow.showPreviewFrame()


    def _fitOneElement(self):
        self._previousHeight = self._mainWindow.scrollArea.height()
        width = self._mainWindow.scrollArea.width()
        height = self._cards[0].height()
        self._mainWindow.scrollArea.setBaseSize(width, height)


    def _background(self):
        if self._selected is not None:
            card = self._cards[self._selected]
            card.lastXY = self._mainWindow.preview1.getLastXY()

