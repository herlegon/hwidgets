from __future__ import annotations
import os
from pathlib import Path
from pprint import pprint
import sys
from typing import Literal

from .style import TOOLBAR_HEIGHT, TitleBarColors

from .pad import PAD_SPACE_WIDTH, Pad
from .app_title import AppTitle
from .app_icon import AppIcon

from ..utils import TitleBarStyle
from .close_button import CloseButton
from .maximize_button import MaximizeButton
from .minimize_button import MinimizeButton
if sys.platform == "darwin":
    from .darwin.utils import MoveResize

from PySide6.QtCore import (
    QEvent,
    Qt,
    Signal,
    QPoint,
    QSize,
)
from PySide6.QtGui import (
    QMouseEvent,
    QPixmap,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QSizePolicy,
    QWidget,
    QSpacerItem,
)


OsStyle = Literal['macos', 'linux', 'windows']


_TITLEBAR_STYLESHEET = """
    #{name} {{
        background-color: {bgd};
        border-top-left-radius: {radius}px;
        border-top-right-radius: {radius}px;
        border-left: {border}px solid;
        border-right: {border}px solid;
        border-top: {border}px solid;
        border-color: {border_color};
    }}
    #{name}:disabled {{
        background-color: {bgd_inactive};
    }}
"""


# Title bar design:
# https://learn.microsoft.com/en-us/windows/apps/design/basics/titlebar-design
# https://developer.apple.com/design/human-interface-guidelines/windows

