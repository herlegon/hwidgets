from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QGridLayout, QPushButton, QLabel,
                               QSizePolicy, QTextEdit)
from PySide6.QtCore import Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Model Browser Layout")

        # Fixed dimensions
        self.FIXED_LOG_WIDTH = 300
        self.FIXED_HEADER_HEIGHT = 60
        self.FIXED_BROWSER_HEIGHT = 80

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left section (all widgets except log)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(5, 5, 5, 5)
        left_layout.setSpacing(5)

        # Header widget with button inside
        self.widget_header = QWidget()
        self.widget_header.setFixedHeight(self.FIXED_HEADER_HEIGHT)
        self.widget_header.setStyleSheet("background-color: #4A90E2;")
        header_layout = QHBoxLayout(self.widget_header)
        header_layout.setContentsMargins(10, 5, 10, 5)

        header_label = QLabel("Widget Header")
        header_label.setStyleSheet("color: white; font-weight: bold;")
        header_layout.addWidget(header_label, 1)

        # Checkable button to show/hide log
        self.checkable_button_show = QPushButton("Hide Log")
        self.checkable_button_show.setCheckable(True)
        self.checkable_button_show.setChecked(True)
        self.checkable_button_show.setStyleSheet("""
            QPushButton {
                background-color: #5CB85C;
                color: white;
                padding: 5px 20px;
                font-weight: bold;
                border: none;
                border-radius: 3px;
            }
            QPushButton:checked {
                background-color: #D9534F;
            }
        """)
        self.checkable_button_show.clicked.connect(self.toggle_log)
        header_layout.addWidget(self.checkable_button_show)

        left_layout.addWidget(self.widget_header)

        # Model browser widget
        self.widget_model_browser = QLabel("Widget Model Browser")
        self.widget_model_browser.setStyleSheet("background-color: #F0AD4E; padding: 10px;")
        self.widget_model_browser.setFixedHeight(self.FIXED_BROWSER_HEIGHT)
        left_layout.addWidget(self.widget_model_browser)

        # Bottom section with grid layout
        bottom_widget = QWidget()
        grid_layout = QGridLayout(bottom_widget)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(5)

        # Left column: model widgets (width calculated from content)
        models_widget = QWidget()
        models_layout = QVBoxLayout(models_widget)
        models_layout.setContentsMargins(0, 0, 0, 0)
        models_layout.setSpacing(5)

        self.widget_pytorch_model = QLabel("PyTorch Model")
        self.widget_pytorch_model.setStyleSheet("background-color: #EE6C4D; color: white; padding: 10px;")
        models_layout.addWidget(self.widget_pytorch_model)

        self.widget_onnx_model = QLabel("ONNX Model")
        self.widget_onnx_model.setStyleSheet("background-color: #3D5A80; color: white; padding: 10px;")
        models_layout.addWidget(self.widget_onnx_model)

        self.widget_tensorrt_model = QLabel("TensorRT Model with Longer Text")
        self.widget_tensorrt_model.setStyleSheet("background-color: #98C1D9; padding: 10px;")
        models_layout.addWidget(self.widget_tensorrt_model)

        models_layout.addStretch()

        # Calculate maximum width of model widgets
        QApplication.processEvents()  # Ensure widgets are laid out
        max_width = max(
            self.widget_pytorch_model.sizeHint().width(),
            self.widget_onnx_model.sizeHint().width(),
            self.widget_tensorrt_model.sizeHint().width()
        )
        models_widget.setFixedWidth(max_width)

        grid_layout.addWidget(models_widget, 0, 0, 2, 1)

        # Metadata widget (expandable horizontally)
        self.widget_metadata = QTextEdit()
        self.widget_metadata.setPlainText("Widget Metadata\n(Expandable horizontally)")
        self.widget_metadata.setStyleSheet("background-color: #E0E0E0; padding: 10px;")
        self.widget_metadata.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        grid_layout.addWidget(self.widget_metadata, 0, 1)

        # Conversion widget (expandable vertically)
        self.widget_conversion = QTextEdit()
        self.widget_conversion.setPlainText("Widget Conversion\n(Expandable vertically)\n\nMultiple widgets can be hidden here...")
        self.widget_conversion.setStyleSheet("background-color: #C9E4CA; padding: 10px;")
        self.widget_conversion.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        grid_layout.addWidget(self.widget_conversion, 1, 1)

        # Set column stretch
        grid_layout.setColumnStretch(0, 0)  # Fixed width column
        grid_layout.setColumnStretch(1, 1)  # Expandable column

        left_layout.addWidget(bottom_widget, 1)

        main_layout.addWidget(left_widget, 1)

        # Right section: Log widget (fixed width, toggleable)
        self.widget_log = QTextEdit()
        self.widget_log.setPlainText("Widget Log\n(Fixed width)")
        self.widget_log.setStyleSheet("background-color: #2D2D2D; color: #00FF00; padding: 10px;")
        self.widget_log.setFixedWidth(self.FIXED_LOG_WIDTH)
        self.widget_log.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        main_layout.addWidget(self.widget_log)

        # Initial window size
        self.resize(900, 600)

    def toggle_log(self):
        if self.checkable_button_show.isChecked():
            # Show log
            self.widget_log.show()
            self.checkable_button_show.setText("Hide Log")
            # Increase window width
            self.resize(self.width() + self.FIXED_LOG_WIDTH, self.height())
        else:
            # Hide log
            self.widget_log.hide()
            self.checkable_button_show.setText("Show Log")
            # Decrease window width
            self.resize(self.width() - self.FIXED_LOG_WIDTH, self.height())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
