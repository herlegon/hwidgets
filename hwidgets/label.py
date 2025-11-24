from string import Template
from typing import Type
from .style_manager import Theme
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
        theme: Type[Theme],
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

        self.theme = theme
        # self.setSizePolicy(
        #     QSizePolicy(self.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Fixed)
        # )
        self.setMinimumWidth(theme.common.height)
        if text and '\n' not in text:
            self.setFixedHeight(theme.common.height)
        else:
            self.setSizePolicy(
                QSizePolicy(self.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Preferred)
            )

        qss_template = Template(load_qss("label.css"))
        qss = qss_template.substitute(
            window_bgd=f"{theme.window_bgd}",
            widget_bgd=f"{theme.common.bgd}",
            radius=f"{theme.common.radius}px",
            disabled_text=f"{theme.common.font_color_disabled}",
            font_color=f"{theme.label.font_color}",
            font_family=f"\"{theme.label.font.family}\"",
            font_size=f"{theme.label.font.size}pt",
        )
        self.setStyleSheet(qss)


    def setText(self, text: str) -> None:
        super().setText(text)
        if text and '\n' not in text:
            self.setFixedHeight(self.theme.common.height)
        else:
            self.setSizePolicy(
                QSizePolicy(self.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Preferred)
            )
        self.setMinimumWidth(self.sizeHint().width())



class HSubtitle(HLabel):
    def __init__(self, /, parent = ..., f = ..., *, theme, text = None, textFormat = None, pixmap = None, scaledContents = None, alignment = None, wordWrap = None, margin = None, indent = None, openExternalLinks = None, textInteractionFlags = None, hasSelectedText = None, selectedText = None):
        super().__init__(parent, f, theme=theme, text=text, textFormat=textFormat, pixmap=pixmap, scaledContents=scaledContents, alignment=alignment, wordWrap=wordWrap, margin=margin, indent=indent, openExternalLinks=openExternalLinks, textInteractionFlags=textInteractionFlags, hasSelectedText=hasSelectedText, selectedText=selectedText)

        qss_template = Template(load_qss("label.css"))
        qss = qss_template.substitute(
            window_bgd=f"{theme.window_bgd}",
            widget_bgd=f"{theme.common.bgd}",
            radius=f"{theme.common.radius}px",
            disabled_text=f"{theme.common.font_color_disabled}",
            font_color=f"{theme.subtitle.font_color}",
            font_family=f"\"{theme.subtitle.font.family}\"",
            font_size=f"{theme.subtitle.font.size}pt",
        )
        self.setStyleSheet(qss)



class HComment(HLabel):
    def __init__(self, /, parent = ..., f = ..., *, theme, text = None, textFormat = None, pixmap = None, scaledContents = None, alignment = None, wordWrap = None, margin = None, indent = None, openExternalLinks = None, textInteractionFlags = None, hasSelectedText = None, selectedText = None):
        super().__init__(parent, f, theme=theme, text=text, textFormat=textFormat, pixmap=pixmap, scaledContents=scaledContents, alignment=alignment, wordWrap=wordWrap, margin=margin, indent=indent, openExternalLinks=openExternalLinks, textInteractionFlags=textInteractionFlags, hasSelectedText=hasSelectedText, selectedText=selectedText)

        qss_template = Template(load_qss("label.css"))
        qss = qss_template.substitute(
            window_bgd=f"{theme.window_bgd}",
            widget_bgd=f"{theme.common.bgd}",
            radius=f"{theme.common.radius}px",
            disabled_text=f"{theme.common.font_color_disabled}",
            font_color=f"{theme.comment.font_color}",
            font_family=f"\"{theme.comment.font.family}\"",
            font_size=f"{theme.comment.font.size}pt",
        )
        self.setStyleSheet(qss)
