from pprint import pprint
from string import Template
import sys
from typing import TYPE_CHECKING, Literal, Type

from PySide6.QtCore import (
    Qt,
    QRect,
)
from PySide6.QtGui import (
    QColor,
    QPainter,
    QBrush,
    QPaintEvent,
)
from PySide6.QtWidgets import (
    QSlider,
    QWidget,
)

from .styles import Theme, SliderStyle
from .debug import (
    DEBUG_GEOMETRY,
    draw_widget_rect
)



class HSlider(QSlider):
    def __init__(
        self,
        parent: QWidget | None,
        /,
        theme: Type[Theme],
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
        show_ticks: bool = False,
        tick_interval: int = 10,
        snap_to_ticks: bool = False,
        snap_threshold: int = 3
    ):
        super().__init__(parent, orientation)
        self.show_ticks: bool = show_ticks
        self.tick_interval: int = tick_interval
        self.snap_to_ticks: bool = snap_to_ticks
        self.snap_threshold: int = snap_threshold
        self.setMinimumHeight(30 if show_ticks else 20)

        self.slider_style: SliderStyle = theme.slider
        self.setFixedHeight(
            max(self.slider_style.track_thickness, self.slider_style.handle_radius * 2)
        )
        self._update_styles()

        if self.snap_to_ticks:
            self.valueChanged.connect(self._snap_value)


    def _update_styles(self) -> None:
        self.track_color = QBrush(self.slider_style.track)
        self.track_disabled_color = QBrush(self.slider_style.track_disabled)

        self.ticks_color = QColor(self.slider_style.ticks)
        self.ticks_disabled_color = QColor(self.slider_style.track_disabled)

        self.handle_colors: dict[str, QBrush] = {
            'normal': QBrush(self.slider_style.handle),
            'hover': QBrush(self.slider_style.handle_hover),
            'pressed': QBrush(self.slider_style.handle_pressed),
            'disabled': QBrush(self.slider_style.handle_disabled),
        }


    def showTicks(self, show: bool):
        """Enable or disable tick marks"""
        self.show_ticks = show
        self.setMinimumHeight(30 if show else 20)
        self.update()


    def setTickInterval(self, interval: int):
        """Set the interval between tick marks"""
        self.tick_interval = interval
        self.update()


    def snapToTicks(self, snap: bool):
        """Enable or disable snapping to ticks"""
        if snap and not self.snap_to_ticks:
            self.valueChanged.connect(self._snap_value)
        elif not snap and self.snap_to_ticks:
            self.valueChanged.disconnect(self._snap_value)
        self.snap_to_ticks = snap


    def setSnapThreshold(self, threshold: int):
        """Set the snap threshold distance"""
        self.snap_threshold = threshold


    def ticksVisible(self):
        """Get current tick visibility state"""
        return self.show_ticks


    def getTickInterval(self):
        """Get current tick interval"""
        return self.tick_interval


    def getSnapToTicks(self):
        """Get current snap state"""
        return self.snap_to_ticks


    def getSnapThreshold(self):
        """Get current snap threshold"""
        return self.snap_threshold


    def _snap_value(self, value: int):
        if not self.snap_to_ticks or self.tick_interval == 0:
            return

        # Find nearest tick
        remainder = value % self.tick_interval

        # Check if within snap threshold
        if remainder <= self.snap_threshold:
            # Snap down
            new_value = value - remainder
            if new_value != value:
                self.blockSignals(True)
                self.setValue(new_value)
                self.blockSignals(False)
        elif remainder >= (self.tick_interval - self.snap_threshold):
            # Snap up
            new_value = value + (self.tick_interval - remainder)
            if new_value != value and new_value <= self.maximum():
                self.blockSignals(True)
                self.setValue(new_value)
                self.blockSignals(False)


    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if DEBUG_GEOMETRY:
            draw_widget_rect(self, painter)

        # Calculate dimensions
        groove_height = 4
        handle_size = 12

        # Get widget dimensions
        width = self.width()
        height = self.height()

        # Calculate groove position (centered vertically, with space for ticks if needed)
        groove_y = (height - groove_height) // 2
        if self.show_ticks:
            groove_y = height // 2 - 10

        # Draw groove (track)
        groove_rect = QRect(handle_size // 2, groove_y, width - handle_size, groove_height)
        painter.setBrush(
            self.track_color
            if self.isEnabled()
            else self.track_disabled_color
        )
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(groove_rect, 2, 2)

        # Draw ticks if enabled
        if self.show_ticks:
            painter.setPen(QColor("#6a6a6a"))
            painter.setBrush(
                self.ticks_color
                if self.isEnabled()
                else self.ticks_disabled_color
            )

            tick_y = groove_y + groove_height + 6

            for value in range(self.minimum(), self.maximum() + 1, self.tick_interval):
                # Calculate x position for this tick
                ratio = (value - self.minimum()) / (self.maximum() - self.minimum())
                tick_x = handle_size // 2 + ratio * (width - handle_size)

                # Draw tick mark
                painter.drawLine(int(tick_x), tick_y, int(tick_x), tick_y + 4)

        # Calculate handle position
        ratio = (self.value() - self.minimum()) / (self.maximum() - self.minimum())
        handle_x = handle_size // 2 + ratio * (width - handle_size)
        handle_y = groove_y + groove_height // 2

        # Draw handle
        if self.isEnabled():
            if self.isSliderDown():
                painter.setBrush(self.handle_colors['pressed'])
            else:
                painter.setBrush(self.handle_colors['normal'])
        else:
            painter.setBrush(self.handle_colors['disabled'])

        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(
            int(handle_x - handle_size // 2),
            int(handle_y - handle_size // 2),
            handle_size,
            handle_size
        )


        painter.end()
