import sys
from PySide6.QtWidgets import QApplication, QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon, QPixmap, QColor, QFont
from PySide6.QtCore import Qt, Signal, QSize


class M3Chip(QPushButton):
    """Material Design 3 Chip widget with optional leading icon"""

    removed = Signal()

    def __init__(self, text="Chip", icon=None, removable=False, parent=None):
        super().__init__(text, parent)
        self.removable = removable
        self.is_hovered = False

        self.setMinimumHeight(32)
        self.setMaximumHeight(32)
        self.setCursor(Qt.PointingHandCursor)

        # Set icon if provided
        if icon:
            if isinstance(icon, str):
                self.setIcon(QIcon(icon))
            else:
                self.setIcon(icon)
            self.setIconSize(QSize(18, 18))

        self._apply_stylesheet()

        self.enterEvent = self._on_enter
        self.leaveEvent = self._on_leave

    def _apply_stylesheet(self):
        """Apply Material Design 3 styling"""
        padding = "8px 12px" if not self.removable else "8px 4px 8px 12px"

        base_style = f"""
            QPushButton {{
                background-color: #e7e0ec;
                color: #1d192b;
                border: 1px solid #79747e;
                border-radius: 8px;
                padding: {padding};
                font-family: 'Roboto';
                font-size: 14px;
                font-weight: 500;
                outline: none;
                spacing: 8px;
            }}
            QPushButton:hover {{
                background-color: #ddd6e5;
            }}
            QPushButton:pressed {{
                background-color: #d0c7d8;
            }}
        """

        self.setStyleSheet(base_style)

    def _on_enter(self, event):
        """Handle mouse enter"""
        self.is_hovered = True

    def _on_leave(self, event):
        """Handle mouse leave"""
        self.is_hovered = False


class M3InputChip(QPushButton):
    """Material Design 3 Input Chip with optional leading icon"""

    removed = Signal()

    def __init__(self, text="Input Chip", icon=None, removable=True, parent=None):
        super().__init__(text, parent)
        self.removable = removable
        self.is_hovered = False

        self.setMinimumHeight(32)
        self.setMaximumHeight(32)
        self.setCursor(Qt.PointingHandCursor)

        # Set icon if provided
        if icon:
            if isinstance(icon, str):
                self.setIcon(QIcon(icon))
            else:
                self.setIcon(icon)
            self.setIconSize(QSize(18, 18))

        self._apply_stylesheet()

        self.enterEvent = self._on_enter
        self.leaveEvent = self._on_leave

    def _apply_stylesheet(self):
        """Apply Material Design 3 input chip styling"""
        padding = "6px 8px 6px 12px"

        style = f"""
            QPushButton {{
                background-color: #fffbfe;
                color: #1d192b;
                border: 1px solid #79747e;
                border-radius: 8px;
                padding: {padding};
                font-family: 'Roboto';
                font-size: 14px;
                font-weight: 500;
                outline: none;
                spacing: 8px;
            }}
            QPushButton:hover {{
                background-color: #faf8fc;
            }}
            QPushButton:pressed {{
                background-color: #f5f3f8;
            }}
        """

        self.setStyleSheet(style)

    def _on_enter(self, event):
        """Handle mouse enter"""
        self.is_hovered = True

    def _on_leave(self, event):
        """Handle mouse leave"""
        self.is_hovered = False


