from PySide6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout,
                               QLabel, QPushButton, QComboBox, QLineEdit, QScrollArea,
                               QWidget, QFrame, QFileDialog, QSpinBox, QMainWindow)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
import sys


class HSwitch(QWidget):
    """Custom horizontal switch widget"""
    toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 24)
        self._checked = False

    def paintEvent(self, event):
        from PySide6.QtGui import QPainter, QColor
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        if self._checked:
            painter.setBrush(QColor(0, 120, 215))
        else:
            painter.setBrush(QColor(160, 160, 160))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, 50, 24, 12, 12)

        # Handle
        painter.setBrush(QColor(255, 255, 255))
        x = 28 if self._checked else 2
        painter.drawEllipse(x, 2, 20, 20)

    def mousePressEvent(self, event):
        self._checked = not self._checked
        self.toggled.emit(self._checked)
        self.update()

    def isChecked(self):
        return self._checked

    def setChecked(self, checked):
        self._checked = checked
        self.update()


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True)
        self.parent_window = parent

        # Store default values
        self.defaults = {
            'reload_model': True,
            'gpu': 0,
            'output_folder': '',
            'onnx_opset': 11,
            'tensorrt_opt': 3,
            'show_log': False,
            'dev_mode': False,
            'auto_save': True,
            'parallel_processing': False,
            'high_quality': True,
            'preserve_alpha': False,
            'use_cache': True,
            'verbose_logging': False,
            'auto_update': True,
            'theme_dark': False,
            'notifications': True,
            'compress_output': False
        }

        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Title bar
        title_bar = QFrame()
        title_bar.setStyleSheet("background-color: #2b2b2b; padding: 10px;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 10, 15, 10)

        title_label = QLabel("Settings")
        title_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        # Minimize button
        min_btn = QPushButton("−")
        min_btn.setFixedSize(30, 30)
        min_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)
        min_btn.clicked.connect(self.showMinimized)
        title_layout.addWidget(min_btn)

        main_layout.addWidget(title_bar)

        # Scroll area for settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background-color: white;")

        # Content widget
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # Add settings
        self.reload_switch = self.add_switch_setting(content_layout, "Reload previous model on startup")
        self.gpu_combo = self.add_combo_setting(content_layout, "Default graphic card",
                                                ["GPU 0 (NVIDIA RTX 4090)", "GPU 1 (Intel UHD)", "CPU"])
        self.output_folder = self.add_folder_setting(content_layout, "Persistent output folder")

        # Default values section
        defaults_label = QLabel("Default Values")
        defaults_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        content_layout.addWidget(defaults_label)

        self.onnx_opset = self.add_spinbox_setting(content_layout, "ONNX Opset", 1, 20, 11)
        self.tensorrt_opt = self.add_spinbox_setting(content_layout, "TensorRT Optimization", 0, 5, 3)

        # More settings
        self.log_switch = self.add_switch_setting(content_layout, "Always show log panel")
        self.dev_switch = self.add_switch_setting(content_layout, "Dev mode")
        self.auto_save = self.add_switch_setting(content_layout, "Auto-save projects")
        self.parallel_proc = self.add_switch_setting(content_layout, "Enable parallel processing")
        self.high_quality = self.add_switch_setting(content_layout, "High quality mode")
        self.preserve_alpha = self.add_switch_setting(content_layout, "Preserve alpha channel")
        self.use_cache = self.add_switch_setting(content_layout, "Use cache")
        self.verbose_log = self.add_switch_setting(content_layout, "Verbose logging")
        self.auto_update = self.add_switch_setting(content_layout, "Check for updates automatically")
        self.theme_dark = self.add_switch_setting(content_layout, "Dark theme")
        self.notifications = self.add_switch_setting(content_layout, "Enable notifications")
        self.compress = self.add_switch_setting(content_layout, "Compress output files")

        content_layout.addStretch()
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # Bottom buttons
        button_frame = QFrame()
        button_frame.setStyleSheet("background-color: #f0f0f0; border-top: 1px solid #ddd;")
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(20, 15, 20, 15)

        restore_btn = QPushButton("Restore to Default")
        restore_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        restore_btn.clicked.connect(self.restore_defaults)
        button_layout.addWidget(restore_btn)

        button_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        ok_btn = QPushButton("OK")
        ok_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)

        main_layout.addWidget(button_frame)

        # Set dialog size and position
        self.resize_and_center()

    def add_switch_setting(self, layout, label_text):
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(label_text)
        row_layout.addWidget(label)
        row_layout.addStretch()

        switch = HSwitch()
        row_layout.addWidget(switch)

        layout.addWidget(row)
        return switch

    def add_combo_setting(self, layout, label_text, items):
        row = QWidget()
        row_layout = QVBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(5)

        label = QLabel(label_text)
        row_layout.addWidget(label)

        combo = QComboBox()
        combo.addItems(items)
        combo.setStyleSheet("padding: 5px;")
        row_layout.addWidget(combo)

        layout.addWidget(row)
        return combo

    def add_folder_setting(self, layout, label_text):
        row = QWidget()
        row_layout = QVBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(5)

        label = QLabel(label_text)
        row_layout.addWidget(label)

        folder_row = QWidget()
        folder_layout = QHBoxLayout(folder_row)
        folder_layout.setContentsMargins(0, 0, 0, 0)

        line_edit = QComboBox()
        line_edit.setEditable(True)
        line_edit.setStyleSheet("padding: 5px;")
        folder_layout.addWidget(line_edit)

        browse_btn = QPushButton("Browse")
        browse_btn.setStyleSheet("""
            QPushButton {
                padding: 5px 15px;
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        browse_btn.clicked.connect(lambda: self.browse_folder(line_edit))
        folder_layout.addWidget(browse_btn)

        row_layout.addWidget(folder_row)
        layout.addWidget(row)
        return line_edit

    def add_spinbox_setting(self, layout, label_text, min_val, max_val, default_val):
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(label_text)
        row_layout.addWidget(label)
        row_layout.addStretch()

        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default_val)
        spinbox.setFixedWidth(80)
        spinbox.setStyleSheet("padding: 5px;")
        row_layout.addWidget(spinbox)

        layout.addWidget(row)
        return spinbox

    def browse_folder(self, combo):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            combo.setCurrentText(folder)

    def resize_and_center(self):
        if self.parent_window:
            parent_geo = self.parent_window.geometry()
            max_height = parent_geo.height() - 50

            # Set dialog size
            width = 500
            height = min(700, max_height)
            self.resize(width, height)

            # Center in parent
            x = parent_geo.x() + (parent_geo.width() - width) // 2
            y = parent_geo.y() + (parent_geo.height() - height) // 2
            self.move(x, y)

    def load_settings(self):
        """Load current settings"""
        self.reload_switch.setChecked(self.defaults['reload_model'])
        self.gpu_combo.setCurrentIndex(self.defaults['gpu'])
        self.log_switch.setChecked(self.defaults['show_log'])
        self.dev_switch.setChecked(self.defaults['dev_mode'])
        self.auto_save.setChecked(self.defaults['auto_save'])
        self.parallel_proc.setChecked(self.defaults['parallel_processing'])
        self.high_quality.setChecked(self.defaults['high_quality'])
        self.preserve_alpha.setChecked(self.defaults['preserve_alpha'])
        self.use_cache.setChecked(self.defaults['use_cache'])
        self.verbose_log.setChecked(self.defaults['verbose_logging'])
        self.auto_update.setChecked(self.defaults['auto_update'])
        self.theme_dark.setChecked(self.defaults['theme_dark'])
        self.notifications.setChecked(self.defaults['notifications'])
        self.compress.setChecked(self.defaults['compress_output'])

    def restore_defaults(self):
        """Restore all settings to default values"""
        self.load_settings()
        self.output_folder.setCurrentText(self.defaults['output_folder'])
        self.onnx_opset.setValue(self.defaults['onnx_opset'])
        self.tensorrt_opt.setValue(self.defaults['tensorrt_opt'])

    def changeEvent(self, event):
        """Handle minimize event for parent window"""
        from PySide6.QtCore import QEvent
        if event.type() == QEvent.WindowStateChange:
            if self.parent_window and self.windowState() & Qt.WindowMinimized:
                self.parent_window.showMinimized()
        super().changeEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        central = QWidget()
        layout = QVBoxLayout(central)

        btn = QPushButton("Open Settings")
        btn.clicked.connect(self.open_settings)
        layout.addWidget(btn)

        self.setCentralWidget(central)

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    def changeEvent(self, event):
        """Prevent main window state changes when dialog is open"""
        from PySide6.QtCore import QEvent
        if event.type() == QEvent.WindowStateChange:
            for child in self.children():
                if isinstance(child, SettingsDialog) and child.isVisible():
                    if self.windowState() & Qt.WindowMinimized:
                        child.showMinimized()
        super().changeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
