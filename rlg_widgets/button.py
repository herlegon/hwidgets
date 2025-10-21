from dataclasses import dataclass
from pprint import pprint
from typing import Optional, overload
from PySide6.QtCore import (
    Qt,
    QSize,
)
from PySide6.QtGui import (
    QPixmap,
)
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
)

from .colors import tuple_to_css
from .default_style import BUTTON_STYLE
from .style_types import (
    ButtonStyle,
    TextStyle,
    textstyle_to_font,
)
from .tooltip import (
    ToolTipEventFilter,
)
from .utils import (
    BORDER_RADIUS,
    TITLE_BAR_ICON_PATH,
    # dp_to_px,
)

dp_to_px = 1
BUTTON_HEIGHT = int(40 / dp_to_px)
BUTTON_MIN_WIDTH = int(64 / dp_to_px)
BUTTON_PADDING = int(16 / dp_to_px)
ICON_PADDING = 16
ICON_SIZE = 16


@dataclass
class ButtonType:
    OUTLINED = 'outlined'
    CONTAINED = 'contained'


@dataclass
class ButtonState:
    ENABLED = 'enabled'
    PUSHED = 'pushed'
    HOVE = 'hover'


class Button(QPushButton):
    @overload
    def __init__(self, parent: QWidget) -> None: ...
    @overload
    def __init__(
        self,
        parent: QWidget,
        text: str,
        type: ButtonType,
    ) -> None: ...
    def __init__(self,
        parent: QWidget,
        text: Optional[str] = '',
        type: Optional[ButtonType] = ButtonType.OUTLINED,
        checkable: Optional[bool] = False,
        style: Optional[TextStyle] = BUTTON_STYLE,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("push_button")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setFlat(True)
        self.setFixedHeight(BUTTON_HEIGHT)
        self.setMinimumWidth(BUTTON_MIN_WIDTH)
        super().setCheckable(checkable)

        self.icon_size = QSize(ICON_SIZE, ICON_SIZE)
        self.button_icon: QPixmap | None = None
        self.state = 'enabled'

        self.button_style: ButtonStyle = style
        self.text_color = self.button_style.color
        if type == ButtonType.OUTLINED:
            self.set_style(self.button_style)
        else:
            self.set_style(self.button_style)

        self.setText(text)


    def setToolTip(self, text: str, delay_ms: int = 500, follow_cursor: bool = False) -> None:
        super().setToolTip(text)
        self.ttef = ToolTipEventFilter(self, delay_ms, follow_cursor)
        self.installEventFilter(self.ttef)


    def set_style(self, style: ButtonStyle) -> None:
        self.button_style = style
        self._update_stylesheet()
        self.setStyleSheet(self.stylesheets[True])
        self.repaint()



    def set_icon(self, ):
        # icon = QIcon()
        # icon.addPixmap(
        #     load_png_icon("minimize.png", color),
        #     QIcon.Mode.Normal, QIcon.State.Off
        # )
        # self.setIconSize(QSize(BUTTON_WIDTH, BUTTON_WIDTH))
        # self.setIcon(icon)

        self._update_stylesheet()
        self.setStyleSheet(self.stylesheets[True])
        self.update()


    def setTextStyle(self, style: TextStyle) -> None:
        # self.setFixedHeight(style.height)
        self.setFont(textstyle_to_font(style))
        self.text_color = tuple_to_css(style.color)
        self._update_stylesheet()
        self.setStyleSheet(self.stylesheets[True])
        self.update()


    def _update_stylesheet(self) -> None:
        style = self.button_style
        button_stylesheet = """
            Button {{
                color: {color};
                background-color: {bgd_color};
                border: 1px solid;
                border-radius: {border_radius}px;
                border-color: {border_color};
                padding-left: {padding}px;
                padding-right: {padding}px;
            }}
            Button:hover {{
                color: {color_hover};
                background-color: {bgd_color_hover};
            }}
            Button:pressed {{
                color: {color_pressed};
                background-color: {bgd_color_pressed};
            }}
            Button:checked {{
                color: {color_checked};
                background-color: {bgd_color_checked};
            }}
            Button:disabled {{
                color: {color_disabled};
                background-color: {bgd_color_disabled};
            }}
        """

        self.stylesheets: dict[bool, str] = {
            # Enabled...
            True: button_stylesheet.format(
                border=style.border,
                border_color=style.border_color,
                border_radius=min(style.border_radius, int(self.height()/2)),
                padding=BUTTON_PADDING,

                color=self.text_color,
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