class M3FilterChip(QPushButton):
    """Material Design 3 Filter Chip with optional leading icon"""

    toggled = Signal(bool)

    def __init__(self, text="Filter", icon=None, parent=None):
        super().__init__(text, parent)
        self.is_selected = False
        self.icon_checked = None
        self.icon_unchecked = QIcon()  # Empty icon for unchecked state

        self.setCheckable(True)
        # self.setMinimumHeight(32)
        # self.setMaximumHeight(32)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.PointingHandCursor)

        # Set checked icon if provided
        if icon:
            if isinstance(icon, str):
                self.icon_checked = QIcon(icon)
            else:
                self.icon_checked = icon
            self.setIconSize(QSize(18, 18))

        self._apply_stylesheet()
        self.setFixedWidth(self.width() + 18)
        self.clicked.connect(self._on_toggled)
        # self.update()


    def _on_toggled(self):
        """Handle toggle"""
        self.is_selected = self.isChecked()

        # Show icon only when checked
        if self.is_selected and self.icon_checked:
            self.setIcon(self.icon_checked)
        # else:
        #     self.setIcon(self.icon_unchecked)

        self.toggled.emit(self.is_selected)

    def _apply_stylesheet(self):
        """Apply Material Design 3 filter chip styling"""
        if self.is_selected:
            bg_color = "#21005e"
            text_color = "#fffbfe"
            border_color = "#21005e"
        else:
            bg_color = "#fffbfe"
            text_color = "#1d192b"
            border_color = "#79747e"

        style = f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 8px;
                padding: 6px 12px;
                font-family: 'Roboto';
                font-size: 14px;
                font-weight: 500;
                outline: none;
                spacing: 8px;
            }}
            QPushButton:hover {{
                background-color: {bg_color};
                opacity: 0.9;
            }}
            QPushButton:pressed {{
                background-color: {bg_color};
                opacity: 0.8;
            }}
            QPushButton:checked {{
                background-color: {bg_color};
                opacity: 0.8;
                margin: 0px;
                opacity: 0.8;
            }}
        """

        self.setStyleSheet(style)


def create_icon(color, char="✓"):
    """Helper function to create a simple icon from a character"""
    pixmap = QPixmap(18, 18)
    pixmap.fill(Qt.transparent)

    from PySide6.QtGui import QPainter, QFont as QGUIFont
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    font = QGUIFont("Roboto", 10, QFont.Bold)
    painter.setFont(font)
    painter.setPen(QColor("red"))  # Changed to red for debugging
    painter.drawText(pixmap.rect(), Qt.AlignCenter, char)
    painter.end()

    return QIcon(pixmap)


class ChipDemo(QWidget):
    """Demo window showcasing M3 chips with leading icons"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Material Design 3 Chips - PySide6 (with Leading Icons)")
        self.setGeometry(100, 100, 900, 700)

        layout = QVBoxLayout()
        layout.setSpacing(24)
        layout.setContentsMargins(24, 24, 24, 24)

        # Create simple icons
        check_icon = create_icon(QColor("#1d192b"), "✓")
        star_icon = create_icon(QColor("#1d192b"), "★")
        heart_icon = create_icon(QColor("#1d192b"), "♥")
        tag_icon = create_icon(QColor("#1d192b"), "⊕")

        # Assist Chips
        assist_label = QLabel("Assist Chips")
        assist_label.setFont(QFont("Roboto", 16, QFont.Bold))
        layout.addWidget(assist_label)

        assist_layout = QHBoxLayout()
        assist_layout.addWidget(M3Chip("Assist 1", icon=check_icon))
        assist_layout.addWidget(M3Chip("Assist 2", icon=star_icon))
        assist_layout.addWidget(M3Chip("Assist 3", icon=heart_icon))
        assist_layout.addStretch()
        layout.addLayout(assist_layout)

        # Filter Chips
        filter_label = QLabel("Filter Chips")
        filter_label.setFont(QFont("Roboto", 16, QFont.Bold))
        layout.addWidget(filter_label)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(M3FilterChip("Filter 1", icon=check_icon))
        filter_layout.addWidget(M3FilterChip("Filter 2", icon=star_icon))
        filter_layout.addWidget(M3FilterChip("Filter 3", icon=heart_icon))
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # Input Chips
        input_label = QLabel("Input Chips")
        input_label.setFont(QFont("Roboto", 16, QFont.Bold))
        layout.addWidget(input_label)

        input_layout = QHBoxLayout()
        input_layout.addWidget(M3InputChip("Input 1", icon=tag_icon, removable=True))
        input_layout.addWidget(M3InputChip("Input 2", icon=check_icon, removable=True))
        input_layout.addWidget(M3InputChip("Input 3", icon=star_icon, removable=True))
        input_layout.addStretch()
        layout.addLayout(input_layout)

        # Suggestion Chips
        suggestion_label = QLabel("Suggestion Chips")
        suggestion_label.setFont(QFont("Roboto", 16, QFont.Bold))
        layout.addWidget(suggestion_label)

        suggestion_layout = QHBoxLayout()
        suggestion_layout.addWidget(M3Chip("Suggestion 1", icon=heart_icon))
        suggestion_layout.addWidget(M3Chip("Suggestion 2", icon=star_icon))
        suggestion_layout.addWidget(M3Chip("Suggestion 3", icon=check_icon))
        suggestion_layout.addStretch()
        layout.addLayout(suggestion_layout)

        # Chips without icons
        no_icon_label = QLabel("Chips Without Icons")
        no_icon_label.setFont(QFont("Roboto", 16, QFont.Bold))
        layout.addWidget(no_icon_label)

        no_icon_layout = QHBoxLayout()
        no_icon_layout.addWidget(M3Chip("Basic Chip"))
        no_icon_layout.addWidget(M3FilterChip("Filter"))
        no_icon_layout.addWidget(M3InputChip("Input"))
        no_icon_layout.addStretch()
        layout.addLayout(no_icon_layout)

        layout.addStretch()
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = ChipDemo()
    demo.show()
    sys.exit(app.exec())
