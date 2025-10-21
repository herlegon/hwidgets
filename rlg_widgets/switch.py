from typing import Optional
from PySide6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    Qt,
    QPoint,
    QRect,
    Property
)
from PySide6.QtGui import (
    QPaintEvent,
    QPainter,
    QColor,
)
from PySide6.QtWidgets import (
    QCheckBox,
    QPushButton,
    QWidget,
)
from .colors import (
    Color,
    tuple_to_css,
)
from .utils import (

    dp_to_px,
    DefaultSwitchColorStyle,
)


# M3 material
# Track
#     Height  32dp
#     Width       52dp
#     Outline width       2dp
#     Shape       md.sys.shape.corner.full
# Handle
#     Height (unselected)     16dp
#     Height - with icon      24dp  <-
#     Height (selected)       24dp
#     Height (pressed)        28dp
#     Width (unselected)      16dp
#     Width - with icon       24dp
#     Width (selected)        24dp
#     Width (pressed)     28dp
#     Shape       md.sys.shape.corner.full
# State layer
#     Size    40dp
#     Shape       md.sys.shape.corner.full
# Target      Size    48dp
# Icon        Size (selected)     16dp
# Icon        Size (unselected)       16dp


TRACK_WIDTH: int = round(52/dp_to_px)
TRACK_HEIGHT: int = round(32/dp_to_px)
# Note: Track outline width is currently not used
TRACK_OUTLINE_WIDTH = 0
HANDLE_RADIUS: int = round(22/dp_to_px) - TRACK_OUTLINE_WIDTH
TRACK_MARGIN = int((TRACK_HEIGHT - HANDLE_RADIUS) / 2)
TRACK_HEIGHT = TRACK_MARGIN * 2 + HANDLE_RADIUS


class Switch(QCheckBox):
    def __init__(
        self,
        parent: Optional[QWidget]
    ) -> None:
        super().__init__(parent)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Use variable for testing purpose: dpi/screen resolution
        track_width = TRACK_WIDTH
        self.track_height = TRACK_HEIGHT
        self.track_radius = int(TRACK_HEIGHT / 2)
        self.handle_radius = HANDLE_RADIUS
        self.margin = TRACK_MARGIN

        self.handle_position_off = self.margin
        self.handle_position_on = TRACK_WIDTH - HANDLE_RADIUS - self.margin

        track_color_on = DefaultSwitchColorStyle.track_color_on
        track_color_off = DefaultSwitchColorStyle.track_color_off
        # track outline color = handle_color
        handle_color_on = DefaultSwitchColorStyle.handle_color_on
        handle_color_off = DefaultSwitchColorStyle.handle_color_off

        self.track_color_off = QColor(track_color_off)
        self.track_color_on = QColor(track_color_on)
        self.handle_color_off = QColor(handle_color_off)
        self.handle_color_on = QColor(handle_color_on)

        self.handle_position = self.margin
        self.setFixedSize(track_width, self.track_height)

        curve: QEasingCurve.Type = QEasingCurve.Type.InOutQuad
        self.animation = QPropertyAnimation(self, b"position")
        self.animation.setEasingCurve(curve)
        self.animation.setDuration(250)
        self.stateChanged.connect(self.state_changed_event)


    @Property(float)
    def position(self) -> int:
        return self.handle_position


    @position.setter
    def position(self, pos: int) -> None:
        self.handle_position = pos
        self.update()


    def setChecked(self, checked: bool) -> None:
        self.blockSignals(True)
        super().setChecked(checked)
        self.handle_position = (
            self.handle_position_on if checked else self.handle_position_off)
        self.blockSignals(False)


    def state_changed_event(self, checked: bool) -> None:
        self.animation.stop()
        self.animation.setEndValue(
            self.handle_position_on if checked else self.handle_position_off)
        self.animation.start()


    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)


    def paintEvent(self, event: QPaintEvent) -> None:
        height = self.height()

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)
        rect = QRect(0, 0, self.width(), height)

        if self.isChecked():
            p.setBrush(QColor(self.track_color_on))
            p.drawRoundedRect(
                0, 0, rect.width(), height, self.track_radius, self.track_radius)

            p.setBrush(QColor(self.handle_color_on))
            p.drawEllipse(
                self.handle_position,
                self.margin,
                self.handle_radius,
                self.handle_radius
            )
        else:
            p.setBrush(QColor(self.track_color_off))
            p.drawRoundedRect(
                0, 0, rect.width(), height, self.track_radius, self.track_radius)

            p.setBrush(QColor(self.handle_color_off))
            p.drawEllipse(
                self.handle_position,
                self.margin,
                self.handle_radius,
                self.handle_radius
            )

        p.end()




class PushButton(QPushButton):
    def __init__(
        self,
        parent: Optional[QWidget],
        text: str,
        border_radius: int = 6,
        text_color: Color = "black",
        bgd_color: Color = (80, 80, 80),
        bgd_color_hover: Color = (190, 190, 190),
        bgd_color_pressed: Color = (0, 100, 180),
    ):
        super().__init__(parent, text=text)
        self.setFlat(True)
        button_style = """
            .PushButton {{
                background-color: {bgd_color};
                color: {color};
                border: none;
                border-radius: {radius};
                padding-left: 8px;
                padding-right: 8px;
            }}
            .PushButton:hover {{
                background-color: {bgd_hover};
            }}
            .PushButton:pressed {{
                background-color: {bgd_pressed};
            }}
        """.format(
            bgd_color=tuple_to_css(bgd_color),
            color=tuple_to_css(text_color),
            radius=border_radius,
            bgd_hover=tuple_to_css(bgd_color_hover),
            bgd_pressed=tuple_to_css(bgd_color_pressed)
        )

        self.setStyleSheet(button_style)
        self.setMinimumHeight(32)

        self.setCursor(Qt.CursorShape.PointingHandCursor)



