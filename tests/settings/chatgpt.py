from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox,
    QLineEdit, QPushButton, QCheckBox, QLabel, QFileDialog, QScrollArea, QWidget,
    QSpacerItem, QSizePolicy, QScrollArea, QDialogButtonBox
)
from PySide6.QtCore import Qt, QSize

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove the window borders and titlebar
        self.setWindowTitle("Settings")

        # Center the dialog and set the maximum height
        self.setGeometry(parent.geometry())  # Place in the center of the parent window
        dialog_height = parent.height() - 50  # Make sure dialog height is not greater than the parent height minus 50px
        self.setFixedHeight(min(dialog_height, 600))  # You can adjust the max height as needed
        self.setFixedWidth(400)

        # Main layout
        main_layout = QVBoxLayout(self)

        # Scroll area to handle long settings
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        settings_widget = QWidget()
        scroll_area.setWidget(settings_widget)
        settings_layout = QFormLayout(settings_widget)

        # Add settings controls
        settings_layout.addRow("Reload previous model on startup:", QCheckBox())  # HSwitch can be replaced with QCheckBox for now
        settings_layout.addRow("Default Graphic Card:", QComboBox())  # Read-only combobox
        settings_layout.addRow("Persistent Output Folder:", QLineEdit())  # Editable combobox (just line edit for simplicity)
        settings_layout.addRow("Always show log panel:", QCheckBox())  # HSwitch can be replaced with QCheckBox for now
        settings_layout.addRow("Dev mode:", QCheckBox())  # HSwitch can be replaced with QCheckBox for now

        # Adding 10 random settings to the form
        for i in range(10):
            settings_layout.addRow(f"Random Setting {i+1}:", QCheckBox())  # Random switch-like settings

        # Add restore to default button
        restore_button = QPushButton("Restore to Default")
        restore_button.clicked.connect(self.restore_to_default)

        # Add the bottom buttons: Cancel and Ok
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # Bottom layout for buttons and restore button
        button_layout = QHBoxLayout()
        button_layout.addWidget(restore_button)
        button_layout.addStretch()
        button_layout.addWidget(buttons)

        # Add everything to the main layout
        main_layout.addWidget(scroll_area)
        main_layout.addLayout(button_layout)

        # Prevent the dialog from moving
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Allow minimize and resize
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint)

    def restore_to_default(self):
        # Logic for restoring to default values can be added here
        print("Restore to default settings.")

if __name__ == "__main__":
    app = QApplication([])

    # Main window to show the dialog
    parent_window = QWidget()
    parent_window.setWindowTitle("Main Window")
    parent_window.resize(800, 600)
    parent_window.show()

    # Open the settings dialog
    settings_dialog = SettingsDialog(parent=parent_window)
    settings_dialog.exec()

    app.exec()
