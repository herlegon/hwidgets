
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
from .style_types import ButtonStyle

dp_to_px = 1
DIVIDER_THICKNESS = 1
DIVIDER_MIN_LENGTH = int(64 / dp_to_px)
DIVIDER_PADDING = int(16 / dp_to_px)

class Divider(QFrame):
    def __init__(self,
            parent: QWidget,
            orientation: Literal['horizontal', 'vertical'] = 'horizontal',
            thickness: int = DIVIDER_THICKNESS,
        ) -> None:
        super().__init__(parent)
        self.setObjectName("divider")
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

        self.set_style(ButtonStyle())
        self.adjustSize()


    def set_style(self, button_style: ButtonStyle) -> None:
        self.button_style = deepcopy(button_style)
        self._update_stylesheet()
        self.setStyleSheet(self.stylesheets[True])
        self.repaint()


    def _update_stylesheet(self) -> None:
        style = self.button_style
        stylesheet = """
            #{name} {{
                border: 1px solid {border_color};
            }}
        """

        self.stylesheets: dict[bool, str] = {
            # Enabled...
            True: stylesheet.format(
                name=self.objectName(),
                border_color=style.border_color,
            )
        }

