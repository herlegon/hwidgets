from string import Template
from .hstyle import (
    COMBOBOX_RADIUS,
    COMBOBOX_HEIGHT,
    HStyle,
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
        hstyle: HStyle,
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
        self.setFixedHeight(COMBOBOX_HEIGHT)

        qss_template = Template(load_qss("label.css"))
        qss = qss_template.substitute(
            window_bgd=f"{hstyle.window_bgd}",
            widget_bgd=f"{hstyle.widget_bgd}",
            text_color=f"{hstyle.text_color}",
            radius=f"{COMBOBOX_RADIUS}px",
            disabled_text=f"{hstyle.disabled_text}",
        )
        self.setStyleSheet(qss)


    def setText(self, text: str) -> None:
        super().setText(text)
        self.setMinimumWidth(self.sizeHint().width())
