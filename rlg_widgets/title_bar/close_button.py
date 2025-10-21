from __future__ import annotations
from pprint import pprint
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
    QMargins,
    QEvent,
    QObject,
    QRect,
    QSize,
    Qt,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QIcon,
    QHoverEvent,
    QMouseEvent,
)
from PySide6.QtWidgets import (
    QPushButton,
    QWidget,
)


class CloseButton(QPushButton):
    signal_entered = Signal()
    signal_leaved = Signal()
    signal_clicked = Signal()

    def __init__(
        self,
        parent: Optional[QWidget],
        border_radius: int = 12,
        grip_size: int = 0
    ) -> None:
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFlat(True)
        self.setFixedSize(QSize(CONTROL_BUTTON_WIDTH, CONTROL_BUTTON_HEIGHT))
        self.setObjectName("close_button")

        self.wstate = 'windowed'
        self.border_color = TitleBarStyle.border_color
        self.border_width = TitleBarStyle.border_width
        self.border_radius = border_radius
        self.bgd_color = TitleBarStyle.bgd
        self.bgd_color_hover = TitleBarStyle.bgd_hover
        self.bgd_color_inactive = TitleBarStyle.bgd_inactive
        self.stylesheets: dict[str, str] = {
            'windowed': "",
            'maximized': "",
        }

        self._is_over: bool = False
        self._mouse_pressed = False

        self.hover_area: QRect = self.rect() - QMargins(0, grip_size, grip_size, 0)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.installEventFilter(self)


    def _update_stylesheet(self) -> None:
        self.stylesheets: dict[str, str] = {
            'windowed': {
                'outside': """
                    #{name} {{
                        background-color: {bgd};
                        border-top-right-radius: {radius}px;
                        border-top-left-radius: 0px;
                        border-bottom-right-radius: 0px;
                        border-bottom-left-radius: 0px;
                        border-top: {border}px solid;
                        border-right: {border}px solid;
                        border-color: {border_color};
                    }}
                    #{name}:disabled {{
                        background-color: {bgd_inactive};
                        border-top: {border}px solid;
                        border-right: {border}px solid;
                        border-color: {bgd_inactive};
                    }}
                """.format(
                    name=self.objectName(),
                    bgd=self.bgd_color,
                    radius=self.border_radius,
                    bgd_inactive=self.bgd_color_inactive,
                    border=self.border_width,
                    border_color=self.border_color
                ),
                'hover': """
                    #{name} {{
                        background-color: {bgd_hover};
                        border-top-right-radius: {radius}px;
                        border-top-left-radius: 0px;
                        border-bottom-right-radius: 0px;
                        border-bottom-left-radius: 0px;
                        border-top: {border}px solid;
                        border-right: {border}px solid;
                        border-color: {bgd_hover};
                    }}
                """.format(
                    name=self.objectName(),
                    bgd_hover=self.bgd_color_hover,
                    radius=self.border_radius,
                    border=self.border_width,
                    bgd_inactive=self.bgd_color_inactive,
                ),
            },
            'maximized': {
                'outside': """
                    #{name} {{
                        background-color: {bgd};
                        border: {border}px;
                        border-radius: 0px;
                    }}
                    #{name}:disabled {{
                        background-color: {bgd_inactive};
                    }}

                """.format(
                    name=self.objectName(),
                    bgd=self.bgd_color,
                    bgd_inactive=self.bgd_color_inactive,
                    border=0,
                ),
                'hover': """
                    #{name} {{
                        background-color: {bgd_hover};
                        border-radius: 0px;
                        border: {border}px;
                    }}
                """.format(
                    name=self.objectName(),
                    bgd_hover=self.bgd_color_hover,
                    border=0,
                    bgd_inactive=self.bgd_color_inactive,
                )
            }
        }


    def set_style(self, style: dict) -> None:
        colors: TitleBarColors = style['titlebar']
        self.bgd_color = colors.background
        self.bgd_color_hover = colors.close_button_hover
        self.bgd_color_inactive = colors.background_inactive
        button_color = QColor(*css_to_tuple(colors.button_color))
        self.border_width = style['window']['border_width']
        self.border_color = style['window']['border_color']

        close_icon = QIcon()
        close_icon.addPixmap(
            load_png_icon("close.png", button_color),
            QIcon.Mode.Normal, QIcon.State.Off
        )
        self.setIconSize(QSize(CONTROL_BUTTON_WIDTH, CONTROL_BUTTON_HEIGHT))
        self.setIcon(close_icon)

        self._update_stylesheet()
        self.setStyleSheet(self.stylesheets[self.wstate]['outside'])
        self.update()


    def entered_event(self, event: QMouseEvent | QHoverEvent) -> None:
        if self.hover_area.contains(event.pos()):
            self.setStyleSheet(self.stylesheets[self.wstate]['hover'])
            if not self._is_over:
                self.signal_entered.emit()
            self._is_over = True
        else:
            self.setStyleSheet(self.stylesheets[self.wstate]['outside'])
            self._is_over = False


    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.entered_event(event)
        return super().mouseMoveEvent(event)


    def leaveEvent(self, event: QEvent):
        self.setStyleSheet(self.stylesheets[self.wstate]['outside'])
        self._is_over = False
        self.signal_leaved.emit()
        super().leaveEvent(event)


    def is_over(self) -> bool:
        return self._is_over


    def set_window_state(self, state: str) -> None:
        self.wstate = state
        self.setStyleSheet(self.stylesheets[self.wstate]['outside'])


    def set_active(self, enabled: bool) -> None:
        self.setEnabled(enabled)


    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self._is_over:
            self._mouse_pressed = True
            return
        return super().mousePressEvent(event)


    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.rect().contains(event.pos())
        if self._mouse_pressed and self._is_over:
            self.signal_clicked.emit()
            self._mouse_pressed = False
            return True
        self._mouse_pressed = False
        return super().mouseReleaseEvent(event)


    def close_button_clicked(self):
        self.signal_clicked.emit()


    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        event_type: QEvent.Type = event.type()
        if event_type in (QEvent.Type.HoverEnter, event.Type.HoverMove):
            self.entered_event(event)

        return super().eventFilter(watched, event)
