from PySide6.QtWidgets import (
    QApplication, QWidget, QToolButton, QGridLayout
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
import sys

class M3IconButton(QToolButton):
    def __init__(self, icon_path, state_name="", forced_state=None):
        super().__init__()

        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(24, 24))
        self.setCursor(Qt.PointingHandCursor)
        self.setAutoRaise(True)

        # State name shown under button
        self.setText(state_name)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # Force pseudo-state (hover/pressed/checked)
        self.forced_state = forced_state

        # Object name for unique styling
        self.setObjectName(state_name.replace(" ", "_"))

        # Base style
        base_style = """
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 8px;
                border-radius: 12px;
            }

            QToolButton:hover {
                background-color: rgba(0, 0, 0, 0.08);
            }

            QToolButton:pressed {
                background-color: rgba(0, 0, 0, 0.16);
            }

            QToolButton:checked {
                background-color: rgba(33, 150, 243, 0.20);
            }

            QToolButton:checked:hover {
                background-color: rgba(33, 150, 243, 0.30);
            }

            QToolButton:checked:pressed {
                background-color: rgba(33, 150, 243, 0.40);
            }

            QToolButton:disabled {
                background-color: transparent;
                opacity: 0.3;
            }
        """

        # Inject forced pseudo-state
        if forced_state:
            base_style += f"""
                QToolButton#{self.objectName()} {{
                    {forced_state}
                }}
            """

        self.setStyleSheet(base_style)

        # Apply logical flag for checked state
        if "checked" in state_name.lower():
            self.setCheckable(True)
            self.setChecked(True)

        if "disabled" in state_name.lower():
            self.setEnabled(False)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)

        # Icon
        icon_path = "icons/heart.svg"

        buttons = [
            ("Default", None),
            ("Hover",  "background-color: rgba(0,0,0,0.08);"),
            ("Pressed", "background-color: rgba(0,0,0,0.16);"),
            ("Disabled", None),
            ("Checked", None),
            ("Checked Hover", "background-color: rgba(33,150,243,0.30);"),
            ("Checked Pressed", "background-color: rgba(33,150,243,0.40);"),
        ]

        row = 0
        col = 0
        for name, pseudo in buttons:
            btn = M3IconButton(icon_path, name, pseudo)
            layout.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.setWindowTitle("Material 3 Icon Button — All States")
        self.setStyleSheet("background:white;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())
