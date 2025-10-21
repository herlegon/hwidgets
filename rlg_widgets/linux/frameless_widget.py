from __future__ import annotations
from pprint import pprint
from time import time
from typing import Optional

from ..window.rlg_window_base import RlgWindowBase

from ..colors import (
    tuple_to_css,
)
from ..utils import (
    EDGE_TO_CURSOR_SHAPE,
    GRIP_BORDER_SIZE,
)
from ..title_bar import (
    TOOLBAR_HEIGHT,
    OsStyle,
    TitleBar,
)
from PySide6.QtCore import (
    QCoreApplication,
    QEvent,
    QObject,
    QPoint,
    Qt,
    QRect,
    QMargins,
    QSize,
)
from PySide6.QtGui import (
    QMouseEvent,
    QGuiApplication,
    QPaintEvent,
    QResizeEvent,
    QColor,
    QPainter,
)
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QSpacerItem,
    QLabel,
    QSizePolicy,
    QMainWindow,
    QGraphicsDropShadowEffect,
)


class FramelessWidget(QMainWindow, RlgWindowBase):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        QMainWindow.__init__(self)
        RlgWindowBase.__init__(self)


    def initialize(self) -> None:
        if self.titlebar is None:
            raise ValueError("Titlebar must be defined before calling this method")

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        # To enable system dropShadowEffect on Linux, TranslucentBackground has to be disabled,
        # * however, in this case, having round corners is not possible
        # * embedding a dropShadowEffect requires to set the content margins of the higher layout.
        #   In this case, snap is not working well because the geometry corresponds to
        #   the widget and not to the main frame.
        # Choice: no dropShadow
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        QCoreApplication.instance().installEventFilter(self)


    def moving_event(self, enabled: bool) -> None:
        if enabled:
            self.windowHandle().startSystemMove()
        self.moving = enabled


    def update_style(self, window_state: Qt.WindowState | None = None) -> None:
        raise NotImplementedError("This method shall be defined in child")


    def update_window_state(self):
        # Unused because unable to get taskbar size
        x, y = self.pos().toTuple()
        x0, y0, x1, y1 = self.windowHandle().screen().geometry().getCoords()
        # print(f"coord: {self.windowHandle().screen().geometry()}")
        x, y = min(max(x, x0), x1 + 1), min(max(y, y0), y1 + 1)
        # Under Linux, too complicated to get the application bar size
        threshold: QSize = QGuiApplication.screenAt(QPoint(x, y)).size() * 4 / 5
        if all([a > b for a, b in zip(self.size().toTuple(), threshold.toTuple())]):
            self.update_style(Qt.WindowState.WindowMaximized)
        else:
            self.update_style(Qt.WindowState.WindowNoState)


    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        event_type = event.type()

        if not self.moving and watched in (self, self.titlebar):
            if event_type == QEvent.Type.WindowActivate:
                self.titlebar.set_active(True)
            elif event_type == QEvent.Type.WindowDeactivate and not self.resizing:
                self.titlebar.set_active(False)

        # When moving this window, border radius has to be removed
        # when snap to full available geometry
        # Disabled because modifying stylesheet in Qt and detection
        # of taskbar size is not reliable
        # if self.moving and isinstance(event, QResizeEvent):
        #     self.update_window_state()

        # print(f"{time()} 0x{event_type:02x}")
        if event_type == QEvent.Type.WindowActivate:
            self.update_style()

        # Size changed
        if event_type == QEvent.Type.WindowStateChange:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.titlebar.setCursor(Qt.CursorShape.ArrowCursor)
            self.update_style()
            return False

        # Resize or move
        if (event_type not in [QEvent.Type.MouseButtonPress, QEvent.Type.MouseMove]
            or not self.resizable):
            return False

        cursor_position: QPoint = (event.globalPosition() - self.pos()).toPoint()
        if self.windowState() == Qt.WindowState.WindowNoState:
            ngrip_area: QRect = (
                self.rect()
                - QMargins(GRIP_BORDER_SIZE, GRIP_BORDER_SIZE, GRIP_BORDER_SIZE, GRIP_BORDER_SIZE)
            )
            if ngrip_area.contains(cursor_position) or self.titlebar.is_cursor_over_buttons():
                self.setCursor(Qt.CursorShape.ArrowCursor)
                self.titlebar.setCursor(Qt.CursorShape.ArrowCursor)
                return False

            near_edges = Qt.Edge(0)
            x, y = cursor_position.toTuple()
            if x < ngrip_area.left():
                near_edges |= Qt.Edge.LeftEdge
            elif x > ngrip_area.right():
                near_edges |= Qt.Edge.RightEdge
            if y < ngrip_area.top():
                near_edges |= Qt.Edge.TopEdge
            elif y > ngrip_area.bottom():
                near_edges |= Qt.Edge.BottomEdge

            if near_edges and event_type == QEvent.Type.MouseButtonPress:
                self.windowHandle().startSystemResize(near_edges)
                self.resizing = True
                return True

            elif event_type == QEvent.Type.MouseMove:
                cursor_shape = EDGE_TO_CURSOR_SHAPE.get(near_edges, Qt.CursorShape.ArrowCursor)
                self.setCursor(cursor_shape)
                self.titlebar.setCursor(cursor_shape)

        return False
