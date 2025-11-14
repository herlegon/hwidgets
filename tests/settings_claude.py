from PySide6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QScrollArea, QWidget, QMainWindow,
                               QComboBox, QFrame, QFileDialog, QGridLayout)
from PySide6.QtCore import Qt, QPoint, QSize, Signal, QRect, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QMouseEvent, QPainter, QColor
import sys


class HSwitch(QWidget):
    """Horizontal toggle switch widget"""
    toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._checked = False
        self._circle_position = 0
        self.setFixedSize(50, 26)
        self.setCursor(Qt.PointingHandCursor)

        # Animation
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(150)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw background track
        if self._checked:
            painter.setBrush(QColor("#0d6efd"))
        else:
            painter.setBrush(QColor("#ccc"))

        painter.setPen(Qt.NoPen)
        track_rect = QRect(0, 0, self.width(), self.height())
        painter.drawRoundedRect(track_rect, self.height() / 2, self.height() / 2)

        # Draw circle
        painter.setBrush(QColor("white"))
        circle_x = int(self._circle_position)
        circle_y = 3
        circle_diameter = self.height() - 6
        painter.drawEllipse(circle_x, circle_y, circle_diameter, circle_diameter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle()

    def toggle(self):
        self._checked = not self._checked
        self.animate_circle()
        self.toggled.emit(self._checked)

    def setChecked(self, checked):
        if self._checked != checked:
            self._checked = checked
            self.animate_circle()

    def isChecked(self):
        return self._checked

    def animate_circle(self):
        start_pos = self._circle_position
        end_pos = self.width() - self.height() + 3 if self._checked else 3

        self.animation.stop()
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.start()

    def get_circle_position(self):
        return self._circle_position

    def set_circle_position(self, pos):
        self._circle_position = pos
        self.update()

    circle_position = Property(float, get_circle_position, set_circle_position)

    def showEvent(self, event):
        super().showEvent(event)
        # Set initial position without animation
        self._circle_position = self.width() - self.height() + 3 if self._checked else 3
        self.update()


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # For dragging
        self.drag_position = QPoint()

        # Store default values
        self.defaults = {
            'reload_previous_model': True,
            'default_graphic_card': 'NVIDIA GeForce RTX 3080',
            'persistent_output_folder': 'C:/Users/Output',
            'always_show_log_panel': False,
            'dev_mode': False
        }

        # Available graphics cards (simulated)
        self.available_gpus = [
            'NVIDIA GeForce RTX 3080',
            'NVIDIA GeForce RTX 4090',
            'AMD Radeon RX 7900 XTX',
            'Intel Arc A770'
        ]

        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        # Main container with border and shadow
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Content frame
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_frame.setStyleSheet("""
            QFrame#contentFrame {
                background-color: white;
                border: 2px solid #ccc;
                border-radius: 8px;
            }
        """)

        frame_layout = QVBoxLayout(content_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        # Title bar
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: #f0f0f0; border-radius: 6px 6px 0 0;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 10, 15, 10)

        title_label = QLabel("Settings")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(24, 24)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #666;
                font-size: 16px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #e81123;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.reject)
        title_layout.addWidget(close_btn)

        frame_layout.addWidget(title_bar)

        # Scroll area for settings
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # Settings content
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.setContentsMargins(20, 20, 20, 20)
        settings_layout.setSpacing(20)

        # Store widgets
        self.widgets = {}

        # Common style for combo boxes
        combo_style = """
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px 10px;
                background-color: white;
                min-height: 24px;
            }
            QComboBox:hover {
                border: 1px solid #999;
            }
            QComboBox:focus {
                border: 1px solid #0d6efd;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid #666;
                margin-right: 5px;
            }
            QComboBox:disabled {
                background-color: #f0f0f0;
                color: #666;
            }
        """

        # 1. Reload previous model on startup
        reload_row = QWidget()
        reload_layout = QHBoxLayout(reload_row)
        reload_layout.setContentsMargins(0, 0, 0, 0)
        reload_label = QLabel("Reload previous model on startup:")
        reload_layout.addWidget(reload_label)
        reload_layout.addStretch()
        self.widgets['reload_previous_model'] = HSwitch()
        reload_layout.addWidget(self.widgets['reload_previous_model'])
        settings_layout.addWidget(reload_row)

        # 2. Default graphic card (read-only)
        settings_layout.addWidget(QLabel("Default graphic card:"))
        self.widgets['default_graphic_card'] = QComboBox()
        self.widgets['default_graphic_card'].addItems(self.available_gpus)
        self.widgets['default_graphic_card'].setEnabled(False)  # Read-only
        self.widgets['default_graphic_card'].setStyleSheet(combo_style)
        settings_layout.addWidget(self.widgets['default_graphic_card'])

        # 3. Persistent output folder (editable combo + browse)
        settings_layout.addWidget(QLabel("Persistent output folder:"))
        folder_row = QWidget()
        folder_layout = QHBoxLayout(folder_row)
        folder_layout.setContentsMargins(0, 0, 0, 0)
        folder_layout.setSpacing(8)

        self.widgets['persistent_output_folder'] = QComboBox()
        self.widgets['persistent_output_folder'].setEditable(True)
        self.widgets['persistent_output_folder'].addItems([
            'C:/Users/Output',
            'D:/Projects/Output',
            'E:/Renders'
        ])
        self.widgets['persistent_output_folder'].setStyleSheet(combo_style)
        folder_layout.addWidget(self.widgets['persistent_output_folder'], stretch=1)

        browse_btn = QPushButton("Browse...")
        browse_btn.setFixedWidth(90)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px 12px;
                color: #333;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border: 1px solid #999;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
        """)
        browse_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(browse_btn)

        settings_layout.addWidget(folder_row)

        # 4. Always show log panel
        log_row = QWidget()
        log_layout = QHBoxLayout(log_row)
        log_layout.setContentsMargins(0, 0, 0, 0)
        log_label = QLabel("Always show log panel:")
        log_layout.addWidget(log_label)
        log_layout.addStretch()
        self.widgets['always_show_log_panel'] = HSwitch()
        log_layout.addWidget(self.widgets['always_show_log_panel'])
        settings_layout.addWidget(log_row)

        # 5. Dev mode
        dev_row = QWidget()
        dev_layout = QHBoxLayout(dev_row)
        dev_layout.setContentsMargins(0, 0, 0, 0)
        dev_label = QLabel("Dev mode:")
        dev_layout.addWidget(dev_label)
        dev_layout.addStretch()
        self.widgets['dev_mode'] = HSwitch()
        dev_layout.addWidget(self.widgets['dev_mode'])
        settings_layout.addWidget(dev_row)

        settings_layout.addStretch()

        scroll_area.setWidget(settings_widget)
        frame_layout.addWidget(scroll_area)

        # Button bar
        button_bar = QWidget()
        button_bar.setStyleSheet("background-color: #f8f8f8; border-radius: 0 0 6px 6px;")
        button_layout = QHBoxLayout(button_bar)
        button_layout.setContentsMargins(15, 10, 15, 10)

        # Restore defaults button (left side)
        restore_btn = QPushButton("Restore to Default")
        restore_btn.setStyleSheet(self.get_button_style("#6c757d"))
        restore_btn.clicked.connect(self.restore_defaults)
        button_layout.addWidget(restore_btn)

        button_layout.addStretch()

        # Cancel and OK buttons (right side)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedWidth(80)
        cancel_btn.setStyleSheet(self.get_button_style("#6c757d"))
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        ok_btn = QPushButton("OK")
        ok_btn.setFixedWidth(80)
        ok_btn.setStyleSheet(self.get_button_style("#0d6efd"))
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)

        frame_layout.addWidget(button_bar)

        main_layout.addWidget(content_frame)

    def get_button_style(self, color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 6px 16px;
                border-radius: 4px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {self.adjust_color(color, -20)};
            }}
            QPushButton:pressed {{
                background-color: {self.adjust_color(color, -40)};
            }}
        """

    def adjust_color(self, hex_color, amount):
        """Darken or lighten a hex color"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = tuple(max(0, min(255, c + amount)) for c in rgb)
        return f"#{new_rgb[0]:02x}{new_rgb[1]:02x}{new_rgb[2]:02x}"

    def browse_folder(self):
        """Open folder browser dialog"""
        current_path = self.widgets['persistent_output_folder'].currentText()
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder",
            current_path,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if folder:
            self.widgets['persistent_output_folder'].setCurrentText(folder)

    def load_settings(self):
        """Load current settings (from defaults initially)"""
        self.widgets['reload_previous_model'].setChecked(self.defaults['reload_previous_model'])
        self.widgets['default_graphic_card'].setCurrentText(self.defaults['default_graphic_card'])
        self.widgets['persistent_output_folder'].setCurrentText(self.defaults['persistent_output_folder'])
        self.widgets['always_show_log_panel'].setChecked(self.defaults['always_show_log_panel'])
        self.widgets['dev_mode'].setChecked(self.defaults['dev_mode'])

    def restore_defaults(self):
        """Restore all settings to default values"""
        self.load_settings()

    def get_settings(self):
        """Get current settings as dictionary"""
        return {
            'reload_previous_model': self.widgets['reload_previous_model'].isChecked(),
            'default_graphic_card': self.widgets['default_graphic_card'].currentText(),
            'persistent_output_folder': self.widgets['persistent_output_folder'].currentText(),
            'always_show_log_panel': self.widgets['always_show_log_panel'].isChecked(),
            'dev_mode': self.widgets['dev_mode'].isChecked()
        }

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and not self.drag_position.isNull():
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def showEvent(self, event):
        super().showEvent(event)
        if self.parent():
            # Calculate maximum height (parent height - 50px)
            parent_height = self.parent().height()
            max_height = parent_height - 50

            # Set a reasonable width
            self.setFixedWidth(500)

            # Set maximum height
            if self.sizeHint().height() > max_height:
                self.setFixedHeight(max_height)
            else:
                self.setFixedHeight(min(self.sizeHint().height(), max_height))

            # Center in parent
            parent_rect = self.parent().geometry()
            dialog_rect = self.geometry()
            center_x = parent_rect.x() + (parent_rect.width() - dialog_rect.width()) // 2
            center_y = parent_rect.y() + (parent_rect.height() - dialog_rect.height()) // 2
            self.move(center_x, center_y)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        central = QWidget()
        layout = QVBoxLayout(central)

        label = QLabel("Click the button to open settings dialog")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        btn = QPushButton("Open Settings")
        btn.setFixedSize(150, 40)
        btn.clicked.connect(self.open_settings)
        layout.addWidget(btn, alignment=Qt.AlignCenter)

        self.setCentralWidget(central)

    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.Accepted:
            settings = dialog.get_settings()
            print("Settings saved:", settings)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
