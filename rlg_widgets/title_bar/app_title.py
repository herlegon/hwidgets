from __future__ import annotations
from pprint import pprint

from .style import TitleBarColors
from ..utils import TitleBarStyle
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QFont,
)
from PySide6.QtWidgets import (
    QLabel,
    QSizePolicy,
    QWidget,
)


_APP_TITLE_STYLESHEET = """
    #{name} {{
        background-color: {bgd};
        color: {text};
        border-top: {border}px solid;
        border-color: {border_color};
    }}
    #{name}:disabled {{
        background-color: {bgd_inactive};
        color: {text_inactive};
        border-top: {border}px solid;
        border-color: {bgd_inactive};
    }}
"""


class AppTitle(QLabel):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setObjectName("titlebar_title")

        self.wstate = 'windowed'
        self.bgd_color = TitleBarStyle.bgd
        self.bgd_color_inactive = TitleBarStyle.bgd_inactive
        self.text_color_active = TitleBarStyle.text
        self.text_color_inactive = TitleBarStyle.text_inactive
        self.border_width = TitleBarStyle.border_width
        self.border_color = TitleBarStyle.border_color
        self._update_stylesheet()


    def set_text_alignment(self, alignment: Qt.AlignmentFlag) -> None:
        super().setAlignment(alignment)


    def set_size_policy(self, h_policy: QSizePolicy.Policy, v_policy: QSizePolicy.Policy):
        policy = QSizePolicy(h_policy, v_policy)
        self.setSizePolicy(policy)


    def set_font_style(
        self,
        font: QFont | None = None,
        font_size: int = 11,
        bold: bool = False,
        italic: bool = False
    ) -> None:
        if font is None:
            font = QFont()
        title_font:QFont = font
        title_font.setPointSize(font_size)
        title_font.setBold(bold)
        title_font.setItalic(italic)
        self.setFont(title_font)


    def set_text(self, app_title: str) -> None:
        super().setText(app_title)


    def _update_stylesheet(self) -> None:
        self.stylesheets: dict[str, str] = {
            'windowed': _APP_TITLE_STYLESHEET.format(
                name=self.objectName(),
                bgd=self.bgd_color,
                bgd_inactive=self.bgd_color_inactive,
                text=self.text_color_active,
                text_inactive=self.text_color_inactive,
                border=self.border_width,
                border_color=self.border_color,
            ),
            'maximized': _APP_TITLE_STYLESHEET.format(
                name=self.objectName(),
                bgd=self.bgd_color,
                bgd_inactive=self.bgd_color_inactive,
                text=self.text_color_active,
                text_inactive=self.text_color_inactive,
                border=0,
                border_color=self.border_color,
            ),
        }


    def set_style(self, style: dict) -> None:
        colors: TitleBarColors = style['titlebar']
        self.bgd_color = colors.background
        self.bgd_color_inactive = colors.background_inactive
        self.text_color_active = colors.title_color
        self.text_color_inactive = colors.title_color_inactive
        self.border_width = style['window']['border_width']
        self.border_color = style['window']['border_color']
        self._update_stylesheet()
        self.setStyleSheet(self.stylesheets[self.wstate])
        self.update()


    def set_window_state(self, state: str) -> None:
        self.wstate = state
        self.setStyleSheet(self.stylesheets[self.wstate])


    def set_active(self, enabled: bool) -> None:
        self.setEnabled(enabled)
