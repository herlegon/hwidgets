from pathlib import Path
from typing import Optional, overload
from PySide6.QtCore import (
    Qt
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QWidget
)
from .colors import tuple_to_css
from .default_style import TITLE_1_STYLE
from .style_types import (
    TextStyle,
    textstyle_to_font,
)
from .utils import png_to_pixmap



class Title_1(QWidget):
    @overload
    def __init__(self, parent: QWidget) -> None: ...
    @overload
    def __init__(self, parent: QWidget, text: str) -> None: ...
    def __init__(self,
        parent: QWidget,
        text: Optional[str] = '',
        icon: Optional[str | Path | None] = None,
        style: Optional[TextStyle] = TITLE_1_STYLE,
    ):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setFixedHeight(style.height)
        self._style = style

        self._layout = QHBoxLayout()
        # M3 margins: https://m3.material.io/components/top-app-bar/specs
        self._layout.setContentsMargins(16, 4, 12, 4)
        self._layout.setSpacing(8)
        self.setLayout(self._layout)

        self._icon: QLabel | None = None
        if icon is not None:
            icon_path = str(icon) if isinstance(icon, Path) else icon
            self._icon = QLabel(self)
            pixmap = png_to_pixmap(icon_path, style.color, style.height)
            self._icon.setPixmap(pixmap)
            self._icon.setFixedSize(pixmap.size())
            self._layout.addWidget(self._icon)
        self._title = QLabel(text, self)
        self._layout.addWidget(
            self._title, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignHCenter
        )

        self._title.setFont(textstyle_to_font(style))
        # Currently use stylesheet. To be replaced by QPainter
        self._title.setStyleSheet(
            """
                QLabel{{
                    color: {color};
                }}
            """.format(
                color=tuple_to_css(style.color)
            )
        )
        # self._title.setFixedHeight(style.height)
        self._title.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        )

        # self.setSizePolicy(
        #     QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # )


    def setText(self, text: str) -> None:
        self._title.setText(text)


    def setIcon(self, icon: Optional[str | Path]):
        icon_path = str(icon) if isinstance(icon, Path) else icon
        if self._icon is None:
            self._icon = QLabel(self)
            self._layout.insertWidget(0, self._icon)
        pixmap = png_to_pixmap(icon_path, self._style.color, self._style.height)
        self._icon.setPixmap(pixmap)
        self._icon.setFixedSize(pixmap.size())

