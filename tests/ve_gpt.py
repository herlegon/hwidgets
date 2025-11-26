from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QButtonGroup, QLabel
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt
import sys

# ------------------------------
# Theme / Colors
# ------------------------------

PRIMARY_ACCENT = "#5545bd"

DARK_THEME = {
    "background": "#212121",         # Keep the main background
    "text": "#EEEEEE",               # General text
    "flat_normal": "#BBBBBB",        # Unselected flat buttons brighter
    "flat_hover": "#FFFFFF",         # Hovered flat buttons
    "flat_pressed": "#AAAAAA",       # Pressed flat buttons
    "flat_selected": PRIMARY_ACCENT, # Selected flat button
    "strong_bg": PRIMARY_ACCENT,     # Filled action button
    "strong_bg_hover": "#9999FF",    # Hover on strong button
    "strong_bg_pressed": "#6666DD",  # Pressed strong button
    "strong_text": "#FFFFFF"         # Strong button text
}


# ------------------------------
# Base button class
# ------------------------------

class BaseButton(QPushButton):
    def __init__(self, text="", icon=None, toggleable=False, parent=None):
        super().__init__(text, parent)
        self.setCheckable(toggleable)
        if icon:
            self.setIcon(icon)
            self.setIconSize(QSize(20, 20))
        self.setCursor(Qt.PointingHandCursor)
        self.update_style()
        self.toggled.connect(self.update_style)

    def update_style(self):
        pass  # implemented in subclasses

# ------------------------------
# Flat buttons
# ------------------------------

class FlatButton(BaseButton):
    def update_style(self):
        t = DARK_THEME
        bg = "transparent"
        color = t["flat_normal"]

        if self.isCheckable() and self.isChecked():
            color = "#FFFFFF"  # full contrast
            bg = "#4b3da8"     # subtle dark blue background

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                border: none;
                color: {color};
                padding: 4px 8px;
                font-size: 14px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                color: #CCCCCC;
            }}
            QPushButton:pressed {{
                color: #CCCCCC;
            }}
        """)


class IconButton(FlatButton):
    def __init__(self, icon, toggleable=False, parent=None):
        super().__init__("", icon=icon, toggleable=toggleable, parent=parent)

class TextButton(FlatButton):
    pass

class TextIconButton(FlatButton):
    def __init__(self, text, icon, toggleable=False, parent=None):
        super().__init__(text=text, icon=icon, toggleable=toggleable, parent=parent)

# ------------------------------
# Strong button (filled)
# ------------------------------

class StrongButton(BaseButton):
    def update_style(self):
        t = DARK_THEME
        bg = t["strong_bg_hover"] if self.underMouse() else t["strong_bg"]
        if self.isDown():
            bg = t["strong_bg_pressed"]

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {t['strong_text']};
                border: none;
                border-radius: 4px;
                padding: 6px 16px;
                font-weight: 600;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {t['strong_bg_hover']};
            }}
            QPushButton:pressed {{
                background-color: {t['strong_bg_pressed']};
            }}
        """)

# ------------------------------
# Demo window
# ------------------------------

class DemoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Editor Buttons Demo")
        self.setStyleSheet(f"background-color: {DARK_THEME['background']}; color: {DARK_THEME['text']}")
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Flat Icon Buttons
        layout.addWidget(QLabel("Flat Icon Buttons (toggleable)"))
        icon_row = QHBoxLayout()
        layout.addLayout(icon_row)
        icon1 = IconButton(QIcon.fromTheme("media-playback-start"))
        icon2 = IconButton(QIcon.fromTheme("media-playback-stop"), toggleable=True)
        icon_row.addWidget(icon1)
        icon_row.addWidget(icon2)

        # Flat Text Buttons
        layout.addWidget(QLabel("Flat Text Buttons (toggleable)"))
        text_row = QHBoxLayout()
        layout.addLayout(text_row)
        t1 = TextButton("Snap", toggleable=True)
        t2 = TextButton("Loop", toggleable=True)
        text_row.addWidget(t1)
        text_row.addWidget(t2)

        # Flat Text + Icon Buttons
        layout.addWidget(QLabel("Flat Text+Icon Buttons (toggleable)"))
        ti_row = QHBoxLayout()
        layout.addLayout(ti_row)
        ti1 = TextIconButton("Cut", QIcon.fromTheme("edit-cut"), toggleable=True)
        ti2 = TextIconButton("Copy", QIcon.fromTheme("edit-copy"), toggleable=True)
        ti_row.addWidget(ti1)
        ti_row.addWidget(ti2)

        # Strong Button
        layout.addWidget(QLabel("Strong Action Button"))
        strong_row = QHBoxLayout()
        layout.addLayout(strong_row)
        strong_btn = StrongButton("Start Processing")
        strong_row.addWidget(strong_btn)

        # Toggle Button Group
        layout.addWidget(QLabel("Toggle Button Group (one selected)"))
        group_row = QHBoxLayout()
        layout.addLayout(group_row)
        self.group = QButtonGroup(self)
        b1 = TextButton("Video", toggleable=True)
        b2 = TextButton("Audio", toggleable=True)
        b3 = TextButton("Effects", toggleable=True)
        self.group.setExclusive(True)
        for b in (b1,b2,b3):
            self.group.addButton(b)
            group_row.addWidget(b)

# ------------------------------
# Run
# ------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())
