from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider
from PySide6.QtCore import Qt
import sys

class StyledSlider(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Custom Slider")
        self.setStyleSheet("background-color: #2a2a2a;")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Label
        label = QLabel("Volume")
        label.setStyleSheet("""
            color: #e0e0e0;
            font-size: 14px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin-bottom: 8px;
        """)

        # Slider
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)
        slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #4a4a4a;
                height: 4px;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #5e7ce0;
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
            QSlider::handle:horizontal:pressed {
                background: #8a9eff;
            }
        """)

        # Value label (optional - shows current value)
        value_label = QLabel("50")
        value_label.setStyleSheet("""
            color: #e0e0e0;
            font-size: 12px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
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
    window = StyledSlider()
    window.show()
    sys.exit(app.exec())
