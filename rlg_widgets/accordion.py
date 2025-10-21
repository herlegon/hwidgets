from .scroll_area_widget import ScrollAreaWidget
from .scroll_v_layout import ScrollVLayout
from .scrollbar import Scrollbar
from .accordion_item import ACCORDION_RADIUS, AccordionItem

from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QResizeEvent,
)
from PySide6.QtWidgets import (
    QSizePolicy,
    QWidget,
    QScrollArea,
    QFrame,
    QSpacerItem,
)

from utils.pretty_print import *



class Accordion(QScrollArea):

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        self.setObjectName("_accordion")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        scrollbar_width = 8
        self._items: list[AccordionItem] = []

        self._widget = ScrollAreaWidget(self)
        self._widget.setObjectName("_widget")
        if True:
            self._layout: ScrollVLayout = ScrollVLayout(self._widget)
            self._layout.setContentsMargins(
                ACCORDION_RADIUS,
                ACCORDION_RADIUS,
                0,
                ACCORDION_RADIUS
            )
        else:
            # For Debug
            self._layout = ScrollVBoxLayout(self._widget)
            self._layout.setContentsMargins(
                ACCORDION_RADIUS,
                0,
                0,
                0
            )
        self._layout.setSpacing(6)
        self._widget.setLayout(self._layout)
        self.setWidget(self._widget)

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollbar = Scrollbar(self)
        self.setVerticalScrollBar(scrollbar)
        self.verticalScrollBar().setFixedWidth(scrollbar_width)
        self.setWidgetResizable(True)
        # self.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self._layout.addItem(QSpacerItem(10, 1, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))
        # self.verticalScrollBar().installEventFilter(self)

        self.bgd_color = "#7F7F7F"

        self.setStyleSheet(
            """
                #{accordion_name} {{
                    background-color: {bgd_color};
                    color: {color};
                    border-radius: {radius}px;
                    padding: {radius}px;
                    padding-left: 0px;
                    padding-right: {padding_right}px;
                    margin-right: 0px;
                }}
                #{widget_name} {{
                    background-color: transparent;
                }}
            """.format(
            accordion_name=self.objectName(),
            widget_name=self._widget.objectName(),
            radius=ACCORDION_RADIUS,
            bgd_color=self.bgd_color,
            padding_right=ACCORDION_RADIUS/2,
            color="#F0F0F0",
        ))


    def addItem(self, item: AccordionItem) -> None:
        if item.parent() != self:
            item.setParent(self)
        item.setContainerBackgroundColor(self.bgd_color)
        item.setExpanded(False)
        self._layout.insertWidget(len(self._items), item)
        item.setWidth(self.viewport().width())
        self._items.append(item)
        item.installEventFilter(self)
        self.adjustSize()


    def resizeEvent(self, event: QResizeEvent) -> None:
        self._widget.setFixedWidth(self.width() - 2*ACCORDION_RADIUS)
        for item in self._items:
            item.setWidth(self.viewport().width())
        return super().resizeEvent(event)
