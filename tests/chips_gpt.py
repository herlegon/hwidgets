from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt
import sys

class FilterChip(QPushButton):
    def __init__(self, text, icon_path, parent=None):
        super().__init__(text, parent)
        self.icon_path = icon_path

        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(32)  # M3 standard chip height

        self.update_icon()
        self.setStyleSheet(self.build_stylesheet())

        # Connect toggle signal
        self.toggled.connect(self.update_icon)

    def build_stylesheet(self):
        return """
    QPushButton {
        border: none;
        padding: 4px 12px;
        border-radius: 8px;
        background-color: #00000010;  /* rgba(0,0,0,0.06) ≈ 0F in hex */
        color: #000000;
        font-size: 14px;
        text-align: left;
    }
    QPushButton:hover {
        background-color: #0000001F;  /* rgba(0,0,0,0.12) ≈ 1F */
    }
    QPushButton:pressed {
        background-color: #0000002E;  /* rgba(0,0,0,0.18) ≈ 2E */
    }
    QPushButton:checked {
        background-color: #2196F333;  /* rgba(33,150,243,0.20) ≈ 33 */
    }
    QPushButton:checked:hover {
        background-color: #2196F33F;  /* rgba(33,150,243,0.25) ≈ 3F */
    }
    QPushButton:checked:pressed {
        background-color: #2196F355;  /* rgba(33,150,243,0.35) ≈ 55 */
    }
        """

    def update_icon(self):
        if self.isChecked():
            self.setIcon(QIcon(self.icon_path))
            self.setIconSize(QSize(18, 18))
        else:
            self.setIcon(QIcon())  # Remove icon when unchecked


class Window(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)

        # Filter chip — icon visible only when checked
        filter_chip = FilterChip("Filter", "icons/filter.svg")
        layout.addWidget(filter_chip)

        filter_chip2 = FilterChip("Filter2", "icons/filter.svg")
        layout.addWidget(filter_chip2)

        layout.addStretch()
        self.setWindowTitle("Filter Chip: Icon Only When Checked")
        self.setStyleSheet("background:white;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())
