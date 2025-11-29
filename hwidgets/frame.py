from pprint import pprint
from typing import Type
from .styles import Theme

from PySide6.QtCore import (
    Qt,
    QRect,
)
from PySide6.QtGui import (
    QColor,
)
from PySide6.QtWidgets import (
    QSizePolicy,
    QWidget,
    QFrame,
)



class HFrame(QFrame):
    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        f: Qt.WindowType = None,
        *,
        theme: Type[Theme],
        frameShape: QFrame.Shape | None = None,
        frameShadow: QFrame.Shadow | None = None,
        lineWidth: int | None = None,
        midLineWidth: int | None = None,
        frameWidth: int | None = None,
        frameRect: QRect | None = None
    ) -> None:
        super().__init__(parent)
        self.f_style = (
            theme.card
            if isinstance(self, HCard)
            else theme.frame
        )
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setFrameShape(QFrame.Shape.StyledPanel)

        self._update_stylesheet()


    def _update_stylesheet(self) -> None:
        thickness: int = 0
        border_color: str = self.f_style.bgd
        if isinstance(self, HCard):
            border_color = self.f_style.border
            thickness = 1

        stylesheet = """
            QFrame {{
                background-color: {bgd};
                border-radius: {radius};
                border: {thickness}px solid {border};
            }}
        """.format(
            bgd=self.f_style.bgd,
            radius=int(self.f_style.radius * 1.5),
            thickness=thickness,
            border=border_color,
        )
        self.setStyleSheet(stylesheet)


    def setFrameShadow(self, shadow: QFrame.Shadow) -> None:
        return

    # def setFrameShape(self, shape: QFrame.Shape) -> None:
    #     return

    def setFrameStyle(self, style: int) -> None:
        return



class HCard(HFrame):
    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        f: Qt.WindowType = None,
        *,
        theme: Type[Theme],
        frameShape: QFrame.Shape | None = None,
        frameShadow: QFrame.Shadow | None = None,
        lineWidth: int | None = None,
        midLineWidth: int | None = None,
        frameWidth: int | None = None,
        frameRect: QRect | None = None
    ) -> None:
        super().__init__(
            parent,
            f=f,
            theme=theme,
            frameShape=QFrame.Shape.StyledPanel,
            frameShadow=frameShadow,
            lineWidth=lineWidth,
            midLineWidth=midLineWidth,
            frameWidth=1,
            frameRect=frameRect
        )

