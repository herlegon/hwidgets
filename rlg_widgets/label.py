from typing import Optional, overload
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtWidgets import (
    QLabel,
    QSizePolicy,
    QWidget,
)

from .colors import tuple_to_css
from .default_style import LABEL_STYLE
from .style_types import (
    TextStyle,
    textstyle_to_font,
)


dp_to_px = 1
LABEL_HEIGHT = int(40 / dp_to_px)
LABEL_MIN_WIDTH = int(64 / dp_to_px)
LABEL_PADDING = int(16 / dp_to_px)


class Label(QLabel):
    @overload
    def __init__(self, parent: QWidget) -> None: ...
    @overload
    def __init__(self, parent: QWidget, text: str) -> None: ...
    @overload
    def __init__(self, parent: QWidget, style: TextStyle) -> None: ...
    def __init__(self,
        parent: QWidget,
        text: Optional[str] = '',
        style: Optional[TextStyle] = LABEL_STYLE,
    ):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setText(text)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        )
        self.setMinimumWidth(LABEL_MIN_WIDTH)
        if style is not None:
            self.setFixedHeight(style.height)
            self.setFont(textstyle_to_font(style))
            # Currently use stylesheet. To be replaced by QPainter
            self.setStyleSheet(
                """
                    QLabel{{
                        color: {color};
                    }}
                """.format(
                    color=tuple_to_css(style.color)
                )
            )
        else:
            self.setFixedHeight(LABEL_HEIGHT)


# POC:
# class Label(QLabel):
#     def __init__(self, text: str, parent: Optional[QWidget | None] = None) -> None:
#         super().__init__(parent)
#         self.setObjectName("label")
#         self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
#         self.setText(text)

#         self.set_style(ButtonStyle())
#         self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred))
#         self.setMinimumWidth(LABEL_MIN_WIDTH)
#         self.adjustSize()


#     def set_style(self, button_style: ButtonStyle) -> None:
#         self.button_style = deepcopy(button_style)
#         self._update_stylesheet()
#         self.setStyleSheet(self.stylesheets[True])
#         self.repaint()



#     def _update_stylesheet(self) -> None:
#         style = self.button_style
#         stylesheet = """
#             #{name} {{
#                 color: {color};
#                 background-color: {bgd_color};
#                 padding-left: {padding}px;
#                 padding-right: {padding}px;
#             }}

#             #{name}:disabled {{
#                 color: {color_disabled};
#                 background-color: {bgd_color_disabled};
#             }}
#         """

#         self.stylesheets: dict[bool, str] = {
#             # Enabled...
#             True: stylesheet.format(
#                 name=self.objectName(),
#                 padding=LABEL_PADDING,
#                 color=style.color,
#                 bgd_color=style.bgd_color,
#                 color_disabled=style.color_disabled,
#                 bgd_color_disabled=style.bgd_color_disabled,
#             )
#         }

