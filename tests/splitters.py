from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QSplitter, QVBoxLayout, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt

# Assuming these widget classes are already defined (HeaderWidget, ModelBrowserWidget, etc.)
class HeaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: lightyellow; border: 2px solid red;")
        # Set up HeaderWidget layout here

class ModelBrowserWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: khaki; border: 2px solid green;")
        # Set up ModelBrowserWidget layout here

class PyTorchWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: lightblue; border: 2px solid blue;")
        # Set up PyTorchWidget layout here

class OnnxWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: lightgreen; border: 2px solid orange;")
        # Set up OnnxWidget layout here

class TensorRTWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: lightcoral; border: 2px solid purple;")
        # Set up TensorRTWidget layout here

class MetadataWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: lightgray; border: 2px solid pink;")
        # Set up MetadataWidget layout here

class ConversionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: lavender; border: 2px solid brown;")
        # Set up ConversionWidget layout here

class LogWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: lightyellow; border: 2px solid black;")
        # Set up LogWidget layout here

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Central widget for the QMainWindow
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setStyleSheet("background-color: #f0f0f0; border: 1px solid gray;")

        # ------------------------
        # Header and Model Browser
        self.widget_header = HeaderWidget(self.central_widget)
        self.widget_model_browser = ModelBrowserWidget(self.central_widget)

        # ------------------------
        # Create layout for the left side (PyTorch, ONNX, TensorRT)
        left_layout = QVBoxLayout()
        self.widget_pytorch_model = PyTorchWidget(self.central_widget)
        self.widget_onnx_model = OnnxWidget(self.central_widget)
        self.widget_tensorrt_model = TensorRTWidget(self.central_widget)
        left_layout.addWidget(self.widget_pytorch_model)
        left_layout.addWidget(self.widget_onnx_model)
        left_layout.addWidget(self.widget_tensorrt_model)

        # ------------------------
        # Create layout for the right side (Metadata, Conversion)
        right_layout = QVBoxLayout()
        self.widget_metadata = MetadataWidget(self.central_widget)
        self.widget_conversion = ConversionWidget(self.central_widget)
        right_layout.addWidget(self.widget_metadata)
        right_layout.addWidget(self.widget_conversion)

        # ------------------------
        # Log Viewer widget
        self.widget_log = LogWidget(self.central_widget)

        # ------------------------
        # Nested Splitter Layout
        main_splitter = QSplitter(Qt.Horizontal)

        # Left side splitter: Vertical layout with PyTorch, ONNX, and TensorRT widgets
        left_splitter = QSplitter(Qt.Vertical)
        left_splitter.addWidget(self.widget_header)
        left_splitter.addWidget(self.widget_model_browser)
        left_splitter.addWidget(self.widget_pytorch_model)
        left_splitter.addWidget(self.widget_onnx_model)
        left_splitter.addWidget(self.widget_tensorrt_model)
        left_splitter.setHandleWidth(0)  # Disable the handle

        # Right side layout with Metadata, Conversion widgets and Log viewer
        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.addWidget(self.widget_metadata)
        right_splitter.addWidget(self.widget_conversion)
        right_splitter.addWidget(self.widget_log)
        right_splitter.setHandleWidth(0)  # Disable the handle

        # Add the left and right splitters to the main horizontal splitter
        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(right_splitter)
        main_splitter.setHandleWidth(0)  # Disable the handle for the main splitter

        # Set the layout to the central widget
        central_layout = QVBoxLayout(self.central_widget)
        central_layout.addWidget(main_splitter)

        # Set window properties
        self.setWindowTitle("Main Window with Nested Splitters and Debug Styles")
        self.resize(1200, 800)  # Adjust window size as necessary

        # ------------------------
        # Button callback to toggle log panel by resizing window
        toggleButton = QPushButton("Show/Hide Log", self.central_widget)
        toggleButton.clicked.connect(self.toggle_log)
        central_layout.addWidget(toggleButton)

    def toggle_log(self):
        log_width = self.widget_log.width()
        window_width = self.width()
        if self.widget_log.isHidden():
            self.widget_log.show()
            self.resize(window_width + log_width, self.height())
        else:
            self.resize(window_width - log_width, self.height())
            self.widget_log.hide()


# Main application loop
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


+---------------------------------------------------+-----------------------+
|    widget_header            checkable_button_show |       widget_log      |
+---------------------------------------------------+                       |
|    widget_model_browser                           |                       |
+---------------------------------------------------+                       |
|  widget_pytorch_model     |   widget_metadata     |                       |
+---------------------------+                       |                       |
|  widget_onnx_model        +-----------------------+                       |
+---------------------------+                       |                       |
|  widget_tensorrt_model    |                       |                       |
+---------------------------+  widget_conversion    |                       |
|                           |                       |                       |
|                           |                       |                       |
|                           |                       |                       |
+---------------------------+-----------------------+-----------------------+

|  widget_pytorch_model
+--------------------------
|  widget_onnx_model
+--------------------------
|  widget_tensorrt_model




