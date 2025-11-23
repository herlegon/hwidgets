from typing import Literal, Type
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QColor,
)
from PySide6.QtWidgets import (
    QSizePolicy,
    QWidget,
    QFrame,
)

from .styles import DividerStyle, Theme


class HDivider(QFrame):
    def __init__(
        self,
        parent: QWidget,
        theme: Type[Theme],
        orientation: Literal['horizontal', 'vertical'] = 'horizontal',
    ) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setFrameShadow(QFrame.Shadow.Plain)

        if orientation == 'vertical':
            self.setFrameShape(QFrame.Shape.VLine)
            self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))
            self.setMinimumHeight(theme.divider.min_length)
            self.setFixedWidth(theme.divider.thickness)

        else:
            self.setFrameShape(QFrame.Shape.HLine)
            self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
            self.setMinimumWidth(theme.divider.min_length)
            self.setFixedHeight(theme.divider.thickness)

        self._update_stylesheet(theme.divider.normal)
        self.adjustSize()


    def _update_stylesheet(self, divider_style: DividerStyle) -> None:
        stylesheet = """
            QFrame {{
                border: {thickness}px solid {divider};
            }}
        """.format(
            divider=divider_style.normal,
            thickness=divider_style.thickness,
        )
        self.setStyleSheet(stylesheet)


    def setFrameShadow(self, shadow: QFrame.Shadow) -> None:
        return

    def setFrameShape(self, shape: QFrame.Shape) -> None:
        return

    def setFrameStyle(self, style: int) -> None:
        return

    def set_line_color(self, color: str) -> None:
        self._update_stylesheet(line_color=color)



class HVerticalDivider(HDivider):
    def __init__(
        self,
        parent: QWidget,
        theme: Type[Theme],
    ) -> None:
        super().__init__(
            parent=parent,
            orientation='vertical',
            theme=theme,
        )



class HHorizontalDivider(HDivider):
    def __init__(
        self,
        parent: QWidget,
        theme: Type[Theme],
    ) -> None:
        super().__init__(
            parent=parent,
            orientation='horizontal',
            theme=theme,
        )

