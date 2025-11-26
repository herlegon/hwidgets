import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                              QWidget, QPushButton, QLabel, QScrollArea)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer


class M3Button(QPushButton):
    """Base Material M3 Button"""
    SIZE = 32

    def __init__(self, text="", icon_path=None, parent=None):
        super().__init__(text, parent)
        self.icon_path = icon_path
        self.setCursor(Qt.PointingHandCursor)

        if icon_path:
            self.setIcon(QIcon(self._load_svg(icon_path, 18)))
            self.setIconSize(QSize(18, 18))

        self.setMinimumHeight(self.SIZE)
        self._setup_stylesheet()

    def _load_svg(self, path, size):
        renderer = QSvgRenderer(path)
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return pixmap

    def _setup_stylesheet(self):
        raise NotImplementedError


class HElevatedButton(M3Button):
    def _setup_stylesheet(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #262625;
                color: #f1f1f1;
                border: none;
                border-radius: 6px;
                padding: 8px 24px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #3a3939;
            }
            QPushButton:pressed {
                background-color: #4a4949;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #616161;
            }
            QPushButton:checked {
                background-color: #3d2d57;
            }
        """)


class HFilledButton(M3Button):
    def _setup_stylesheet(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #d0bcff;
                color: #21005e;
                border: none;
                border-radius: 6px;
                padding: 8px 24px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #cbb4f8;
            }
            QPushButton:pressed {
                background-color: #c1acf0;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #616161;
            }
            QPushButton:checked {
                background-color: #d0bcff;
            }
        """)


class HFilledTonalButton(M3Button):
    def _setup_stylesheet(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #4f378b;
                color: #f1f1f1;
                border: none;
                border-radius: 6px;
                padding: 8px 24px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #593f98;
            }
            QPushButton:pressed {
                background-color: #634aa5;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #616161;
            }
            QPushButton:checked {
                background-color: #593f98;
            }
        """)


class HOutlinedButton(M3Button):
    def _setup_stylesheet(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #d0bcff;
                border: 1px solid #8b7bb8;
                border-radius: 6px;
                padding: 8px 24px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
            }
            QPushButton:pressed {
                background-color: #3a3939;
            }
            QPushButton:disabled {
                background-color: transparent;
                color: #616161;
                border: 1px solid #525252;
            }
            QPushButton:checked {
                background-color: #3d2d57;
                border: 1px solid #d0bcff;
            }
        """)


class HTextButton(M3Button):
    def _setup_stylesheet(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #d0bcff;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
            }
            QPushButton:pressed {
                background-color: #3a3939;
            }
            QPushButton:disabled {
                background-color: transparent;
                color: #616161;
            }
            QPushButton:checked {
                background-color: #3d2d57;
            }
        """)


# Icon Buttons (32px total, 24px icon)

class M3IconButton(QPushButton):
    """Base Material M3 Icon Button"""
    SIZE = 32

    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self.setFixedSize(self.SIZE, self.SIZE)
        self.setIconSize(QSize(24, 24))
        self.setIcon(QIcon(self._load_svg(icon_path, 24)))
        self.setCursor(Qt.PointingHandCursor)
        self.setFlat(False)
        self._setup_stylesheet()

    def _load_svg(self, path, size):
        renderer = QSvgRenderer(path)
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return pixmap

    def _setup_stylesheet(self):
        raise NotImplementedError


class HStandardIconButton(M3IconButton):
    def _setup_stylesheet(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #e8def8;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
            }
            QPushButton:pressed {
                background-color: #3a3939;
            }
            QPushButton:disabled {
                background-color: transparent;
                color: #616161;
            }
            QPushButton:checked {
                background-color: #3d2d57;
            }
        """)


class HFilledIconButton(M3IconButton):
    def _setup_stylesheet(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #d0bcff;
                color: #21005e;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #cbb4f8;
            }
            QPushButton:pressed {
                background-color: #c1acf0;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #616161;
            }
            QPushButton:checked {
                background-color: #d0bcff;
            }
        """)


class HFilledTonalIconButton(M3IconButton):
    def _setup_stylesheet(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #4f378b;
                color: #f1f1f1;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #593f98;
            }
            QPushButton:pressed {
                background-color: #634aa5;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #616161;
            }
            QPushButton:checked {
                background-color: #593f98;
            }
        """)


