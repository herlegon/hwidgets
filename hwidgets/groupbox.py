from string import Template
from typing import Type
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtWidgets import (
    QGroupBox,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QLabel,
)
from .style_manager import Theme
from .utils import load_qss


class HGroupBox(QGroupBox):
    def __init__(
        self,
        /,
        parent: QWidget | None = ...,
        *,
        theme: Type[Theme],
        title: str | None = None,
        alignment: Qt.AlignmentFlag | None = ...,
        flat: bool | None = ...,
        checkable: bool | None = ...,
        checked: bool | None = ...
    ) -> None:

        super().__init__(parent)

        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setCheckable(False)
        self.setTitle(title)

        qss_template = Template(load_qss("groupbox.css"))
        title_left_adjust = 0
        radius: int = theme.default.radius
        qss = qss_template.substitute(
            window_bgd=f"{theme.window_bgd}",
            widget_bgd=f"{theme.window_bgd}",
            font_color=f"{theme.default.font_color}",
            radius=f"{theme.default.radius}",
            border_color=f"{theme.default.border}",
            margin_top=f"{int(radius + theme.groupbox.height) - 1}",
            disabled_text=f"{theme.default.font_color_disabled}",
            widget_disabled=f"{theme.window_bgd}",
            padding=f"{radius + title_left_adjust}",
            title_margins=f"{title_left_adjust}",
        )
        self.setStyleSheet(qss)
        self.setFont(theme.default.font.make_font())

        self.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.adjustSize()



