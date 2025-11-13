from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QSizePolicy, QSplitter
)
from PySide6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # --- Widgets ---
        self.widget_header = QFrame()
        self.widget_header.setFrameShape(QFrame.Box)
        self.widget_header.setFixedHeight(50)

        self.checkable_button_show = QPushButton("Show Log")
        self.checkable_button_show.setCheckable(True)
        self.checkable_button_show.setChecked(True)
        self.checkable_button_show.clicked.connect(self.toggle_log)

        self.widget_model_browser = QFrame()
        self.widget_model_browser.setFrameShape(QFrame.Box)
        self.widget_model_browser.setFixedHeight(120)

        # Fixed-width widgets
        self.widget_pytorch_model = QFrame()
        self.widget_pytorch_model.setFrameShape(QFrame.Box)
        self.widget_pytorch_model.setFixedWidth(200)

        self.widget_onnx_model = QFrame()
        self.widget_onnx_model.setFrameShape(QFrame.Box)
        self.widget_onnx_model.setFixedWidth(200)

        self.widget_tensorrt_model = QFrame()
        self.widget_tensorrt_model.setFrameShape(QFrame.Box)
        self.widget_tensorrt_model.setFixedWidth(200)

        # Expandable horizontally
        self.widget_metadata = QFrame()
        self.widget_metadata.setFrameShape(QFrame.Box)
        self.widget_metadata.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Expandable vertically
        self.widget_conversion = QFrame()
        self.widget_conversion.setFrameShape(QFrame.Box)
        self.widget_conversion.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Fixed width log panel
        self.widget_log = QFrame()
        self.widget_log.setFrameShape(QFrame.Box)
        self.widget_log.setFixedWidth(300)

        # --- Layout Composition ---

        # Left column layout (models + conversion)
        left_layout = QVBoxLayout()
        left_layout.setSpacing(2)
        left_layout.addWidget(self.widget_pytorch_model)
        left_layout.addWidget(self.widget_onnx_model)
        left_layout.addWidget(self.widget_tensorrt_model)
        left_layout.addWidget(self.widget_conversion)
        left_layout.setStretch(3, 1)  # conversion grows vertically

        # Middle column (metadata)
        middle_layout = QVBoxLayout()
        middle_layout.addWidget(self.widget_metadata)

        # Combine left + middle into horizontal layout
        bottom_layout = QHBoxLayout()
        bottom_layout.addLayout(left_layout)
        bottom_layout.addLayout(middle_layout)

        # Top layout (header + toggle button + log)
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.widget_header)
        top_layout.addWidget(self.checkable_button_show)
        top_layout.addWidget(self.widget_log)

        # Full layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(5)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.widget_model_browser)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Model Tool GUI Layout")
        self.resize(1100, 700)

    def toggle_log(self, checked):
        if checked:
            self.widget_log.show()
            self.checkable_button_show.setText("Hide Log")
            self.adjustSize()
        else:
            self.widget_log.hide()
            self.checkable_button_show.setText("Show Log")
            self.adjustSize()


if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()
