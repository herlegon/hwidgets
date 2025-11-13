from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QTimer

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)

        # Main layout
        self.main_layout = QHBoxLayout(self)

        # Left Panel Layout (with a checkbox to control visibility)
        self.left_layout = QVBoxLayout()
        self.left_widget = QWidget()
        self.left_widget.setLayout(self.left_layout)
        self.left_widget.setFixedWidth(150)  # Fixed width for the left panel

        # Checkbox to toggle visibility of the log widget
        self.toggle_checkbox = QCheckBox("Show Log")
        self.toggle_checkbox.stateChanged.connect(self.toggle_log_visibility)
        self.left_layout.addWidget(self.toggle_checkbox)

        # Right Panel Layout (for the log widget)
        self.right_layout = QVBoxLayout()
        self.widget_log = QPushButton("Log")
        self.widget_log.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_layout.addWidget(self.widget_log)
        self.right_widget = QWidget()
        self.right_widget.setLayout(self.right_layout)

        # Add left and right widgets to the main layout
        self.main_layout.addWidget(self.left_widget)
        self.main_layout.addWidget(self.right_widget)

        self.setLayout(self.main_layout)

    def toggle_log_visibility(self, state: int) -> None:
        # Get the current window width and calculate the log widget width
        window_width = self.width()
        log_width = self.widget_log.width() + 2 * self.main_layout.spacing()

        # Check current visibility status
        was_visible = self.widget_log.isVisible()

        if was_visible and state == Qt.Unchecked:  # Hiding the log widget
            print(f"set to hide: {window_width} - {log_width}")
            self.widget_log.hide()
            self.right_widget.hide()  # Make sure to hide the parent widget as well
            QTimer.singleShot(0, lambda: self.resize(window_width - log_width, self.height()))  # Defer resize
            self.updateGeometry()  # Update the layout after the widget is hidden
        elif not was_visible and state == Qt.Checked:  # Showing the log widget
            print(f"set to visible: {window_width} + {log_width}")
            self.widget_log.show()
            self.right_widget.show()  # Ensure the parent widget is shown too
            QTimer.singleShot(0, lambda: self.resize(window_width + log_width, self.height()))  # Defer resize
            self.updateGeometry()  # Update the layout after the widget is shown

if __name__ == "__main__":
    app = QApplication([])
    win = MyWindow()
    win.show()
    app.exec()
