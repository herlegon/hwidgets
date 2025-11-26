import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize

# =========================================================
#  MATERIAL 3 THEME SYSTEM
# =========================================================

class M3Theme:
    def __init__(self, primary, on_primary, surface, on_surface, outline):
        self.primary = primary
        self.on_primary = on_primary
        self.surface = surface
        self.on_surface = on_surface
        self.outline = outline


LIGHT_THEME = M3Theme(
    primary="rgba(33,150,243,1.0)",
    on_primary="white",
    surface="white",
    on_surface="black",
    outline="rgba(0,0,0,0.22)"
)

LIGHT_THEME.surface_container = "rgba(240,240,240,1.0)"
LIGHT_THEME.surface_container_hover = "rgba(230,230,230,1.0)"
LIGHT_THEME.surface_container_pressed = "rgba(220,220,220,1.0)"

DARK_THEME = M3Theme(
    primary="rgba(33,150,243,1.0)",
    on_primary="black",
    surface="rgba(24,24,24,1.0)",
    on_surface="white",
    outline="rgba(255,255,255,0.25)"
)

DARK_THEME.surface_container = "rgba(40,40,40,1.0)"
DARK_THEME.surface_container_hover = "rgba(50,50,50,1.0)"
DARK_THEME.surface_container_pressed = "rgba(60,60,60,1.0)"



CURRENT_THEME = DARK_THEME  # start in light mode


# =========================================================
#  BASE M3 BUTTON
# =========================================================

class M3Button(QPushButton):
    """
    Base class for Material 3 buttons.
    Subclasses override build_base_colors() for colors.
    """

    def __init__(self, text="", icon: QIcon = None, toggleable=False, parent=None):
        super().__init__(text, parent)
        self.setCheckable(toggleable)

        if icon:
            self.setIcon(icon)
            self.setIconSize(QSize(18, 18))

        self.update_stylesheet()
        self.toggled.connect(self.update_stylesheet)

    def build_base_colors(self):
        raise NotImplementedError

    def update_stylesheet(self):
        c = self.build_base_colors()
        checked_bg = c["checked"] if self.isChecked() else c["base"]

        self.setStyleSheet(f"""
            QPushButton {{
                border: none;
                border-radius: 8px;
                padding: 6px 16px;
                background-color: {checked_bg};
                color: {c["text"]};
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {c["hover"]};
            }}
            QPushButton:pressed {{
                background-color: {c["pressed"]};
            }}
            QPushButton:disabled {{
                background-color: rgba(255,255,255,0.08);
                color: rgba(255,255,255,0.30);
            }}
        """)


# =========================================================
#  BUTTON VARIANTS
# =========================================================

class M3FilledButton(M3Button):
    def build_base_colors(self):
        t = CURRENT_THEME

        # Normal (non-toggle) filled button
        if not self.isCheckable():
            return {
                "base":    t.primary,
                "hover":   "rgba(33,150,243,0.92)",
                "pressed": "rgba(33,150,243,0.80)",
                "checked": t.primary,
                "text":    t.on_primary,
                "text_checked": t.on_primary,
            }

        # Toggleable filled button (SPEC-CORRECT)
        if self.isChecked():
            # SELECTED → primary container
            return {
                "base":    t.primary,
                "hover":   "rgba(33,150,243,0.92)",
                "pressed": "rgba(33,150,243,0.80)",
                "checked": t.primary,
                "text":    t.on_primary,
                "text_checked": t.on_primary,
            }
        else:
            # UNSELECTED → surface-container (neutral)
            return {
                "base":    t.surface_container,
                "hover":   t.surface_container_hover,
                "pressed": t.surface_container_pressed,
                "checked": t.primary,          # will be applied when checked
                "text":    t.on_surface,
                "text_checked": t.on_primary,
            }



class M3TonalButton(M3Button):
    def build_base_colors(self):
        t = CURRENT_THEME
        return {
            "base":    "rgba(33,150,243,0.18)" if t == DARK_THEME else "rgba(33,150,243,0.20)",
            "hover":   "rgba(33,150,243,0.30)",
            "pressed": "rgba(33,150,243,0.40)",
            "checked": "rgba(33,150,243,0.35)",
            "text":    t.on_surface
        }


