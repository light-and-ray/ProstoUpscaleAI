from fileCard import FileCard


class FileCardsList:
#public:
    def __init__(self, mainWindow, onStart, onCancel):
        self._cards : list[FileCard] = []
        self._mainWindow = mainWindow
        self._onStart = onStart
        self._onCancel = onCancel
        self._selected = None


    def addFileCard(self, imagePath):
        index = len(self._cards)
        card = FileCard(self._mainWindow.ui.scrollAreaWidgetContents, imagePath, index)
        card.setOnStart(self._onStart)
        card.setOnCancel(self._onCancel)

        card.setOnRemove(self.remove)
        card.setOnSelect(self.select)
        self._cards.append(card)
        self._mainWindow.addCard(card)


    def select(self, index, reselect = False):
        if self._selected is not None:
            if self._selected == index and not reselect:
                return
            self._cards[self._selected].setUnselectedColor()

        card = self._cards[index]
        card.setSelectedColor()
        self._selected = index
        self._mainWindow.setPicture(card.getImagePath())

        if card.lastXY is not None:
            self._mainWindow.setXY(*card.lastXY)


    def remove(self, index):
        print('remove', index)
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
                    self._selected = None

        if self._selected is not None:
            self.select(self._selected, True)
        else:
            self._mainWindow.setPicture(None)


#private:

    def _background(self):
        if self._selected is not None:
            card = self._cards[self._selected]
            card.lastXY = self._mainWindow.preview1.picture.getLastXY()

