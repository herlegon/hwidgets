
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
    QPaintEvent,
    QResizeEvent,
    QPalette,
    QBrush,
    QPainter,
)
from PySide6.QtWidgets import (
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QFrame,
    QSpacerItem,
    QLayout,
    QLayoutItem,
    QBoxLayout,
    QScrollBar
)

from rlg_widgets.accordion_item import ACCORDION_RADIUS



SCROLLBAR_STYLESHEET = """
    QScrollBar:vertical {{
        background-color: {track_bgd};
        margin-top: {widget_margin}px;
        margin-bottom: {widget_margin}px;
        border-radius: {track_radius}px;
        width:{track_width}px;
    }}

    QScrollBar:handle:vertical {{
        background-color: {handle_bgd};
        border-radius: {handle_radius}px;
        width:{handle_width}px;
        border: 0px;
    }}

    QScrollBar:handle:vertical:hover {{
        background-color: {handle_bgd_hover};
        width:{handle_width}px;
        border: 0px;
    }}

    QScrollBar::add-line:vertical {{
        height: 0px;
    }}

    QScrollBar:sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar:add-page:vertical, QScrollBar:sub-page:vertical {{
        height: 0px;
        background: none;
    }}
"""


class Scrollbar(QScrollBar):
    def __init__(
        self,
        parent: QWidget
    ) -> None:
        super().__init__(parent)
        self._update_stylesheet()


    def _update_stylesheet(self) -> None:
        stylesheet = SCROLLBAR_STYLESHEET.format(
            track_bgd="#3A3A3A",
            widget_margin=1,
            track_width=self.width(),
            track_radius=int(self.width()/2),
            handle_width=self.width(),
            handle_radius=int(self.width() / 2),
            handle_bgd="#505050",
            handle_bgd_hover="#606060",
        )
        self.setStyleSheet(stylesheet)


    def setFixedWidth(self, w: int) -> None:
        super().setFixedWidth(w)
        self._update_stylesheet()
