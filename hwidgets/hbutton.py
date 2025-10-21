from string import Template
from .hstyle import COMBOBOX_RADIUS, LABEL_HEIGHT, LABEL_MIN_WIDTH, HStyle, load_qss

from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QIcon,
    QPixmap,
)
from PySide6.QtWidgets import (
    QPushButton,
    QSizePolicy,
    QWidget,
)


class HButton(QPushButton):

    # def __init__(
    #     self, text: str, /, parent: QWidget | None = ..., *,
    #     autoDefault: bool | None = ..., default: bool | None = ...,
    #     flat: bool | None = ...
    # ) -> None:
    # def __init__(
    #     self, /, parent: QWidget | None = ..., *,
    #     autoDefault: bool | None = ..., default: bool | None = ...,
    #     flat: bool | None = ...
    # ) -> None:
    def __init__(
        self,
        /,
        parent: QWidget | None = ...,
        *,
        icon: QIcon | QPixmap | None = None,
        text: str | None = None,
        hstyle: HStyle,
        autoDefault: bool | None = None,
        default: bool | None = None,
        flat: bool | None = True,
    ) -> None:

        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        if text is not None:
            self.setText(text)
        self.setFlat(True)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        )
        self.setMinimumWidth(LABEL_MIN_WIDTH)
        self.setFixedHeight(LABEL_HEIGHT)

        qss_template = Template(load_qss(f"hbutton.qss"))
        qss = qss_template.substitute(
            widget_bgd=f"{hstyle.widget_bgd}",
            widget_hover=f"{hstyle.hover_bgd}",
            widget_disabled=f"{hstyle.disabled_bgd}",
            text_color=f"{hstyle.text_color}",
            selection_bgd=f"{hstyle.selection_bgd}",
            checked_color=f"{hstyle.enabled}",
            radius=f"{COMBOBOX_RADIUS}px",
        )
        self.setStyleSheet(qss)
