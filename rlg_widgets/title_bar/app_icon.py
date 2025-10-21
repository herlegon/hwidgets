from __future__ import annotations
import os
from pathlib import Path

from .style import TitleBarColors
from ..utils import TitleBarStyle

from PySide6.QtCore import (
    Qt,
    QSize,
    QRect,
    QPoint,
)
from PySide6.QtGui import (
    QPaintEvent,
    QPixmap,
    QPainter,
    QImage,
)
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
)


_APP_ICON_STYLESHEET = """
    #{name} {{
        background-color: {bgd};
        border-top: {border}px solid;
        border-color: {border_color};
    }}
    #{name}:disabled {{
        background-color: {bgd_inactive};
        border-top: {border}px solid;
        border-color: {bgd_inactive};
    }}
"""


class AppIcon(QLabel):
    def __init__(
        self,
        parent: QWidget,
        size: QSize = QSize(16, 16),
        right_margin: int = 0,
    ):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setObjectName("__app_icon")

        self.wstate: str = 'windowed'
        self.border_color = TitleBarStyle.border_color
        self.border_width = TitleBarStyle.border_width
        self.bgd_color = TitleBarStyle.bgd
        self.bgd_color_inactive = TitleBarStyle.bgd_inactive
        self._update_stylesheet()

        # Default transparent icon
        self.icon_size: QSize = size
        qimage = QImage(self.icon_size, QImage.Format.Format_ARGB32)
        self.set_icon(QPixmap().fromImage(qimage))
        x, y  = ((self.size() - self.icon.size())/2).toTuple()
        self.pixmap_origin = QPoint(max(0, int(x)), max(0, int(y)))

        self.setFixedSize(size.width() + right_margin, size.height())


    def set_icon(self, icon: str | Path | QPixmap) -> None:
        if isinstance(icon, str | Path):
            if not os.path.exists(icon):
                raise ValueError(f"{icon} not found")
            icon = QPixmap(icon)
        if icon.size() != self.icon_size:
            icon = icon.scaled(
                self.icon_size,
                aspectMode=Qt.AspectRatioMode.IgnoreAspectRatio
            )
        self.icon = icon
        self.icon_rect = QRect(0, 0, icon.size().width(), icon.size().height())
        x, y  = ((self.size() - self.icon.size())/2).toTuple()
        self.pixmap_origin = QPoint(max(0, int(x)), max(0, int(y)))


    def set_size(self, size: QSize) -> None:
        self.setFixedSize(size)
        super().setAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )


    def _update_stylesheet(self) -> None:
        self.stylesheets: dict[str, str] = {
            'windowed': _APP_ICON_STYLESHEET.format(
                    name=self.objectName(),
                    bgd=self.bgd_color,
                    border=self.border_width,
                    border_color=self.border_color,
                    bgd_inactive=self.bgd_color_inactive,
                ),
            'maximized': _APP_ICON_STYLESHEET.format(
                    name=self.objectName(),
                    bgd=self.bgd_color,
                    border=0,
                    border_color=self.border_color,
                    bgd_inactive=self.bgd_color_inactive,
                ),
        }


    def set_style(self, style: dict) -> None:
        colors: TitleBarColors = style['titlebar']
        self.bgd_color = colors.background
        self.bgd_color_inactive = colors.background_inactive
        self.border_width = style['window']['border_width']
        self.border_color = style['window']['border_color']
        self._update_stylesheet()
        self.setStyleSheet(self.stylesheets[self.wstate])
        self.update()


    def set_window_state(self, state: str) -> None:
        # Faster and timing more reproducible than using custom property in stylesheet
        self.wstate = state
        self.setStyleSheet(self.stylesheets[self.wstate])
        self.update()


    def set_active(self, enabled: bool) -> None:
        self.setEnabled(enabled)


    def paintEvent(self, event: QPaintEvent) -> None:
        painter: QPainter = QPainter(self)
        painter.drawPixmap(self.pixmap_origin, self.icon)


