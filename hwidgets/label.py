from copy import deepcopy
from string import Template
from typing import Type
from .styles import Theme, FontConfig, weight_from_css
from .utils import load_qss

from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QPixmap,
    QFont,
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
        parent: QWidget | None = None,
        f: Qt.WindowType = None,
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
        self.font_config: FontConfig = deepcopy(theme.label.font)
        self._update_stylesheet()


    def setText(self, text: str) -> None:
        super().setText(text)
        if isinstance(self, HDescription | HComment):
            self.setWordWrap(True)
            self.setSizePolicy(
                QSizePolicy(
                    QSizePolicy.Policy.Preferred,
                    QSizePolicy.Policy.Minimum
                )
            )
            self.setMinimumHeight(0)
            self.adjustSize()
        else:
            if text and '\n' not in text:
                self.setFixedHeight(self.theme.default.height)
            else:
                self.setSizePolicy(
                    QSizePolicy(self.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Preferred)
                )
        self.setMinimumWidth(self.sizeHint().width())


    def setItalic(self, b: bool) -> None:
        self.font_config.style = QFont.Style.StyleItalic if b else QFont.Style.StyleNormal
        self._update_stylesheet()


    def setWeight(self, weight: int | QFont.Weight) -> None:
        if isinstance(weight, int):
            weight = weight_from_css(weight)
        self.font_config.weight = weight
        self._update_stylesheet()


    def setFontSize(self, size: int) -> None:
        self.font_config.size = size
        self._update_stylesheet()


    def _update_stylesheet(self) -> None:
        # Determine which theme style to use based on class
        if isinstance(self, HSubtitle):
            style = self.theme.subtitle
        elif isinstance(self, HComment):
            style = self.theme.comment
        else:
            style = self.theme.label

        qss_template = Template(load_qss("label.css"))
        qss = qss_template.substitute(
            window_bgd=f"{self.theme.window_bgd}",
            widget_bgd=f"{self.theme.default.bgd}",
            radius=f"{self.theme.default.radius}px",

            font_color_disabled=f"{self.theme.default.font_color_disabled}",
            font_color=f"{style.font_color}",
        )
        self.setStyleSheet(qss)
        self.setFont(self.font_config.make_font())



class HDescription(HLabel):
    def __init__(self, /, parent: QWidget | None = None, f: Qt.WindowType = None, *, theme, text = None, textFormat = None, pixmap = None, scaledContents = None, alignment = None, wordWrap = None, margin = None, indent = None, openExternalLinks = None, textInteractionFlags = None, hasSelectedText = None, selectedText = None):
        super().__init__(parent, f, theme=theme, text=text, textFormat=textFormat, pixmap=pixmap, scaledContents=scaledContents, alignment=alignment, wordWrap=wordWrap, margin=margin, indent=indent, openExternalLinks=openExternalLinks, textInteractionFlags=textInteractionFlags, hasSelectedText=hasSelectedText, selectedText=selectedText)

        # Override defaults from theme
        self.font_config.size = theme.description.font.size
        self.font_config.weight = theme.description.font.weight
        self._update_stylesheet()




class HComment(HLabel):
    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        f: Qt.WindowType = None,
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
        italic: bool = False,
    ) -> None:
        super().__init__(
            parent,
            f,
            theme=theme,
            text=text,
            textFormat=textFormat,
            pixmap=pixmap,
            scaledContents=scaledContents,
            alignment=alignment,
            wordWrap=wordWrap,
            margin=margin,
            indent=indent,
            openExternalLinks=openExternalLinks,
            textInteractionFlags=textInteractionFlags,
            hasSelectedText=hasSelectedText,
            selectedText=selectedText
        )

        # Override defaults from theme
        self.font_config.size = theme.comment.font.size
        self.font_config.weight = theme.comment.font.weight
        self.setItalic(italic)
        self._update_stylesheet()



class HSubtitle(HLabel):
    def __init__(self, /, parent: QWidget | None = None, f: Qt.WindowType = None, *, theme, text = None, textFormat = None, pixmap = None, scaledContents = None, alignment = None, wordWrap = None, margin = None, indent = None, openExternalLinks = None, textInteractionFlags = None, hasSelectedText = None, selectedText = None):
        super().__init__(parent, f, theme=theme, text=text, textFormat=textFormat, pixmap=pixmap, scaledContents=scaledContents, alignment=alignment, wordWrap=wordWrap, margin=margin, indent=indent, openExternalLinks=openExternalLinks, textInteractionFlags=textInteractionFlags, hasSelectedText=hasSelectedText, selectedText=selectedText)

        # Override defaults from theme
        self.font_config.size = theme.subtitle.font.size
        self.font_config.weight = theme.subtitle.font.weight
        self._update_stylesheet()
