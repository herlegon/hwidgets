import os
from typing import Optional
from PySide6.QtCore import (
    Qt,
    QSize,
)
from PySide6.QtGui import (
    QPainter,
    QColor,
    QImage,
    QPixmap,
    QIcon,
)
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
)
from .style_types import (
    ButtonStyle,
)
from .tooltip import (
    ToolTipEventFilter,
)
from .utils import (
    TITLE_BAR_ICON_PATH,
)
from .button import (
    ButtonType,
)

# Small FAB
# https://m3.material.io/components/floating-action-button/specs#b4625d66-f5ca-45f8-bb9f-45edb498ce1a
dp_to_px = 1
FAB_HEIGHT = int(40 / dp_to_px)
FAB_WIDTH = FAB_HEIGHT
FAB_RADIUS = 12
FAB_PADDING = int(16 / dp_to_px)
ICON_PADDING = 16
ICON_SIZE = int(24 / dp_to_px)



class FloatingButtonAction(QPushButton):
    def __init__(
        self,
        parent: Optional[QWidget],
        icon: str | None = None,
        button_type: ButtonType = ButtonType.OUTLINED,
        checkable: bool = False,
    ) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setObjectName("fab")
        self.setFlat(True)
        self.setFixedSize(QSize(FAB_WIDTH, FAB_HEIGHT))
        self.setCheckable(checkable)

        self.icon_size = QSize(ICON_SIZE, ICON_SIZE)

        self.button_style = ButtonStyle()
        if button_type == ButtonType.OUTLINED:
            self.set_style(self.button_style)
        else:
            self.set_style(self.button_style)
        if icon is not None:
            self.set_icon(icon)


    def _generate_pixmap(self, filename: str, color: str) -> QPixmap:
        filepath = os.path.join(TITLE_BAR_ICON_PATH, filename)
        if not os.path.exists(filepath):
            raise ValueError(f"image {filepath} does not exist")
        qimage: QImage = QImage(filepath)
        color = QColor(color)

        painter: QPainter = QPainter()
        painter.begin(qimage)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.setBrush(color)
        painter.setPen(color)
        painter.drawRect(qimage.rect())
        painter.end()
        return QPixmap(qimage)



    def setToolTip(self, text: str, delay_ms: int = 500, follow_cursor: bool = False) -> None:
        super().setToolTip(text)
        self.ttef = ToolTipEventFilter(self, delay_ms, follow_cursor)
        self.installEventFilter(self.ttef)


    def setText(self, text: str) -> None:
        return super().setText(text)


    def set_style(self, style: ButtonStyle) -> None:
        self.button_style = style
        self._update_stylesheet()
        self.setStyleSheet(self.stylesheets[self.isEnabled()])
        self.repaint()


    def set_icon(self, filepath: str) -> None:
        icon = QIcon()
        icon.addPixmap(
            self._generate_pixmap(filepath, self.button_style.color),
            QIcon.Mode.Normal, QIcon.State.Off
        )
        self.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.setIcon(icon)
        self._update_stylesheet()
        self.setStyleSheet(self.stylesheets[self.isEnabled()])
        self.repaint()


    def _update_stylesheet(self) -> None:
        style = self.button_style
        button_stylesheet = """
            #{name} {{
                color: {color};
                border: 1px solid {border_color};
                border-radius: {radius}px;
                border-color: {border_color};
                padding-left: {padding}px;
                padding-right: {padding}px;
            }}
            #{name}:hover {{
                color: {color_hover};
                background-color: {bgd_color_hover};
            }}
            #{name}:pressed {{
                color: {color_pressed};
                background-color: {bgd_color_pressed};
            }}
            #{name}:checked {{
                color: {color_checked};
                background-color: {bgd_color_checked};
            }}
            #{name}:disabled {{
                color: {color_disabled};
                background-color: {bgd_color_disabled};
            }}
        """

        self.stylesheets: dict[bool, str] = {
            # Enabled...
            True: button_stylesheet.format(
                name=self.objectName(),
                border=style.border,
                border_color=style.border_color,
                radius=min(style.border_radius, FAB_RADIUS),
                padding=FAB_PADDING,
                text_align='center',

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



