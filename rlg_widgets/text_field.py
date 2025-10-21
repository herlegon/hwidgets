from typing import Optional, overload
from PySide6.QtCore import (
    Qt
)
from PySide6.QtWidgets import (
    QLabel,
    QSizePolicy,
    QWidget
)
from .colors import tuple_to_css
from .default_style import LABEL_STYLE
from .style_types import (
    TextStyle,
    textstyle_to_font,
)


class TextField(QLabel):
    @overload
    def __init__(self, parent: QWidget) -> None: ...
    @overload
    def __init__(self, parent: QWidget, text: str) -> None: ...
    @overload
    def __init__(self, parent: QWidget, style: TextStyle) -> None: ...
    def __init__(self,
        parent: QWidget,
        text: Optional[str] = '',
        style: Optional[TextStyle] = LABEL_STYLE,
    ):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setText(text)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        )
        if style is not None:
            self.setFixedHeight(style.height)
            self.setFont(textstyle_to_font(style))
            # Currently use stylesheet. To be replaced by QPainter
            self.setStyleSheet(
                """
                    QLabel{{
                        color: {color};
                    }}
                """.format(
                    color=tuple_to_css(style.color)
                )
            )
