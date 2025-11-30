from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QColor, QFont
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QColor, QFont
import sys

class CustomSlider(QSlider):
    def __init__(self, orientation=Qt.Horizontal, show_ticks=False, tick_interval=10, snap_to_ticks=False, snap_threshold=3):
        super().__init__(orientation)
        self.show_ticks = show_ticks
        self.tick_interval = tick_interval
        self.snap_to_ticks = snap_to_ticks
        self.snap_threshold = snap_threshold
        self.setMinimumHeight(30 if show_ticks else 20)

        if self.snap_to_ticks:
            self.valueChanged.connect(self._snap_value)


    def showTicks(self, show):
        """Enable or disable tick marks"""
        self.show_ticks = show
        self.setMinimumHeight(30 if show else 20)
        self.update()


    def setTickInterval(self, interval):
        """Set the interval between tick marks"""
        self.tick_interval = interval
        self.update()


    def set_snap_to_ticks(self, snap):
        """Enable or disable snapping to ticks"""
        if snap and not self.snap_to_ticks:
            self.valueChanged.connect(self._snap_value)
        elif not snap and self.snap_to_ticks:
            self.valueChanged.disconnect(self._snap_value)
        self.snap_to_ticks = snap


    def setSnapThreshold(self, threshold):
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


    def _snap_value(self, value):
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

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

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
        painter.setBrush(QColor("#4a4a4a"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(groove_rect, 2, 2)

        # Draw ticks if enabled
        if self.show_ticks:
            painter.setPen(QColor("#6a6a6a"))
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
        if self.isSliderDown():
            painter.setBrush(QColor("#8a9eff"))
        else:
            painter.setBrush(QColor("#5e7ce0"))

        painter.setPen(Qt.NoPen)
        painter.drawEllipse(
            int(handle_x - handle_size // 2),
            int(handle_y - handle_size // 2),
            handle_size,
            handle_size
        )

class StyledSlider(QWidget):
    def __init__(self, show_ticks=False, tick_interval=10, snap_to_ticks=False, snap_threshold=3):
        super().__init__()
        self.show_ticks = show_ticks
        self.tick_interval = tick_interval
        self.snap_to_ticks = snap_to_ticks
        self.snap_threshold = snap_threshold
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Custom Slider")
        self.setStyleSheet("background-color: #2a2a2a;")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Label
        label = QLabel("Volume")
        label.setFont(QFont("Segoe UI", 14))
        label.setStyleSheet("""
            color: #e0e0e0;
        """)

        # Custom Slider
        slider = CustomSlider(Qt.Horizontal, self.show_ticks, self.tick_interval,
                             self.snap_to_ticks, self.snap_threshold)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)

        # Value label (optional - shows current value)
        value_label = QLabel("50")
        value_label.setFont(QFont("Segoe UI", 12))
        value_label.setStyleSheet("""
            color: #e0e0e0;
        """)

        slider.valueChanged.connect(lambda v: value_label.setText(str(v)))

        layout.addWidget(label)
        layout.addWidget(slider)
        layout.addWidget(value_label)
        layout.addStretch()

        self.setLayout(layout)
        self.resize(400, 150)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Example without ticks
    # window = StyledSlider(show_ticks=False)

    # Example with ticks and snapping (every 10 units, snap within 3 units)
    window = StyledSlider(show_ticks=True, tick_interval=10, snap_to_ticks=True, snap_threshold=3)

    window.show()
    sys.exit(app.exec())
