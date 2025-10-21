from PySide6.QtCore import (
    QObject,
    Qt,
    QSize,
    QRect,
    QEvent,
)
from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLayout,
    QLayoutItem,
    QBoxLayout,
)


class ScrollVLayout(QLayout):
    """Known bug: use a list of children
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._widgets: list[QWidget] = []
        self._items: list[QLayoutItem] = []


    def maximumSize(self) -> QSize:
        return super().maximumSize()


    def addItem(self, item: QLayoutItem) -> None:
        self._items.append(item)


    def addWidget(self, widget: QWidget) -> None:
        if widget in self._widgets:
            return
        widget.installEventFilter(self.parentWidget())


    def count(self) -> int:
        return len(self._items)


    def direction(self) -> QBoxLayout.Direction:
        return QBoxLayout.Direction.TopToBottom

    def expandingDirections(self) -> Qt.Orientation:
        return Qt.Orientation.Vertical


    def hasHeightForWidth(self) -> bool:
        return True


    def heightForWidth(self, width: int) -> int:
        margins = self.contentsMargins()
        height = margins.top() + margins.bottom()
        widgets = [w for w in self._widgets if w.isVisible()]
        height += self.spacing() * (len(widgets) - 1)
        height += sum([w.height() for w in widgets])
        return height


    def insertWidget(self, index: int, widget: QWidget) -> None:
        self._widgets.insert(index, widget)
        widget.installEventFilter(self.parentWidget())


    def itemAt(self, index: int) -> QLayoutItem | None:
        try:
            return self._items[index]
        except Exception as _:
            pass
        return None


    def children(self) -> list[QWidget | QLayoutItem]:
        # known bug: return widgets AND items
        return self._widgets


    def minimumSize(self) -> QSize:
        size = QSize()
        for widget in self._widgets:
            size = size.expandedTo(widget.minimumSize())
        margins = self.contentsMargins()
        size += QSize(
            margins.left() + margins.right(),
            margins.top() + margins.bottom()
        )
        return size


    def sizeHint(self) -> QSize:
        return self.minimumSize()


    def takeAt(self, index):
        try:
            return self._items.pop(index)
        except Exception as _:
            pass
        return None





class ScrollVBoxLayout(QVBoxLayout):
    """Used for DEBUG"""
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.installEventFilter(self)

    def heightForWidth(self, arg__1: int) -> int:
        print("heightForWidth")
        return super().heightForWidth(arg__1)

    def sizeHint(self) -> QSize:
        # print("sizeHint")
        return super().sizeHint()

    def invalidate(self) -> None:
        print("invalidate")
        return super().invalidate()

    def update(self) -> None:
        print("update")
        return super().update()

    def widgetEvent(self, arg__1: QEvent) -> None:
        print("widgetEvent")
        return super().widgetEvent(arg__1)

    def setGeometry(self, arg__1: QRect) -> None:
        # print("setGeometry")
        return super().setGeometry(arg__1)


    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        print(f"{watched} 0x{event.type():02x}")
        return super().eventFilter(watched, event)

