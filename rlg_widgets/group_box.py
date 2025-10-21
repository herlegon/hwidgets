
from copy import deepcopy
from typing import Optional
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtWidgets import (
    QGroupBox,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from .style_types import ButtonStyle
from .line_edit import LineEdit


dp_to_px = 1
GROUPBOX_HEIGHT = int(40 / dp_to_px)
GROUPBOX_MIN_WIDTH = int(64 / dp_to_px)
GROUPBOX_PADDING = int(16 / dp_to_px)
TITLE_PADDING = GROUPBOX_PADDING + int(4 / dp_to_px)


class GroupBox(QGroupBox):
    def __init__(self, parent: Optional[QWidget]) -> None:
        super().__init__(parent)
        self.setObjectName("groupbox")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setCheckable(False)

        verticalLayout = QVBoxLayout(self)
        line_edit = LineEdit(self)
        # label = QLabel(self)
        # label.setText(u"label")
        # label.setStyleSheet("color: white; background-color: green;")
        verticalLayout.addWidget(line_edit)
        # verticalLayout.setContentsMargins(16,16,16,16)
        self.setTitle("groupbox")

        self.set_style(ButtonStyle())
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred))
        self.setMinimumWidth(GROUPBOX_MIN_WIDTH)
        self.adjustSize()


    def set_style(self, style: ButtonStyle) -> None:
        self.button_style = style
        self._update_stylesheet()
        self.setStyleSheet(self.stylesheets[True])
        self.repaint()



    def _update_stylesheet(self) -> None:
        style = self.button_style
        stylesheet = """
            #{name} {{
                color: {color};
                background-color: {bgd_color};
                border: 1px solid;
                border-radius: {radius}px;
                border-color: {border_color};
                padding-left: {padding}px;
                padding-right: {padding}px;
                margin-top: 8px;
            }}

            #{name}:title {{
                subcontrol-origin: margin;
                background-color: {bgd_color};
                left: {padding}px;
                padding: 0px 3px;
            }}

            #{name}:disabled {{
                color: {color_disabled};
                background-color: {bgd_color_disabled};
            }}
        """

        self.stylesheets: dict[bool, str] = {
            # Enabled...
            True: stylesheet.format(
                name=self.objectName(),
                border=style.border,
                border_color=style.border_color,
                radius=min(style.border_radius, int(self.height()/2)),
                padding=GROUPBOX_PADDING,
                title_padding=TITLE_PADDING,

                color=style.color,
                bgd_color=style.bgd_color,
                color_hover=style.color_hover,
                bgd_color_hover=style.bgd_color_hover,
                color_pressed=style.color_pressed,
                bgd_color_pressed=style.bgd_color_pressed,
                color_checked=style.color_checked,
                bgd_color_checked=style.bgd_color_checked,
                color_disabled=style.color_disabled,
                bgd_color_disabled=style.bgd_color_disabled,
            )
        }

