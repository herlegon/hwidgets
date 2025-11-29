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

from .styles import Theme


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
        self.w_style = theme.divider
        self.setFrameShape(
            QFrame.Shape.VLine if orientation == 'vertical' else QFrame.Shape.HLine
        )
        self._update_stylesheet()
        self.adjustSize()


    def _update_stylesheet(self) -> None:
        stylesheet = """
            QFrame {{
                border: {thickness}px solid {divider};
            }}
        """.format(
            divider=self.w_style.normal,
            thickness=self.w_style.thickness,
        )
        self.setStyleSheet(stylesheet)


    def setFrameShadow(self, shadow: QFrame.Shadow) -> None:
        return


    def setFrameShape(self, shape: QFrame.Shape) -> None:
        super().setFrameShape(shape)
        if shape == QFrame.Shape.VLine:
            self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))
            self.setMinimumHeight(self.w_style.min_length)
            self.setFixedWidth(self.w_style.thickness)

        else:
            self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
            self.setMinimumWidth(self.w_style.min_length)
            self.setFixedHeight(self.w_style.thickness)
        self.adjustSize()

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

