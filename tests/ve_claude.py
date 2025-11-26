#!/usr/bin/env python3
"""
Single-file PySide6 Video Editor Button Demo
DaVinci Resolve-inspired dark theme with minimal color usage
"""

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QButtonGroup, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPalette, QColor
import sys


class VideoEditorButtons(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Editor Buttons - DaVinci Style")
        self.setMinimumSize(900, 700)

        # Set dark theme
        self.setup_dark_theme()

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(30)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel("Video Editor Button System")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)

        # Flat Icon Buttons
        layout.addWidget(self.create_section_label("Flat Icon Buttons (Toggleable)"))
        layout.addWidget(self.create_flat_icon_buttons())

        # Flat Text Buttons
        layout.addWidget(self.create_section_label("Flat Text Buttons (Toggleable)"))
        layout.addWidget(self.create_flat_text_buttons())

        # Flat Text+Icon Buttons
        layout.addWidget(self.create_section_label("Flat Text + Icon Buttons (Toggleable)"))
        layout.addWidget(self.create_flat_text_icon_buttons())

        # Strong Buttons
        layout.addWidget(self.create_section_label("Strong Action Buttons (Filled)"))
        layout.addWidget(self.create_strong_buttons())

        # Button Groups
        layout.addWidget(self.create_section_label("Toggle Groups (Radio Behavior)"))
        layout.addWidget(self.create_button_groups())

        layout.addStretch()

    def setup_dark_theme(self):
        """DaVinci-inspired dark theme"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(200, 200, 200))
        palette.setColor(QPalette.Base, QColor(40, 40, 40))
        palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
        palette.setColor(QPalette.Text, QColor(200, 200, 200))
        palette.setColor(QPalette.Button, QColor(50, 50, 50))
        palette.setColor(QPalette.ButtonText, QColor(200, 200, 200))
        self.setPalette(palette)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #c8c8c8;
            }
        """)

    def create_section_label(self, text):
        """Create a section header label"""
        label = QLabel(text)
        label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #909090;
            padding: 8px 0px;
        """)
        return label

    def create_flat_icon_buttons(self):
        """Flat icon buttons with toggle capability"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)

        icons = ["▶", "⏸", "⏹", "✂", "📋", "↶", "↷"]
        tooltips = ["Play", "Pause", "Stop", "Cut", "Copy", "Undo", "Redo"]

        for icon, tooltip in zip(icons, tooltips):
            btn = QPushButton(icon)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            btn.setFixedSize(36, 36)
            btn.setStyleSheet(self.flat_icon_button_style())
            layout.addWidget(btn)

        layout.addStretch()
        return container

    def create_flat_text_buttons(self):
        """Flat text buttons with toggle capability"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)

        buttons = ["Select", "Trim", "Ripple", "Roll", "Slip"]

        for text in buttons:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setStyleSheet(self.flat_text_button_style())
            layout.addWidget(btn)

        layout.addStretch()
        return container

    def create_flat_text_icon_buttons(self):
        """Flat text+icon buttons with toggle capability"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)

        buttons = [
            ("📁 Open", "Open Project"),
            ("💾 Save", "Save Project"),
            ("📤 Export", "Export Video"),
            ("⚙ Settings", "Settings")
        ]

        for text, tooltip in buttons:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            btn.setStyleSheet(self.flat_text_button_style())
            layout.addWidget(btn)

        layout.addStretch()
        return container

    def create_strong_buttons(self):
        """Strong action buttons (filled) - these are NOT toggleable"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        # Primary strong button (most important)
        render_btn = QPushButton("⚡ Start Rendering")
        render_btn.setStyleSheet(self.strong_button_style("#4a9eff"))
        render_btn.setMinimumHeight(40)
        render_btn.clicked.connect(lambda: print("Rendering started!"))
        layout.addWidget(render_btn)

        # Success strong button
        export_btn = QPushButton("✓ Export Complete")
        export_btn.setStyleSheet(self.strong_button_style("#4caf50"))
        export_btn.setMinimumHeight(40)
        layout.addWidget(export_btn)

        # Error strong button
        error_btn = QPushButton("⚠ Error Occurred")
        error_btn.setStyleSheet(self.strong_button_style("#ef4444"))
        error_btn.setMinimumHeight(40)
        layout.addWidget(error_btn)

        layout.addStretch()
        return container

    def create_button_groups(self):
        """Demonstrate button groups with radio behavior"""
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Tool selection group
        tool_label = QLabel("Tool Selection:")
        tool_label.setStyleSheet("color: #909090; font-size: 12px;")
        main_layout.addWidget(tool_label)

        tool_container = QWidget()
        tool_container.setStyleSheet("""
            QWidget {
                background-color: #2a2a2a;
                border-radius: 6px;
            }
        """)
        tool_layout = QHBoxLayout(tool_container)
        tool_layout.setSpacing(4)
        tool_layout.setContentsMargins(4, 4, 4, 4)

        tool_group = QButtonGroup(self)
        tool_group.setExclusive(True)

        tools = ["Select", "✂ Cut", "Trim", "Split", "Razor"]
        for i, text in enumerate(tools):
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setStyleSheet(self.button_group_style())
            btn.setMinimumHeight(32)
            tool_layout.addWidget(btn)
            tool_group.addButton(btn)
            if i == 0:
                btn.setChecked(True)

        tool_layout.addStretch()
        main_layout.addWidget(tool_container)

        # View mode group
        view_label = QLabel("View Mode:")
        view_label.setStyleSheet("color: #909090; font-size: 12px;")
        main_layout.addWidget(view_label)

        view_container = QWidget()
        view_container.setStyleSheet("""
            QWidget {
                background-color: #2a2a2a;
                border-radius: 6px;
            }
        """)
        view_layout = QHBoxLayout(view_container)
        view_layout.setSpacing(4)
        view_layout.setContentsMargins(4, 4, 4, 4)

        view_group = QButtonGroup(self)
        view_group.setExclusive(True)

        views = ["☰ Timeline", "▦ Grid", "📋 List", "🎬 Storyboard"]
        for i, text in enumerate(views):
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setStyleSheet(self.button_group_style())
            btn.setMinimumHeight(32)
            view_layout.addWidget(btn)
            view_group.addButton(btn)
            if i == 0:
                btn.setChecked(True)

        view_layout.addStretch()
        main_layout.addWidget(view_container)

        return container

    def flat_icon_button_style(self):
        """Style for flat icon buttons"""
        return """
            QPushButton {
                background-color: transparent;
                border: none;
                color: #909090;
                font-size: 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                color: #c8c8c8;
            }
            QPushButton:checked {
                background-color: #4a4a4a;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #505050;
            }
        """

    def flat_text_button_style(self):
        """Style for flat text buttons"""
        return """
            QPushButton {
                background-color: transparent;
                border: none;
                color: #909090;
                font-size: 13px;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                color: #c8c8c8;
            }
            QPushButton:checked {
                background-color: #4a4a4a;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #505050;
            }
        """

    def button_group_style(self):
        """Style for buttons within a group (radio behavior)"""
        return """
            QPushButton {
                background-color: transparent;
                border: none;
                color: #707070;
                font-size: 13px;
                padding: 6px 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                color: #a0a0a0;
            }
            QPushButton:checked {
                background-color: #404040;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #454545;
            }
        """

    def strong_button_style(self, color):
        """Style for strong action buttons"""
        hover_color = self.adjust_color_brightness(color, 1.15)
        return f"""
            QPushButton {{
                background-color: {color};
                border: none;
                color: #ffffff;
                font-size: 14px;
                font-weight: 600;
                padding: 10px 24px;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {color};
            }}
        """

    def adjust_color_brightness(self, hex_color, factor):
        """Adjust color brightness for hover effects"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return f"#{r:02x}{g:02x}{b:02x}"


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = VideoEditorButtons()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
