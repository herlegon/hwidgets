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
        self.theme = theme
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setFrameShadow(QFrame.Shadow.Plain)

        self._update_stylesheet()


    def _update_stylesheet(self) -> None:
        f_style = self.theme.frame
        stylesheet = """
            QFrame {{
                background-color: {bgd};
                border-radius: {radius};
            }}
        """.format(
            bgd=f_style.bgd,
            radius=f_style.radius * 1.5,
        )
        self.setStyleSheet(stylesheet)


    def setFrameShadow(self, shadow: QFrame.Shadow) -> None:
        return

    def setFrameShape(self, shape: QFrame.Shape) -> None:
        return

    def setFrameStyle(self, style: int) -> None:
        return