class TitleBar(QWidget):
    signal_close = Signal()
    signal_minimize = Signal()
    signal_maximize_clicked = Signal()
    signal_moving_started = Signal()
    signal_is_moving = Signal(bool)
    signal_is_pressed = Signal()
    signal_double_clicked = Signal()

    CONTROL_BUTTON_WIDTH: int = 46
    APP_ICON_SIZE = 16
    APP_ICON_RIGHT_MARGIN: int = 16 if sys.platform == 'win32' else 16


    def __init__(
        self,
        parent: QWidget | None = None,
        resizable: bool = True,
        border_radius: int = 12,
        close_border_size: int = 0,
        os_style: OsStyle = 'linux',
    ) -> None:
        super().__init__(parent)
        self.setObjectName("titlebar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setCursor(Qt.CursorShape.ArrowCursor)

        self.os_style = os_style
        self.bgd_color = (127, 127, 127)
        self.border_color = self.bgd_color
        self.border_width = 0
        self.border_radius = border_radius
        self.is_active: bool = False

        self.setFixedHeight(TOOLBAR_HEIGHT)
        self.main_layout: QHBoxLayout = QHBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Left padding
        self.left_pad: Pad = Pad(
            self,
            border_radius=border_radius,
            height=TOOLBAR_HEIGHT,
            side='left'
        )
        self.right_pad: Pad | None = None

        self.app_icon: AppIcon = AppIcon(
            self,
            QSize(self.APP_ICON_SIZE, self.APP_ICON_SIZE),
            right_margin = self.APP_ICON_RIGHT_MARGIN
        )
        self.app_icon.set_size(
            QSize(self.APP_ICON_SIZE + self.APP_ICON_RIGHT_MARGIN, TOOLBAR_HEIGHT))

        self.app_title: AppTitle = AppTitle(self)
        self.app_title.set_text("")
        if os_style == 'windows':
            self.app_title.set_text_alignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.app_title.set_size_policy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        elif os_style == 'linux':
            self.app_title.set_text_alignment(Qt.AlignmentFlag.AlignCenter)
            self.app_title.set_size_policy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        elif os_style == 'macos':
            self.app_title.set_text_alignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.app_title.set_size_policy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)

        # Control buttons
        self.control_layout: QHBoxLayout = QHBoxLayout()
        self.control_layout.setSpacing(0)
        self.control_layout.setContentsMargins(0, 0, 0, 0)
        self.control_buttons: list[CloseButton | MinimizeButton | MaximizeButton] = []
        self.minimize_button: MinimizeButton | None = None
        self.maximize_button: MaximizeButton | None = None
        if resizable:
            self.minimize_button = MinimizeButton(self)
            self.maximize_button = MaximizeButton(self)
            self.control_layout.addWidget(self.minimize_button)
            self.control_layout.addWidget(self.maximize_button)
            self.control_buttons += (self.minimize_button, self.maximize_button)
            self.minimize_button.clicked.connect(self.minimize_button_clicked)
            self.maximize_button.clicked.connect(self.maximize_button_clicked)
        self.close_button = CloseButton(self,
            border_radius=border_radius,
            grip_size=close_border_size,
        )
        self.control_layout.addWidget(self.close_button)
        self.control_buttons.append(self.close_button)

        self.main_layout.addWidget(self.left_pad)
        if os_style == 'windows':
            self.main_layout.addWidget(self.app_icon)
            self.main_layout.addWidget(self.app_title)
            self.main_layout.addLayout(self.control_layout)

        elif os_style == 'macos':
            # Right padding
            self.right_pad: Pad = Pad(
                self,
                border_radius=border_radius,
                height=TOOLBAR_HEIGHT,
                side='right'
            )
            app_right_padding = (
                max(PAD_SPACE_WIDTH, border_radius)
                + self.CONTROL_BUTTON_WIDTH * len(self.control_buttons)
            )
            self.right_pad.setFixedSize(app_right_padding, TOOLBAR_HEIGHT)
            self.main_layout.addLayout(self.control_layout)
            self.main_layout.addItem(QSpacerItem(1, TOOLBAR_HEIGHT, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
            self.main_layout.addWidget(self.app_icon)
            self.main_layout.addWidget(self.app_title)
            self.main_layout.addItem(QSpacerItem(1, TOOLBAR_HEIGHT, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
            self.main_layout.addWidget(self.right_pad)

        elif os_style == 'linux':
            self.app_title_left_padding_width = (
                (self.CONTROL_BUTTON_WIDTH * len(self.control_buttons))
                - max(PAD_SPACE_WIDTH, border_radius)
                - self.APP_ICON_SIZE
                - self.APP_ICON_RIGHT_MARGIN
            )
            self.main_layout.addWidget(self.app_icon)
            self.app_title.setContentsMargins(self.app_title_left_padding_width,0,0,0)
            self.main_layout.addWidget(self.app_title)
            self.main_layout.addLayout(self.control_layout)
        else:
            raise ValueError(f"{os_style} is not a valid key")

        self.widgets = [
            self.app_title,
            self.app_icon,
            self.left_pad,
            self.minimize_button,
            self.maximize_button,
            self.close_button,
        ]
        if os_style == 'macos':
            self.widgets.append(self.right_pad)

        self.bgd_color = TitleBarStyle.bgd
        self.bgd_color_inactive = TitleBarStyle.bgd_inactive
        self.border_color = TitleBarStyle.border_color
        self.border_width = 1
        self.border_radius = 12
        self._update_stylesheet()

        self.close_button.signal_clicked.connect(self.close_button_clicked)
        for w in self.control_buttons:
            w.signal_entered.connect(self.entered_event)


    def _update_stylesheet(self) -> None:
        # Set colors for this frame
        self.stylesheets: dict[str, str] = {
            'windowed': _TITLEBAR_STYLESHEET.format(
                name=self.objectName(),
                bgd=self.bgd_color,
                radius=self.border_radius,
                border=self.border_width,
                border_color=self.border_color,
                bgd_inactive=self.bgd_color_inactive
            ),
            'maximized': _TITLEBAR_STYLESHEET.format(
                name=self.objectName(),
                bgd=self.bgd_color,
                radius=0,
                border=0,
                border_color=self.border_color,
                bgd_inactive=self.bgd_color_inactive
            )
        }


    def set_style(self, style: dict) -> None:
        colors: TitleBarColors = style['titlebar']
        self.bgd_color = colors.background
        self.bgd_color_inactive = colors.background_inactive
        self.border_color = style['window']['border_color']
        self.border_width = style['window']['border_width']
        self.border_radius = style['window']['border_radius']

        for w in self.widgets:
            w.set_style(style)
        self._update_stylesheet()
        self.setStyleSheet(self.stylesheets['windowed'])
        self.update()


    def set_active(self, enabled: bool) -> None:
        if enabled != self.is_active:
            print(f"active: {enabled}")
            # self.setEnabled(enabled)
            for w in self.widgets:
                w.set_active(enabled)
            # self.setEnabled(enabled)
            self.repaint()
        self.is_active = enabled


    def entered_event(self) -> None:
        if sys.platform != 'linux':
            self.setCursor(Qt.CursorShape.ArrowCursor)


    def close_button_clicked(self) -> None:
        self.signal_close.emit()


    def minimize_button_clicked(self, event: QEvent) -> None:
        self.signal_minimize.emit()


    def maximize_button_clicked(self, event: QEvent) -> None:
        self.signal_maximize_clicked.emit()


    def mouseDoubleClickEvent(self, event) -> None:
        self.signal_double_clicked.emit()
        return True


    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if sys.platform == "darwin":
            MoveResize.startSystemMove(self.window(), event.globalPos())


    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.set_active(True)
        if self.is_cursor_over_buttons():
            return
        self.signal_is_pressed.emit()
        self.signal_is_moving.emit(True)


    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.signal_is_moving.emit(False)


    def is_cursor_over_buttons(self) -> bool:
        return True if any([b.is_over() for b in self.control_buttons]) else False


    def is_over(self, cursor_position: QPoint) -> bool:
        if self.rect().contains(cursor_position):
            return True
        return False


    def is_over_maximize_button(self, cursor_pos: QPoint | None = None) -> bool:
        return self.maximize_button.is_over(cursor_pos)


    def set_window_state(self, window_state: Qt.WindowState) -> None:
        state = 'windowed'
        if window_state in (Qt.WindowState.WindowMaximized,
                            Qt.WindowState.WindowFullScreen):
            state = 'maximized'

        self.setStyleSheet(self.stylesheets[state])
        self.left_pad.set_window_state(state)
        self.app_icon.set_window_state(state)
        self.app_title.set_window_state(state)
        if self.maximize_button is not None:
            self.maximize_button.set_window_state(state)
            self.minimize_button.set_window_state(state)
        self.close_button.set_window_state(state)

        if self.right_pad is not None:
            self.right_pad.set_window_state(state)


    def set_title(self, title: str = '') -> None:
        self.app_title.setText(title)
        self.app_title.raise_()


    def set_icon(self, icon: str | Path | QPixmap) -> None:
        if isinstance(icon, str | Path) and not os.path.exists(icon):
            raise ValueError(f"{icon} not found")
        self.app_icon.set_icon(icon)