class HOutlinedIconButton(M3IconButton):
    def _setup_stylesheet(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #e8def8;
                border: 1px solid #8b7bb8;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
            }
            QPushButton:pressed {
                background-color: #3a3939;
            }
            QPushButton:disabled {
                background-color: transparent;
                color: #616161;
                border: 1px solid #525252;
            }
            QPushButton:checked {
                background-color: #3d2d57;
                border: 1px solid #d0bcff;
            }
        """)


def create_demo_icon():
    """Create a simple SVG icon for demo"""
    svg = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"/>
    </svg>
    """
    with open('/tmp/m3_demo_icon.svg', 'w') as f:
        f.write(svg)
    return '/tmp/m3_demo_icon.svg'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Material M3 Buttons - All States (32px)")
        self.setGeometry(100, 100, 1200, 800)

        icon_path = create_demo_icon()

        scroll = QScrollArea()
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Dark theme for window and scroll area
        dark_stylesheet = """
            QMainWindow { background-color: #1c1b1f; }
            QWidget { background-color: #1c1b1f; color: #f1f1f1; }
            QLabel { color: #f1f1f1; }
            QScrollArea { background-color: #1c1b1f; }
        """
        self.setStyleSheet(dark_stylesheet)
        scroll.setStyleSheet(dark_stylesheet)

        # TEXT BUTTONS
        layout.addWidget(QLabel("TEXT BUTTONS"))

        # Elevated
        layout.addWidget(QLabel("Elevated"))
        row = QHBoxLayout()
        row.addWidget(self._state_group(HElevatedButton, "Elevated", icon_path))
        layout.addLayout(row)

        # Filled
        layout.addWidget(QLabel("Filled"))
        row = QHBoxLayout()
        row.addWidget(self._state_group(HFilledButton, "Filled", icon_path))
        layout.addLayout(row)

        # Filled Tonal
        layout.addWidget(QLabel("Filled Tonal"))
        row = QHBoxLayout()
        row.addWidget(self._state_group(HFilledTonalButton, "Tonal", icon_path))
        layout.addLayout(row)

        # Outlined
        layout.addWidget(QLabel("Outlined"))
        row = QHBoxLayout()
        row.addWidget(self._state_group(HOutlinedButton, "Outlined", icon_path))
        layout.addLayout(row)

        # Text
        layout.addWidget(QLabel("Text"))
        row = QHBoxLayout()
        row.addWidget(self._state_group(HTextButton, "Text", icon_path))
        layout.addLayout(row)

        # ICON BUTTONS
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel("ICON BUTTONS"))

        # Standard
        layout.addWidget(QLabel("Standard"))
        row = QHBoxLayout()
        row.addWidget(self._icon_state_group(HStandardIconButton, "Standard", icon_path))
        layout.addLayout(row)

        # Filled
        layout.addWidget(QLabel("Filled"))
        row = QHBoxLayout()
        row.addWidget(self._icon_state_group(HFilledIconButton, "Filled", icon_path))
        layout.addLayout(row)

        # Filled Tonal
        layout.addWidget(QLabel("Filled Tonal"))
        row = QHBoxLayout()
        row.addWidget(self._icon_state_group(HFilledTonalIconButton, "Tonal", icon_path))
        layout.addLayout(row)

        # Outlined
        layout.addWidget(QLabel("Outlined"))
        row = QHBoxLayout()
        row.addWidget(self._icon_state_group(HOutlinedIconButton, "Outlined", icon_path))
        layout.addLayout(row)

        layout.addStretch()

        scroll.setWidget(container)
        self.setCentralWidget(scroll)

    def _state_group(self, btn_class, label, icon_path):
        """Create a group showing: Normal, Toggled, Disabled, Disabled+Toggled"""
        group = QWidget()
        layout = QHBoxLayout(group)
        layout.setSpacing(10)

        # Normal
        btn1 = btn_class("Normal")
        layout.addWidget(btn1)

        # Toggled
        btn2 = btn_class("Toggled")
        btn2.setCheckable(True)
        btn2.setChecked(True)
        layout.addWidget(btn2)

        # Disabled
        btn3 = btn_class("Disabled")
        btn3.setEnabled(False)
        layout.addWidget(btn3)

        # Disabled + Toggled
        btn4 = btn_class("Dis+Tog")
        btn4.setCheckable(True)
        btn4.setChecked(True)
        btn4.setEnabled(False)
        layout.addWidget(btn4)

        return group

    def _icon_state_group(self, btn_class, label, icon_path):
        """Create a group of icon buttons showing different states"""
        group = QWidget()
        layout = QHBoxLayout(group)
        layout.setSpacing(10)

        # Normal
        btn1 = btn_class(icon_path)
        layout.addWidget(btn1)

        # Toggled
        btn2 = btn_class(icon_path)
        btn2.setCheckable(True)
        btn2.setChecked(True)
        layout.addWidget(btn2)

        # Disabled
        btn3 = btn_class(icon_path)
        btn3.setEnabled(False)
        layout.addWidget(btn3)

        # Disabled + Toggled
        btn4 = btn_class(icon_path)
        btn4.setCheckable(True)
        btn4.setChecked(True)
        btn4.setEnabled(False)
        layout.addWidget(btn4)

        return group


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
