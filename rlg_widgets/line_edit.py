
from copy import deepcopy
from typing import Optional
from PySide6.QtCore import (
    QSize,
    Qt,
)
from PySide6.QtGui import (
    QIcon,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
    QLineEdit,
)

from .style_types import ButtonStyle
from .utils import (
    dp_to_px,
    load_png_icon,
)

LINEEDIT_HEIGHT = 32
LINEEDIT_RADIUS = 4
LINEEDIT_PADDING = 12
LINEEDIT_MIN_WIDTH = int(64 / dp_to_px)


class LineEdit(QLineEdit):

    def __init__(self, parent: Optional[QWidget]) -> None:

        super().__init__(parent)
        # self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(LINEEDIT_HEIGHT)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.lineedit_style = ButtonStyle()
        self.set_style(self.lineedit_style)
        self.setClearButtonEnabled(False)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setFixedWidth(300)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,LINEEDIT_PADDING,0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.addStretch(1)

        self.clear_button = QPushButton(self)
        self.clear_button.setFixedSize(QSize(LINEEDIT_HEIGHT, LINEEDIT_HEIGHT))
        self.clear_button.setFlat(True)
        self.clear_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_button.released.connect(self.clear_button_released)
        icon = QIcon()
        icon.addPixmap(
            load_png_icon("cancel_FILL0_wght300_GRAD0_opsz24.png", "#E1E1E1"),
            QIcon.Mode.Normal, QIcon.State.Off
        )
        self.clear_button.setIcon(icon)
        self.main_layout.addWidget(self.clear_button, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.setLayout(self.main_layout)

        self.clear_button.hide()
        self.textChanged[str].connect(self.text_changed)
        self.textEdited[str].connect(self.text_changed)


    def clear_button_released(self):
        self.clear()
        self.clear_button.hide()


    def text_changed(self, text: str) -> None:
        if len(text) > 0:
            self.clear_button.show()
        else:
            self.clear_button.hide()


    # def enterEvent(self, event: QEnterEvent) -> None:
    #     if len(self.text()) > 0:
    #         self.clear_button.show()
    #     return super().enterEvent(event)


    def set_style(self, lineedit_style: ButtonStyle) -> None:
        self.lineedit_style = deepcopy(lineedit_style)
        self._update_stylesheet()
        self.setStyleSheet(self.stylesheets[True])
        self.repaint()


    def _update_stylesheet(self) -> None:
        style = self.lineedit_style
        stylesheet = """
            QPushButton {{
                border: 0px;
                outline: none;
            }}

            LineEdit {{
                color: {color};
                border: 1px solid;
                border-radius: {radius}px;
                border-color: {border_color};
                padding-left: {padding}px;
                padding-right: {padding_right}px;
                min-width: {min_width}px;
                background-color: {bgd_color};

            }}
            LineEdit:focus {{
                color: {color_hover};
                border-color: {bgd_color_hover};
            }}
            LineEdit:hover {{
                color: {color_hover};
                border-color: {bgd_color_hover};
            }}
            LineEdit:disabled {{
                color: {color_disabled};
                background-color: {bgd_color_disabled};
            }}
        """

        self.stylesheets: dict[bool, str] = {
            # Enabled...
            True: stylesheet.format(
                border=style.border,
                border_color=style.border_color,
                radius=min(style.border_radius, int(self.height()/2)),
                min_width=LINEEDIT_MIN_WIDTH,
                padding=LINEEDIT_PADDING,
                padding_right=LINEEDIT_HEIGHT + LINEEDIT_PADDING,

                color=style.color,
                bgd_color=style.bgd_color,
                color_hover=style.color,
                bgd_color_hover=style.bgd_color_hover,
                color_pressed=style.color_pressed,
                bgd_color_pressed=style.bgd_color_pressed,
                color_checked=style.color_checked,
                bgd_color_checked=style.bgd_color_checked,
                color_disabled=style.color_disabled,
                bgd_color_disabled=style.bgd_color_disabled,
            )
        }