class M3OutlinedButton(M3Button):
    def update_stylesheet(self):
        c = self.build_base_colors()
        checked_bg = c["checked"] if self.isChecked() else c["base"]

        self.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid {c["outline"]};
                border-radius: 8px;
                padding: 6px 16px;
                background-color: {checked_bg};
                color: {c["text"]};
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{ background-color: {c["hover"]}; }}
            QPushButton:pressed {{ background-color: {c["pressed"]}; }}
        """)

    def build_base_colors(self):
        t = CURRENT_THEME
        return {
            "base":    "transparent",
            "hover":   "rgba(255,255,255,0.06)" if t == DARK_THEME else "rgba(33,150,243,0.08)",
            "pressed": "rgba(255,255,255,0.12)" if t == DARK_THEME else "rgba(33,150,243,0.18)",
            "checked": "rgba(33,150,243,0.20)",
            "text":    t.primary,
            "outline": t.outline
        }


class M3TextButton(M3Button):
    def build_base_colors(self):
        t = CURRENT_THEME
        return {
            "base":    "transparent",
            "hover":   "rgba(255,255,255,0.06)" if t == DARK_THEME else "rgba(33,150,243,0.08)",
            "pressed": "rgba(255,255,255,0.12)" if t == DARK_THEME else "rgba(33,150,243,0.18)",
            "checked": "rgba(33,150,243,0.15)",
            "text":    t.primary
        }


class M3IconButton(M3Button):
    def __init__(self, icon, toggleable=False, parent=None):
        super().__init__("", icon, toggleable, parent)
        self.setFixedSize(40, 40)

    def build_base_colors(self):
        t = CURRENT_THEME
        return {
            "base":    "transparent",
            "hover":   "rgba(255,255,255,0.06)" if t == DARK_THEME else "rgba(33,150,243,0.08)",
            "pressed": "rgba(255,255,255,0.12)" if t == DARK_THEME else "rgba(33,150,243,0.18)",
            "checked": "rgba(33,150,243,0.25)",
            "text":    t.on_surface
        }


class M3IconTextButton(M3Button):
    def __init__(self, text, icon, toggleable=False, parent=None):
        super().__init__(text, icon, toggleable, parent)
        self.setIconSize(QSize(18, 18))

    def build_base_colors(self):
        t = CURRENT_THEME
        return {
            "base":    "rgba(33,150,243,0.20)" if t == LIGHT_THEME else "rgba(33,150,243,0.18)",
            "hover":   "rgba(33,150,243,0.30)",
            "pressed": "rgba(33,150,243,0.40)",
            "checked": "rgba(33,150,243,0.35)",
            "text":    t.on_surface
        }


# =========================================================
#  DEMO WINDOW
# =========================================================

class DemoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Material 3 Buttons (Light/Dark Mode)")

        self.main = QVBoxLayout(self)

        # Dark mode toggle
        self.dark_toggle = M3FilledButton("Dark Mode", toggleable=True)
        self.dark_toggle.toggled.connect(self.switch_theme)
        self.main.addWidget(self.dark_toggle)

        self.container = QVBoxLayout()
        self.main.addLayout(self.container)

        self.build_buttons()

    def build_buttons(self):
        # clear old
        while self.container.count():
            item = self.container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # icon fallback (blue square)
        pix = QPixmap(64, 64)
        pix.fill("#2196F3")
        icon = QIcon(pix)

        def section(title):
            label = QLabel(title)
            label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 16px;")
            self.container.addWidget(label)

        # Filled
        section("Filled Buttons")
        row = QHBoxLayout()
        row.addWidget(M3FilledButton("Normal"))
        row.addWidget(M3FilledButton("Toggle", toggleable=True))
        self.container.addLayout(row)

        # Tonal
        section("Tonal Buttons")
        row = QHBoxLayout()
        row.addWidget(M3TonalButton("Normal"))
        row.addWidget(M3TonalButton("Toggle", toggleable=True))
        self.container.addLayout(row)

        # Outlined
        section("Outlined Buttons")
        row = QHBoxLayout()
        row.addWidget(M3OutlinedButton("Normal"))
        row.addWidget(M3OutlinedButton("Toggle", toggleable=True))
        self.container.addLayout(row)

        # Text
        section("Text Buttons")
        row = QHBoxLayout()
        row.addWidget(M3TextButton("Normal"))
        row.addWidget(M3TextButton("Toggle", toggleable=True))
        self.container.addLayout(row)

        # Icon
        section("Icon Buttons")
        row = QHBoxLayout()
        row.addWidget(M3IconButton(icon))
        row.addWidget(M3IconButton(icon, toggleable=True))
        self.container.addLayout(row)

        # Icon + Text
        section("Icon + Text Buttons")
        row = QHBoxLayout()
        row.addWidget(M3IconTextButton("Normal", icon))
        row.addWidget(M3IconTextButton("Toggle", icon, toggleable=True))
        self.container.addLayout(row)

    def switch_theme(self, dark):
        global CURRENT_THEME
        CURRENT_THEME = DARK_THEME if dark else LIGHT_THEME

        # Apply dark or light background to the WINDOW
        if dark:
            self.setStyleSheet("background-color: rgb(30,30,30); color: white;")
        else:
            self.setStyleSheet("background-color: white; color: black;")

        # Rebuild all buttons so they get new theme colors
        self.build_buttons()



# =========================================================
#  MAIN
# =========================================================

def main():
    app = QApplication(sys.argv)
    win = DemoApp()
    win.resize(500, 800)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
