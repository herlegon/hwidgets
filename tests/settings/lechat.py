import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QDialog, QHBoxLayout, QScrollArea, QCheckBox, QComboBox, QLabel, QSpinBox
)
from PySide6.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Main layout
        main_layout = QVBoxLayout(self)

        # Restore to default button (top-right)
        restore_btn = QPushButton("Restore to Default")
        restore_btn.setFixedWidth(150)
        restore_btn.clicked.connect(self.restore_defaults)
        main_layout.addWidget(restore_btn, alignment=Qt.AlignRight)

        # Scroll area for settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Add settings widgets
        self.add_setting(scroll_layout, "Reload previous model on startup", QCheckBox())
        self.add_setting(scroll_layout, "Default graphic card", self.create_readonly_combobox(["NVIDIA", "AMD", "Intel"]))
        self.add_setting(scroll_layout, "Persistent output folder", self.create_editable_combobox())
        self.add_setting(scroll_layout, "Always show log panel", QCheckBox())
        self.add_setting(scroll_layout, "Dev mode", QCheckBox())
        self.add_setting(scroll_layout, "Auto-save interval", self.create_spinbox())
        self.add_setting(scroll_layout, "Theme", self.create_combobox(["Light", "Dark", "System"]))
        self.add_setting(scroll_layout, "Language", self.create_combobox(["English", "French", "Spanish"]))
        self.add_setting(scroll_layout, "Enable notifications", QCheckBox())
        self.add_setting(scroll_layout, "Enable analytics", QCheckBox())
        self.add_setting(scroll_layout, "Enable dark mode", QCheckBox())
        self.add_setting(scroll_layout, "Enable auto-update", QCheckBox())
        self.add_setting(scroll_layout, "Enable cloud sync", QCheckBox())
        self.add_setting(scroll_layout, "Enable hardware acceleration", QCheckBox())

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # Buttons layout (bottom-right)
        buttons = QHBoxLayout()
        buttons.addStretch()
        cancel_btn = QPushButton("Cancel")
        ok_btn = QPushButton("OK")
        buttons.addWidget(cancel_btn)
        buttons.addWidget(ok_btn)
        main_layout.addLayout(buttons)

        # Size and position
        self.adjustSize()
        if parent:
            self.setMaximumHeight(parent.height() - 50)
            self.move(parent.rect().center() - self.rect().center())

    def add_setting(self, layout, label, widget):
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(label))
        hbox.addWidget(widget)
        layout.addLayout(hbox)

    def create_readonly_combobox(self, items):
        cb = QComboBox()
        cb.addItems(items)
        cb.setEnabled(False)
        return cb

    def create_editable_combobox(self):
        cb = QComboBox()
        cb.setEditable(True)
        cb.addItems(["C:/Output", "D:/Projects/Output"])
        return cb

    def create_combobox(self, items):
        cb = QComboBox()
        cb.addItems(items)
        return cb

    def create_spinbox(self):
        sb = QSpinBox()
        sb.setRange(1, 60)
        return sb

    def restore_defaults(self):
        print("Restore defaults clicked")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings Dialog Demo")
        self.setGeometry(100, 100, 600, 400)

        btn = QPushButton("Open Settings", self)
        btn.clicked.connect(self.open_settings)
        btn.setFixedSize(150, 30)

        layout = QVBoxLayout()
        layout.addWidget(btn, alignment=Qt.AlignCenter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_settings(self):
        dlg = SettingsDialog(self)
        dlg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
