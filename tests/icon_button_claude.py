import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QColor
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QPixmap, QPainter

class IconButton(QPushButton):
    """Material M3 Icon Button without animation"""

    def __init__(self, icon_path: str, size: int = 48, parent=None):
        super().__init__(parent)
        self.size = size
        self.setIconSize(QSize(size - 16, size - 16))
        self.setFixedSize(QSize(size, size))

        # Load SVG icon
        if icon_path.endswith('.svg'):
            pixmap = self._load_svg(icon_path, size - 16)
        else:
            pixmap = QPixmap(icon_path)

        self.setIcon(QIcon(pixmap))
        self.setFlat(False)
        self.setCursor(Qt.PointingHandCursor)
        self._setup_stylesheet()

    def _load_svg(self, path: str, size: int) -> QPixmap:
        """Load and render SVG icon"""
        renderer = QSvgRenderer(path)
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return pixmap

    def _setup_stylesheet(self):
        """Apply Material M3 styling without animation"""
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #e8eaf6;
                border: none;
                border-radius: {self.size // 2}px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: #d6d9f0;
            }}
            QPushButton:pressed {{
                background-color: #c5c9e6;
            }}
        """)


class FilledIconButton(IconButton):
    """Material M3 Filled Icon Button"""

    def _setup_stylesheet(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #3f51b5;
                border: none;
                border-radius: {self.size // 2}px;
                padding: 8px;
                color: white;
            }}
            QPushButton:hover {{
                background-color: #3949a3;
            }}
            QPushButton:pressed {{
                background-color: #303f9f;
            }}
        """)


class TonalIconButton(IconButton):
    """Material M3 Tonal Icon Button"""

    def _setup_stylesheet(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #e8eaf6;
                border: none;
                border-radius: {self.size // 2}px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: #d1d5eb;
            }}
            QPushButton:pressed {{
                background-color: #c5cae0;
            }}
        """)


class OutlinedIconButton(IconButton):
    """Material M3 Outlined Icon Button"""

    def _setup_stylesheet(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid #79747e;
                border-radius: {self.size // 2}px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: #f5f5f5;
            }}
            QPushButton:pressed {{
                background-color: #efefef;
            }}
        """)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Material M3 Icon Buttons")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a simple SVG for demonstration
        svg_content = """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"/>
        </svg>
        """

        with open('/tmp/test_icon.svg', 'w') as f:
            f.write(svg_content)

        # Standard Icon Buttons
        row1 = QHBoxLayout()
        row1.addWidget(IconButton('/tmp/test_icon.svg', 48))
        row1.addWidget(IconButton('/tmp/test_icon.svg', 40))
        row1.addWidget(IconButton('/tmp/test_icon.svg', 32))
        layout.addLayout(row1)

        # Filled Icon Buttons
        row2 = QHBoxLayout()
        row2.addWidget(FilledIconButton('/tmp/test_icon.svg', 48))
        row2.addWidget(FilledIconButton('/tmp/test_icon.svg', 40))
        row2.addWidget(FilledIconButton('/tmp/test_icon.svg', 32))
        layout.addLayout(row2)

        # Tonal Icon Buttons
        row3 = QHBoxLayout()
        row3.addWidget(TonalIconButton('/tmp/test_icon.svg', 48))
        row3.addWidget(TonalIconButton('/tmp/test_icon.svg', 40))
        row3.addWidget(TonalIconButton('/tmp/test_icon.svg', 32))
        layout.addLayout(row3)

        # Outlined Icon Buttons
        row4 = QHBoxLayout()
        row4.addWidget(OutlinedIconButton('/tmp/test_icon.svg', 48))
        row4.addWidget(OutlinedIconButton('/tmp/test_icon.svg', 40))
        row4.addWidget(OutlinedIconButton('/tmp/test_icon.svg', 32))
        layout.addLayout(row4)

        layout.addStretch()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
