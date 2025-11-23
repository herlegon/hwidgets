from string import Template
from typing import Type
from .hstyle import (
    COMBOBOX_RADIUS,
    COMBOBOX_HEIGHT,
    Theme,
)
from .utils import load_qss

from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QPixmap,
)
from PySide6.QtWidgets import (
    QLabel,
    QSizePolicy,
    QWidget,
)


class HLabel(QLabel):

    def __init__(
        self,
        /,
        parent:QWidget | None = ...,
        f: Qt.WindowType = ...,
        *,
        hstyle: Type[Theme],
        text: str | None = None,
        textFormat: Qt.TextFormat | None = None,
        pixmap: QPixmap | None = None,
        scaledContents: bool | None = None,
        alignment: Qt.AlignmentFlag | None = None,
        wordWrap: bool | None = None,
        margin: int | None = None,
        indent: int | None = None,
        openExternalLinks: bool | None = None,
        textInteractionFlags: Qt.TextInteractionFlag | None = None,
        hasSelectedText: bool | None = None,
        selectedText: str | None = None,
    ) -> None:
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        if text is not None:
            self.setText(text)

        # self.setSizePolicy(
        #     QSizePolicy(self.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Fixed)
        # )
        self.setMinimumWidth(COMBOBOX_RADIUS)
        if text and '\n' not in text:
            self.setFixedHeight(COMBOBOX_HEIGHT)
        else:
            self.setSizePolicy(
                QSizePolicy(self.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Preferred)
            )

        qss_template = Template(load_qss("label.css"))
        qss = qss_template.substitute(
            window_bgd=f"{hstyle.window_bgd}",
            widget_bgd=f"{hstyle.widget_bgd}",
            font_color=f"{hstyle.font_color}",
            radius=f"{COMBOBOX_RADIUS}px",
            disabled_text=f"{hstyle.disabled_text}",
            font_family=f"\"{hstyle.font_family}\"",
            font_size=f"{hstyle.font_size}pt",
        )
        self.setStyleSheet(qss)


    def setText(self, text: str) -> None:
        super().setText(text)
        if text and '\n' not in text:
            self.setFixedHeight(COMBOBOX_HEIGHT)
        else:
            self.setSizePolicy(
                QSizePolicy(self.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Preferred)
            )
        self.setMinimumWidth(self.sizeHint().width())


class HSubtitle(HLabel):
    ...

