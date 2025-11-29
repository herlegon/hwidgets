from string import Template
from typing import Type

from PySide6.QtCore import (
    Qt,
)
from PySide6.QtWidgets import (
    QWidget,
    QPlainTextEdit,
)

from .plain_text_edit import (
    HPlainTextEdit,
    OverlayVScrollBar,
)
from .style_manager import Theme
from .utils import (
    load_png_icon,
    load_qss,
)




class HLogViewer(HPlainTextEdit):

    def __init__(
        self,
        text: str | QWidget | None = None,
        /,
        parent: QWidget | None = None,
        *,
        theme: Type[Theme],
        tabChangesFocus: bool | None = None,
        documentTitle: str | None = None,
        undoRedoEnabled: bool | None = None,
        lineWrapMode: QPlainTextEdit.LineWrapMode | None = None,
        readOnly: bool | None = None,
        plainText: str | None = None,
        overwriteMode: bool | None = None,
        tabStopDistance: float | None = None,
        cursorWidth: int | None = None,
        textInteractionFlags: Qt.TextInteractionFlag | None = None,
        blockCount: int | None = None,
        maximumBlockCount: int | None = None,
        backgroundVisible: bool | None = None,
        centerOnScroll: bool | None = None,
        placeholderText: str | None = None,
        clearButtonEnabled: bool = True,
    ) -> None:
        self.theme = theme
        self.log_style = theme.log_viewer

        super().__init__(
            parent=parent,
            theme=theme,
            tabChangesFocus=True,
            documentTitle=documentTitle,
            undoRedoEnabled=False,
            lineWrapMode=True,
            readOnly=True,
            plainText=plainText,
            clearButtonEnabled=False,
        )
        self.setContentsMargins(20, 0, 20, 10)
        self._update_stylesheet()


    def _update_stylesheet(self) -> None:
        log_style = self.log_style
        radius = self.theme.default.radius

        padding_left, padding_right = radius, radius

        # Same style sheet as line edit
        qss_template = Template(load_qss("plain_text_edit.qss"))
        qss = qss_template.substitute(
            radius=f"{radius}px",
            padding_right=f"{padding_right}px",
            padding_left=f"{padding_left}px",

            widget_bgd=f"{log_style.bgd}",
            hover=f"{log_style.hover}",
            disabled=f"{log_style.disabled}",

            border_color=f"{log_style.border}",
            border_read_only_color=f"{log_style.border_read_only}",
            border_edition=f"{log_style.selection}",

            selection=f"{log_style.selection}",

            font_family=f"{log_style.font.family}",
            font_size=f"{log_style.font.size}pt",
            font_weight=f"{log_style.font.weight}",
            font_color=f"{log_style.font_color}",
            font_color_disabled=f"{log_style.font_color_disabled}",
        )
        self.setStyleSheet(qss)

