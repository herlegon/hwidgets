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
    QDoubleSpinBox,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QSizePolicy,
)

from .style_types import ButtonStyle
from .utils import (
    dp_to_px,
    load_png_icon,
)


SPINBOX_HEIGHT = 32
SPINBOX_RADIUS = 4
SPINBOX_PADDING = 12
SPINBOX_MIN_WIDTH = int(64 / dp_to_px)


class SpinBox(QDoubleSpinBox):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(SPINBOX_HEIGHT)
        self.spinbox_style = ButtonStyle()
        self.set_style(self.spinbox_style)
        self.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, SPINBOX_RADIUS, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.addStretch(1)
        icon_size = QSize(SPINBOX_HEIGHT, (SPINBOX_HEIGHT/2))
        self.plus_button = QPushButton(self)
        self.plus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.plus_button.setFlat(True)
        self.plus_button.setFixedSize(icon_size)
        icon_plus = QIcon()
        icon_plus.addPixmap(
            load_png_icon("add_FILL0_wght500_GRAD0_opsz20.png", "#F0F0F0"),
            QIcon.Mode.Normal, QIcon.State.Off
        )
        self.plus_button.setIconSize(icon_size)
        self.plus_button.setIcon(icon_plus)
        self.plus_button.setAutoRepeat(True)

        self.minus_button = QPushButton(self)
        self.minus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.minus_button.setFlat(True)
        self.minus_button.setFixedSize(icon_size)
        icon_minus = QIcon()
        icon_minus.addPixmap(
            load_png_icon("remove_FILL0_wght500_GRAD0_opsz20.png", "#F0F0F0"),
            QIcon.Mode.Normal, QIcon.State.Off
        )
        self.minus_button.setIconSize(icon_size)
        self.minus_button.setIcon(icon_minus)
        self.minus_button.setAutoRepeat(True)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(0)
        button_layout.setContentsMargins(0,2,0,2)
        button_layout.addWidget(self.plus_button, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        button_layout.addWidget(self.minus_button, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        print(button_layout.contentsMargins())
        self.main_layout.addLayout(button_layout)
        self.plus_button.clicked.connect(self.stepUp)
        self.minus_button.clicked.connect(self.stepDown)

        # self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.customContextMenuRequested.connect(self._showContextMenu)

        self.setLayout(self.main_layout)
        # self.installEventFilter(self.lineEdit())


    def set_style(self, style: ButtonStyle) -> None:
        self.spinbox_style = style
        self._update_stylesheet()
        self.setStyleSheet(self.stylesheets[True])
        self.repaint()



    def _update_stylesheet(self) -> None:
        print(f"{type(self)}")
        style = self.spinbox_style
        stylesheet = """
            QPushButton {{
                border: 0px;
                outline: none;
            }}

            QDoubleSpinBox {{
                color: {color};
                border: 1px solid;
                border-radius: {radius}px;
                border-color: {border_color};
                padding-left: {padding}px;
                padding-right: {padding_right}px;
                min-width: {min_width}px;
                background-color: {bgd_color};
                selection-background-color: transparent;
                selection-color: {color};

            }}
            QDoubleSpinBox:focus {{
                color: {color_hover};
                border-color: {bgd_color_hover};
            }}
            QDoubleSpinBox:hover {{
                color: {color_hover};
                border-color: {bgd_color_hover};
            }}
            QDoubleSpinBox:disabled {{
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
                min_width=SPINBOX_MIN_WIDTH,
                padding=SPINBOX_PADDING,
                padding_right=SPINBOX_HEIGHT,

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


