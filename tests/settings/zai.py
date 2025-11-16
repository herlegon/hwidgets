import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog, QVBoxLayout,
                               QHBoxLayout, QPushButton, QScrollArea, QWidget,
                               QLabel, QComboBox, QLineEdit, QFrame, QSizePolicy)
from PySide6.QtCore import Qt, QSize, QRect, QEvent
from PySide6.QtGui import QIcon

# Custom HSwitch widget (toggle switch)
class HSwitch(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 26)
        self.setStyleSheet("""
            HSwitch {
                border-radius: 13px;
                background-color: #cccccc;
            }
            HSwitch[checked="true"] {
                background-color: #4CAF50;
            }
        """)

        self._checked = False
        self.setProperty("checked", self._checked)

        self.handle = QFrame(self)
        self.handle.setFixedSize(22, 22)
        self.handle.setStyleSheet("""
            QFrame {
                border-radius: 11px;
                background-color: white;
            }
        """)
        self.handle.move(2, 2)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle()

    def toggle(self):
        self._checked = not self._checked
        self.setProperty("checked", self._checked)
        self.style().unpolish(self)
        self.style().polish(self)

        if self._checked:
            self.handle.move(26, 2)
        else:
            self.handle.move(2, 2)

    def isChecked(self):
        return self._checked

    def setChecked(self, checked):
        if self._checked != checked:
            self.toggle()

# Settings Dialog
class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent

        # Make dialog frameless but with minimize button
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowMinimizeButtonHint)
        # Remove the close button by overriding the close event
        self.closeEvent = lambda e: e.ignore()

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Title bar with "Restore to default" button and minimize button
        self.title_bar = QFrame()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet("background-color: #f0f0f0;")
        self.title_bar.mousePressEvent = self.title_bar_mouse_press
        self.title_bar.mouseMoveEvent = self.title_bar_mouse_move

        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)

        self.title_label = QLabel("Settings")
        self.title_label.setStyleSheet("font-weight: bold;")

        self.minimize_button = QPushButton("—")
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
                border-radius: 15px;
            }
        """)

        self.restore_button = QPushButton("Restore to Default")
        self.restore_button.clicked.connect(self.restore_defaults)

        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.restore_button)
        title_layout.addWidget(self.minimize_button)

        # Content area with scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)

        # Add settings
        self.add_settings()

        self.scroll_area.setWidget(self.content_widget)

        # Button area at the bottom
        self.button_frame = QFrame()
        self.button_frame.setFixedHeight(50)
        self.button_layout = QHBoxLayout(self.button_frame)
        self.button_layout.setContentsMargins(10, 10, 10, 10)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)

        self.button_layout.addStretch()
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.ok_button)

        # Add all components to main layout
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.button_frame)

        # Set size and position
        self.resize(500, min(600, parent.height() - 50))
        self.center_dialog()

        # Style
        self.setStyleSheet("""
            QPushButton {
                padding: 5px 15px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: white;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
            QLabel {
                padding: 5px 0;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                min-width: 150px;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
        """)

        # For dragging the dialog
        self.drag_position = None

    def title_bar_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def title_bar_mouse_move(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPosition().toPoint() - self.drag_position)

    def center_dialog(self):
        if self.parent_window:
            parent_rect = self.parent_window.geometry()
            dialog_rect = self.geometry()

            x = parent_rect.x() + (parent_rect.width() - dialog_rect.width()) // 2
            y = parent_rect.y() + (parent_rect.height() - dialog_rect.height()) // 2

            self.move(x, y)

    def add_settings(self):
        # Setting 1: Reload previous model on startup
        setting1_layout = QHBoxLayout()
        setting1_label = QLabel("Reload previous model on startup:")
        self.reload_switch = HSwitch()
        setting1_layout.addWidget(setting1_label)
        setting1_layout.addStretch()
        setting1_layout.addWidget(self.reload_switch)
        self.content_layout.addLayout(setting1_layout)

        # Setting 2: Default graphic card
        setting2_layout = QHBoxLayout()
        setting2_label = QLabel("Default graphic card:")
        self.graphic_card_combo = QComboBox()
        self.graphic_card_combo.addItems(["NVIDIA GTX 1080", "AMD Radeon RX 580", "Intel HD Graphics"])
        self.graphic_card_combo.setEditable(False)
        setting2_layout.addWidget(setting2_label)
        setting2_layout.addStretch()
        setting2_layout.addWidget(self.graphic_card_combo)
        self.content_layout.addLayout(setting2_layout)

        # Setting 3: Persistent output folder
        setting3_layout = QHBoxLayout()
        setting3_label = QLabel("Persistent output folder:")
        self.output_folder_combo = QComboBox()
        self.output_folder_combo.setEditable(True)
        self.output_folder_combo.addItems(["/home/user/output", "/data/output", "/tmp/output"])
        self.browse_button = QPushButton("Browse...")
        self.browse_button.setMaximumWidth(80)
        setting3_layout.addWidget(setting3_label)
        setting3_layout.addWidget(self.output_folder_combo)
        setting3_layout.addWidget(self.browse_button)
        self.content_layout.addLayout(setting3_layout)

        # Setting 4: Always show log panel
        setting4_layout = QHBoxLayout()
        setting4_label = QLabel("Always show log panel:")
        self.log_panel_switch = HSwitch()
        setting4_layout.addWidget(setting4_label)
        setting4_layout.addStretch()
        setting4_layout.addWidget(self.log_panel_switch)
        self.content_layout.addLayout(setting4_layout)

        # Setting 5: Dev mode
        setting5_layout = QHBoxLayout()
        setting5_label = QLabel("Dev mode:")
        self.dev_mode_switch = HSwitch()
        setting5_layout.addWidget(setting5_label)
        setting5_layout.addStretch()
        setting5_layout.addWidget(self.dev_mode_switch)
        self.content_layout.addLayout(setting5_layout)

        # Add 10 more random settings to demonstrate scrollbar
        for i in range(6, 16):
            setting_layout = QHBoxLayout()
            setting_label = QLabel(f"Random Setting {i}:")
            setting_switch = HSwitch()
            setting_layout.addWidget(setting_label)
            setting_layout.addStretch()
            setting_layout.addWidget(setting_switch)
            self.content_layout.addLayout(setting_layout)

    def restore_defaults(self):
        # Implement restore defaults logic
        self.reload_switch.setChecked(False)
        self.graphic_card_combo.setCurrentIndex(0)
        self.output_folder_combo.setCurrentIndex(0)
        self.log_panel_switch.setChecked(False)
        self.dev_mode_switch.setChecked(False)

        # Reset all other switches
        for i in range(self.content_layout.count()):
            item = self.content_layout.itemAt(i)
            if item and item.layout():
                for j in range(item.layout().count()):
                    widget = item.layout().itemAt(j).widget()
                    if isinstance(widget, HSwitch):
                        widget.setChecked(False)

# Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application")
        self.resize(800, 600)

        # Add a button to open settings
        button = QPushButton("Open Settings", self)
        button.clicked.connect(self.open_settings)
        button.move(350, 275)
        button.resize(100, 50)

    def open_settings(self):
        # Store current position to prevent movement
        original_pos = self.pos()

        # Create and show settings dialog
        dialog = SettingsDialog(self)
        result = dialog.exec()

        # Restore original position
        self.move(original_pos)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                # Handle minimize event if needed
                pass
        super().changeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
