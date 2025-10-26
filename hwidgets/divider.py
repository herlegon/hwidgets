
from copy import deepcopy
from typing import Literal
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtWidgets import (
    QSizePolicy,
    QWidget,
    QFrame
)
from .hstyle import (
    DIVIDER_MIN_LENGTH,
    DIVIDER_THICKNESS,
    HStyle
)

class HDivider(QFrame):
    def __init__(
        self,
        parent: QWidget,
        hstyle: HStyle,
        orientation: Literal['horizontal', 'vertical'] = 'horizontal',
        thickness: int = DIVIDER_THICKNESS,
    ) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setFrameShadow(QFrame.Shadow.Plain)

        if orientation == 'vertical':
            self.setFrameShape(QFrame.Shape.VLine)
            self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))
            self.setMinimumHeight(DIVIDER_MIN_LENGTH)
            self.setFixedWidth(thickness)

        else:
            self.setFrameShape(QFrame.Shape.HLine)
            self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
            self.setMinimumWidth(DIVIDER_MIN_LENGTH)
            self.setFixedHeight(DIVIDER_THICKNESS)

        stylesheet = """
                QFrame {{
                    border: 1px solid {divider};
                }}
            """.format(
                divider=hstyle.divider,
            )

        self.setStyleSheet(stylesheet)


        self.adjustSize()


    def setFrameShadow(self, shadow: QFrame.Shadow) -> None:
        return

    def setFrameShape(self, shape: QFrame.Shape) -> None:
        return

    def setFrameStyle(self, style: int) -> None:
        return
