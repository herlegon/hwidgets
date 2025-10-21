from __future__ import annotations
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


_MINIMIZE_BUTTON_STYLESHEET =  """
    #{name} {{
        background-color: {bgd};
        border-top: {border}px solid;
        border-color: {border_color};
    }}
    #{name}:hover {{
        background-color: {bgd_hover};
        border-top: 0px solid;
    }}
    #{name}:disabled {{
        background-color: {bgd_inactive};
        border-top: 0px solid;
    }}
"""


class MinimizeButton(QPushButton):
    signal_entered = Signal()
    signal_leaved = Signal()

    def __init__(
        self,
        parent: Optional[QWidget],
    ) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFlat(True)
        self.setFixedSize(QSize(CONTROL_BUTTON_WIDTH, CONTROL_BUTTON_HEIGHT))
        self.setObjectName("minimize_button")

        self.wstate = 'windowed'
        self._is_over: bool = False
        self.border_color = TitleBarStyle.border_color
        self.border_width = TitleBarStyle.border_width
        self.bgd_color = TitleBarStyle.bgd
        self.bgd_color_hover = TitleBarStyle.bgd_hover
        self.bgd_color_inactive = TitleBarStyle.bgd_inactive


    def _update_stylesheet(self) -> None:
        self.stylesheets: dict[str, str] = {
            'windowed':
               _MINIMIZE_BUTTON_STYLESHEET.format(
                    name=self.objectName(),
                    bgd=self.bgd_color,
                    bgd_hover=self.bgd_color_hover,
                    bgd_inactive=self.bgd_color_inactive,
                    border=self.border_width,
                    border_color=self.border_color,
                ),
            'maximized':
                _MINIMIZE_BUTTON_STYLESHEET.format(
                    name=self.objectName(),
                    bgd=self.bgd_color,
                    bgd_hover=self.bgd_color_hover,
                    bgd_inactive=self.bgd_color_inactive,
                    border=0,
                    border_color=self.border_color,
                ),
        }


    def set_style(self, style: dict) -> None:
        colors: TitleBarColors = style['titlebar']
        self.bgd_color = colors.background
        self.bgd_color_hover = colors.button_hover
        self.bgd_color_inactive = colors.background_inactive
        button_color = QColor(*css_to_tuple(colors.button_color))
        self.border_width = style['window']['border_width']
        self.border_color = style['window']['border_color']

        icon = QIcon()
        icon.addPixmap(
            load_png_icon("minimize.png", button_color),
            QIcon.Mode.Normal, QIcon.State.Off
        )
        self.setIconSize(QSize(CONTROL_BUTTON_WIDTH, CONTROL_BUTTON_HEIGHT))
        self.setIcon(icon)

        self._update_stylesheet()
        self.setStyleSheet(self.stylesheets[self.wstate])
        self.update()


    def enterEvent(self, event):
        self._is_over = True
        self.signal_entered.emit()
        super().enterEvent(event)


    def leaveEvent(self, event: QEvent):
        self._is_over = False
        self.signal_leaved.emit()
        super().leaveEvent(event)


    def is_over(self) -> bool:
        return self._is_over


    def set_window_state(self, state: str) -> None:
        self.wstate = state
        self.setStyleSheet(self.stylesheets[self.wstate])


    def set_active(self, enabled: bool) -> None:
        self.setEnabled(enabled)


