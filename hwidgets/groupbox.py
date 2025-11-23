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

from .hstyle import (
    Theme,
    COMBOBOX_RADIUS,
    GROUPBOX_TITLE_HEIGHT,
)
from .utils import load_qss


class HGroupBox(QGroupBox):
    def __init__(
        self,
        /,
        parent: QWidget | None = ...,
        *,
        hstyle: Type[Theme],
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
        qss = qss_template.substitute(
            window_bgd=f"{hstyle.window_bgd}",
            widget_bgd=f"{hstyle.window_bgd}",
            font_color=f"{hstyle.font_color}",
            radius=f"{COMBOBOX_RADIUS}",
            border_color=f"{hstyle.hover_bgd}",
            margin_top=f"{int(COMBOBOX_RADIUS + GROUPBOX_TITLE_HEIGHT) - 1}",
            disabled_text=f"{hstyle.disabled_text}",
            widget_disabled=f"{hstyle.window_bgd}",
            padding=f"{COMBOBOX_RADIUS + title_left_adjust}",
            title_margins=f"{title_left_adjust}",
        )
        self.setStyleSheet(qss)

        self.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.adjustSize()



