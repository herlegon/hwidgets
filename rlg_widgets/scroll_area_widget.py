from PySide6.QtCore import (
    QObject,
    Qt,
    QSize,
    QRect,
    QPoint,
    QEvent,
)
from PySide6.QtGui import (
    QColor,
    QMoveEvent,
    QPaintEvent,
    QResizeEvent,
    QPainter,
)
from PySide6.QtWidgets import (
    QSizePolicy,
    QWidget,
    QScrollArea,
    QFrame,
    QSpacerItem,
)

from .scroll_v_layout import ScrollVLayout
from .scrollbar import Scrollbar

from utils.pretty_print import red

from .accordion_item import ACCORDION_RADIUS, AccordionItem




class ScrollAreaWidget(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        # self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.bgd_color = QColor(0,0,0,0)
        self.installEventFilter(self)


    def setBackgroundColor(self, color: str | QColor) -> None:
        self.bgd_color = QColor(color) if isinstance(color, str) else color


    def updateWidgetGeometry(self, rect: QRect) -> None:
        # Known bug: use children: widgets AND items
        layout: ScrollVLayout = self.layout()
        spacing = layout.spacing()
        children = layout.children()
        margins = layout.contentsMargins()

        x = rect.x() + margins.left()
        y = rect.y() + margins.top()
        width = rect.width() - margins.left() - margins.right()
        for i, child in enumerate(children):
            if child.isHidden():
                continue
            y += spacing if i > 0 else 0

            child.setGeometry(
                QRect(QPoint(x, y), QSize(width, child.height()))
            )
            y += child.height()


    def moveEvent(self, event: QMoveEvent) -> None:
        if not isinstance(self.layout(), ScrollVLayout):
            super().moveEvent(event)
        self.updateWidgetGeometry(QRect(event.pos(), self.size()))


    def paintEvent(self, event: QPaintEvent) -> None:
        margins = self.layout().contentsMargins()
        left, top, right, bottom = (
            margins.left(),
            margins.top(),
            margins.right(),
            margins.bottom(),
        )
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.bgd_color)
        painter.drawRoundedRect(
            self.rect().adjusted(left, top, left+right, top+bottom),
            left,
            top
        )


    def resizeEvent(self, event: QResizeEvent) -> None:
        if not isinstance(self.layout(), ScrollVLayout):
            super().resizeEvent(event)
        self.updateWidgetGeometry(QRect(self.pos(), self.size()))


    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        # print(f"{watched} 0x{event.type():02x}")
        if event.type() == QEvent.Type.Resize:
            if watched in self.layout().children():
                # print(f"resizing: {watched}")
                event: QResizeEvent = event
                new_size: QSize = event.size() - event.oldSize()
                if new_size.width() == 0 and new_size.height() != 0:
                    # parent_widget: QWidget = self.parentWidget()
                    self.resize(
                        self.width(),
                        self.height() + new_size.height()
                    )
                    # print(f"resizing: {watched}")
        return super().eventFilter(watched, event)

