from __future__ import annotations
import sys
from typing import Optional
from .style import TitleBarColors
from ..colors import (
    css_to_tuple
)
from ..utils import (
    CONTROL_BUTTON_HEIGHT,
    CONTROL_BUTTON_WIDTH,
    TitleBarStyle,
    load_png_icon,
)
from PySide6.QtCore import (
    QEvent,
    QPoint,
    QSize,
    Qt,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QIcon,
)
from PySide6.QtWidgets import (
    QPushButton,
    QWidget,
)


_MAXIMIZE_BUTTON_STYLESHEET =  """
    #{name} {{
        background-color: {bgd};
        border-radius: 0px;
        border-top: {border}px solid;
        border-color: {border_color};
    }}
    #{name}:hover {{
        background-color: {bgd_hover};
        border-top: {border}px solid;
        border-color: {border_color};
    }}
    #{name}:disabled {{
        background-color: {bgd_inactive};
        border-top: {border}px solid;
        border-color: {bgd_inactive};
    }}
"""


class MaximizeButton(QPushButton):
    signal_entered = Signal()
    signal_leaved = Signal()

    def __init__(
        self,
        parent: Optional[QWidget],
    ) -> None:
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFlat(True)
        self.setFixedSize(QSize(CONTROL_BUTTON_WIDTH, CONTROL_BUTTON_HEIGHT))
        self.setObjectName("maximize_button")

        self.wstate = 'windowed'
        self._is_over: bool = False
        self.border_color = TitleBarStyle.border_color
        self.border_width = TitleBarStyle.border_width
        self.bgd_color = TitleBarStyle.bgd
        self.bgd_color_hover = TitleBarStyle.bgd_hover
        self.bgd_color_inactive = TitleBarStyle.bgd_inactive
        self._update_stylesheet()


    def _update_stylesheet(self) -> None:
        if sys.platform != 'win32':
            self.stylesheets: dict[str, str] = {
                'windowed': _MAXIMIZE_BUTTON_STYLESHEET.format(
                    name=self.objectName(),
                    bgd=self.bgd_color,
                    bgd_hover=self.bgd_color_hover,
                    bgd_inactive=self.bgd_color_inactive,
                    border=self.border_width,
                    border_color=self.border_color,
                ),
                'maximized': _MAXIMIZE_BUTTON_STYLESHEET.format(
                    name=self.objectName(),
                    bgd=self.bgd_color,
                    bgd_hover=self.bgd_color_hover,
                    bgd_inactive=self.bgd_color_inactive,
                    border=0,
                    border_color=self.border_color,
                ),
            }

        else:
            # Specific to windows
            self.stylesheets: dict[str, dict[str, str]] = {
                'windowed': {
                    'outside':
                        _MAXIMIZE_BUTTON_STYLESHEET.format(
                            name=self.objectName(),
                            bgd=self.bgd_color,
                            bgd_hover=self.bgd_color_hover,
                            bgd_inactive=self.bgd_color_inactive,
                            border=self.border_width,
                            border_color=self.border_color
                        ),
                    'over':
                        _MAXIMIZE_BUTTON_STYLESHEET.format(
                            name=self.objectName(),
                            bgd=self.bgd_color_hover,
                            bgd_hover=self.bgd_color_hover,
                            bgd_inactive=self.bgd_color_inactive,
                            border=self.border_width,
                            border_color=self.border_color,
                        ),
                },
                'maximized': {
                    'outside':
                        _MAXIMIZE_BUTTON_STYLESHEET.format(
                            name=self.objectName(),
                            bgd=self.bgd_color,
                            bgd_hover=self.bgd_color_hover,
                            bgd_inactive=self.bgd_color_inactive,
                            border=0,
                            border_color=self.bgd_color
                        ),
                    'over':
                        _MAXIMIZE_BUTTON_STYLESHEET.format(
                            name=self.objectName(),
                            bgd=self.bgd_color_hover,
                            bgd_hover=self.bgd_color_hover,
                            bgd_inactive=self.bgd_color_inactive,
                            border=0,
                            border_color=self.bgd_color,
                        ),
                }
            }


    def set_style(self, style: dict) -> None:
        colors: TitleBarColors = style['titlebar']
        self.bgd_color = colors.background
        self.bgd_color_hover = colors.button_hover
        self.bgd_color_inactive = colors.background_inactive
        button_color = QColor(*css_to_tuple(colors.button_color))
        self.border_width = style['window']['border_width']
        self.border_color = style['window']['border_color']

        self.maximize_icon = QIcon()
        self.maximize_icon.addPixmap(
            load_png_icon("maximize.png", button_color),
            QIcon.Mode.Normal, QIcon.State.Off)
        self.restore_icon = QIcon()
        self.restore_icon.addPixmap(
            load_png_icon("restore.png", button_color),
            QIcon.Mode.Normal, QIcon.State.Off
        )
        self.setIconSize(QSize(CONTROL_BUTTON_WIDTH, CONTROL_BUTTON_HEIGHT))
        self.setIcon(self.maximize_icon)

        self._update_stylesheet()
        if sys.platform == 'win32':
            self.setStyleSheet(self.stylesheets[self.wstate]['outside'])
        else:
            self.setStyleSheet(self.stylesheets[self.wstate])
        self.update()


    def enterEvent(self, event):
        # Linux only
        self._is_over = True
        self.signal_entered.emit()


    def leaveEvent(self, event: QEvent):
        # Linux only
        self._is_over = False
        self.signal_leaved.emit()


    def is_over(self, cursor_pos: QPoint | None = None) -> bool:
        if cursor_pos is not None:
            return self.rect().contains(cursor_pos - self.geometry().topLeft())
        return self._is_over


    def set_window_state(self, state: str) -> None:
        if state == 'maximized':
            self.setIcon(self.restore_icon)
        else:
            self.setIcon(self.maximize_icon)
        self.wstate = state
        if sys.platform == 'win32':
            self.setStyleSheet(self.stylesheets[self.wstate]['outside'])
        else:
            self.setStyleSheet(self.stylesheets[self.wstate])


    def force_over_state(self, enabled: bool, force: bool = False) -> None:
        # Used on win32 only
        if enabled != self._is_over or force:
            if enabled:
                self.setStyleSheet(self.stylesheets[self.wstate]['over'])
            else:
                self.setStyleSheet(self.stylesheets[self.wstate]['outside'])
        self._is_over = enabled


    def set_active(self, enabled: bool) -> None:
        self.setEnabled(enabled)


    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        event_type: QEvent.Type = event.type()
        if event_type in (QEvent.Type.HoverEnter, event.Type.HoverMove):
            self.entered_event(event)

        return super().eventFilter(watched, event)


