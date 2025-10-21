from __future__ import annotations
from pprint import pprint
import sys
from typing import Literal

from .title_bar import TitleBarColors
from ..utils import TitleBarStyle
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtWidgets import (
    QLabel,
    QSizePolicy,
    QWidget,
)

PAD_SPACE_WIDTH: int = 8 if sys.platform == 'linux' else 16


_PAD_STYLESHEET: str = """
    #{name} {{
        background-color: {bgd};
        border-top-left-radius: {radius_left}px;
        border-top-right-radius: {radius_right}px;
        border-top: {border}px solid;
        border-left: {border_left}px solid;
        border-right: {border_right}px solid;
        border-color: {border_color};
    }}
    #{name}:disabled {{
        background-color: {bgd_inactive};
    }}
"""

class Pad(QLabel):
    def __init__(
        self,
        parent: QWidget,
        border_radius: int,
        height: int,
        side: Literal['left', 'right', 'center'] = 'left',
    ):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setObjectName(f"pad_{side}")
        self.side = side

        self.wstate = 'windowed'
        self.border_radius = border_radius
        self.border_color = TitleBarStyle.border_color
        self.border_width = TitleBarStyle.border_width
        self.bgd_color = TitleBarStyle.bgd
        self.bgd_color_inactive = TitleBarStyle.bgd_inactive
        space_width = max(PAD_SPACE_WIDTH, self.border_radius)
        self.setFixedSize(space_width, height)
        self._update_stylesheet()


    def set_size_policy(self, h_policy: QSizePolicy.Policy, v_policy: QSizePolicy.Policy):
        policy = QSizePolicy(h_policy, v_policy)
        self.setSizePolicy(policy)


    def set_style(self, style: dict) -> None:
        colors: TitleBarColors = style['titlebar']
        self.bgd_color = colors.background
        self.bgd_color_inactive = colors.background_inactive
        self.border_radius = style['window']['border_radius']
        self.border_width = style['window']['border_width']
        self.border_color = style['window']['border_color']
        self._update_stylesheet()
        self.setStyleSheet(self.stylesheets[self.wstate])
        self.update()


    def set_window_state(self, state: str) -> None:
        self.wstate = state
        self.setStyleSheet(self.stylesheets[state])


    def set_active(self, enabled: bool) -> None:
        self.setEnabled(enabled)


    def _update_stylesheet(self) -> None:
        self.stylesheets: dict[str, str] = {
            'windowed': _PAD_STYLESHEET.format(
                name=self.objectName(),
                bgd=self.bgd_color,
                radius_left=self.border_radius if self.side == 'left' else 0,
                radius_right=self.border_radius if self.side == 'right' else 0,
                border=self.border_width,
                border_left=self.border_width if self.side == 'left' else 0,
                border_right=self.border_width if self.side == 'right' else 0,
                border_color=self.border_color,
                bgd_inactive=self.bgd_color_inactive,
            ),
            'maximized': _PAD_STYLESHEET.format(
                name=self.objectName(),
                bgd=self.bgd_color,
                radius_left=0,
                radius_right=0,
                border=0,
                border_left=0,
                border_right=0,
                border_color=self.border_color,
                bgd_inactive=self.bgd_color_inactive,
            ),
        }


