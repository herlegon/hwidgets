import sys
from PySide6.QtWidgets import (QApplication, QWidget, QToolButton,
                               QHBoxLayout, QButtonGroup)
from PySide6.QtCore import Qt

QSS = """
QWidget {
    /* Base font settings */
    font-family: Roboto, Arial, sans-serif;
}

QToolButton {
    /* Basic Material-like properties */
    border: 1px solid #BBBBBB;
    background-color: #FFFFFF;
    color: #424242;
    padding: 8px 16px;
    outline: none;

    /* chatgpt */
    border-style: solid;
    border-color: #BBBBBB;
}

/* --- Unchecked States --- */
QToolButton:hover {
    background-color: #F5F5F5;
}
QToolButton:pressed {
    background-color: #EEEEEE;
}

/* --- Checked/Selected State (Primary Color) --- */
QToolButton:checked {
    border-color: #2196F3;
    background-color: #2196F3;
    color: #FFFFFF;
    /* Remove hover effect from checked button for solid look */
}

QToolButton:checked:hover {
    background-color: #2196F3; /* Same as checked */
}

/* --- Shape and Borders (The "Segmented" Look) --- */

QToolButton#segment-left {
    border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
    border-right-width: 0;
}

QToolButton#segment-center {
    border-radius: 0;
    border-right-width: 0;
}

QToolButton#segment-right {
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
}

/* Restore borders on selected segments */
QToolButton#segment-left:checked {
    border-right-width: 1px;
}
QToolButton#segment-center:checked {
    border-left-width: 1px;
    border-right-width: 1px;
}
QToolButton#segment-right:checked {
    border-left-width: 1px;
}
"""

class MaterialButtonGroup(QWidget):
    def __init__(self, buttons, parent=None):
        super().__init__(parent)

        # Visual Layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Logical Group
        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        for i, text in enumerate(buttons):
            button = QToolButton()
            button.setText(text)
            button.setCheckable(True)
            button.setFixedHeight(24)

            # Set object name for QSS targeting
            if i == 0:
                button.setObjectName("segment-left")
            elif i == len(buttons) - 1:
                button.setObjectName("segment-right")
            else:
                button.setObjectName("segment-center")

            self.group.addButton(button, i)
            self.layout.addWidget(button)

        # Ensure the first button is checked by default
        if self.group.buttons():
            self.group.buttons()[0].setChecked(True)

        # Optional: Connect a signal for utility
        self.group.buttonClicked.connect(self.on_button_clicked)

    def on_button_clicked(self, button):
        print(f"Button clicked: {button.text()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply the custom stylesheet
    app.setStyleSheet(QSS)

    main_window = QWidget()
    main_window.setWindowTitle("Custom Material Button Group")

    main_layout = QHBoxLayout(main_window)

    # Create the button group
    group = MaterialButtonGroup(["Daily", "Weekly", "Monthly", "Yearly"])

    main_layout.addWidget(group, alignment=Qt.AlignCenter)

    main_window.show()
    sys.exit(app.exec())
