#!/usr/bin/env python3
# settings_dialog_full.py
"""
Single-file runnable PySide6 example:
 - MainWindow with button to open SettingsDialog
 - SettingsDialog: frameless, draggable title bar, rounded corners,
   dark/light theme, fade animations, scroll area, footer (Restore / Cancel / OK)
 - All requested settings included
"""

import sys
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QEvent, Slot
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QScrollArea,
    QComboBox,
    QFileDialog,
    QSizePolicy,
    QFrame,
)


# -------------------------
# Tiny HSwitch toggle widget
# -------------------------
class HSwitch(QPushButton):
    def __init__(self, checked: bool = False, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setChecked(checked)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(56, 26)
        self.update_styles()
        self.toggled.connect(self.update_styles)

    def update_styles(self):
        if self.isChecked():
            # simple filled look for ON
            self.setStyleSheet(
                """
                HSwitch {
                    border-radius: 13px;
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #4caf50, stop:1 #2e7d32);
                }
                """
            )
        else:
            # simple gray for OFF
            self.setStyleSheet(
                """
                HSwitch {
                    border-radius: 13px;
                    background: #4a4a4a;
                }
                """
            )


# -------------------------
# SettingsDialog
# -------------------------
class SettingsDialog(QDialog):
    RADIUS = 12
    MARGIN_BOTTOM = 50
    ANIM_DURATION_MS = 200

    def __init__(self, parent=None, theme: str = "dark"):
        super().__init__(parent)

        # Frameless + translucent so we can paint rounded background
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)

        self.theme = theme.lower()
        self._title_bar_pressed = False
        self._mouse_offset = QPoint(0, 0)
        self._collected = None

        self.defaults = {
            "reload_previous": True,
            "default_gpu_index": 0,
            "output_folder": "",
            "always_show_log": False,
            "dev_mode": False,
        }

        self._create_ui()
        self.apply_theme(self.theme)

        # Fade animations
        self._show_anim = QPropertyAnimation(self, b"windowOpacity", self)
        self._show_anim.setDuration(self.ANIM_DURATION_MS)
        self._show_anim.setStartValue(0.0)
        self._show_anim.setEndValue(1.0)
        self._show_anim.setEasingCurve(QEasingCurve.InOutCubic)

        self._hide_anim = QPropertyAnimation(self, b"windowOpacity", self)
        self._hide_anim.setDuration(self.ANIM_DURATION_MS)
        self._hide_anim.setStartValue(1.0)
        self._hide_anim.setEndValue(0.0)
        self._hide_anim.setEasingCurve(QEasingCurve.InOutCubic)
        self._hide_anim.finished.connect(super().hide)

        # init UI values from defaults
        self.restore_defaults_ui()

    # --------------------------
    def _create_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(0)

        # Title bar
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setObjectName("title_bar")
        t_layout = QHBoxLayout(self.title_bar)
        t_layout.setContentsMargins(10, 0, 8, 0)

        self.title_label = QLabel("Settings")
        self.title_label.setObjectName("title_label")
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.btn_min = QPushButton("—")
        self.btn_min.setFixedSize(26, 26)
        self.btn_min.clicked.connect(self.showMinimized)

        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(26, 26)
        self.btn_close.clicked.connect(self.reject)

        t_layout.addWidget(self.title_label)
        t_layout.addStretch()
        t_layout.addWidget(self.btn_min)
        t_layout.addWidget(self.btn_close)

        root_layout.addWidget(self.title_bar)

        # Scroll area for settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        # patched: use QFrame.NoFrame (QScrollArea has no NoFrame attribute)
        scroll.setFrameShape(QFrame.NoFrame)

        self.scroll_content = QWidget()
        scroll.setWidget(self.scroll_content)
        self.form_layout = QVBoxLayout(self.scroll_content)
        self.form_layout.setContentsMargins(12, 12, 12, 12)
        self.form_layout.setSpacing(12)

        # ---- Settings rows ----
        # 1) Reload previous model
        self.reload_switch = HSwitch(False)
        self.form_layout.addLayout(self._row("Reload previous model on startup:", self.reload_switch))

        # 2) Default GPU (read-only)
        self.gpu_combo = QComboBox()
        self.gpu_combo.addItems(["NVIDIA RTX 4070", "Intel ARC", "None"])
        self.gpu_combo.setEnabled(False)
        self.form_layout.addLayout(self._row("Default graphic card:", self.gpu_combo))

        # 3) Persistent output folder (editable combobox + browse)
        out_layout = QHBoxLayout()
        self.output_combo = QComboBox()
        self.output_combo.setEditable(True)
        self.output_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self._browse_folder)
        out_layout.addWidget(self.output_combo)
        out_layout.addWidget(browse_btn)
        self.form_layout.addLayout(self._row("Persistent output folder:", out_layout))

        # 4) Always show log panel
        self.log_switch = HSwitch(False)
        self.form_layout.addLayout(self._row("Always show log panel:", self.log_switch))

        # 5) Dev mode
        self.dev_switch = HSwitch(False)
        self.form_layout.addLayout(self._row("Developer mode:", self.dev_switch))

        self.form_layout.addStretch()
        root_layout.addWidget(scroll)

        # Footer
        footer = QWidget()
        f_layout = QHBoxLayout(footer)
        f_layout.setContentsMargins(6, 8, 6, 6)

        self.restore_btn = QPushButton("Restore Defaults")
        self.restore_btn.clicked.connect(self.restore_defaults_ui)

        f_layout.addWidget(self.restore_btn)
        f_layout.addStretch()

        self.cancel_btn = QPushButton("Cancel")
        self.ok_btn = QPushButton("OK")
        self.cancel_btn.clicked.connect(self.reject)
        self.ok_btn.clicked.connect(self._on_ok)

        f_layout.addWidget(self.cancel_btn)
        f_layout.addWidget(self.ok_btn)

        root_layout.addWidget(footer)

        # allow dragging using title_bar
        self.title_bar.installEventFilter(self)

    # --------------------------
    def _row(self, label_text, widget_or_layout):
        hl = QHBoxLayout()
        lbl = QLabel(label_text)
        lbl.setMinimumWidth(220)
        lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        hl.addWidget(lbl)
        if isinstance(widget_or_layout, QWidget):
            hl.addWidget(widget_or_layout)
        else:
            hl.addLayout(widget_or_layout)
        return hl

    # --------------------------
    def apply_theme(self, theme: str):
        theme = theme.lower()
        if theme == "light":
            qss = f"""
            QLabel#title_label {{
                font-weight: 600;
                color: #222;
                font-size: 15px;
            }}
            QDialog {{
                background: transparent;
            }}
            QWidget#title_bar {{
                background: rgba(245,245,245,0.95);
                border-top-left-radius: {self.RADIUS}px;
                border-top-right-radius: {self.RADIUS}px;
            }}
            QLabel {{
                color: #222;
            }}
            QPushButton {{
                background: transparent;
                color: #444;
            }}
            """
        else:
            qss = f"""
            QLabel#title_label {{
                font-weight: 600;
                color: #fff;
                font-size: 15px;
            }}
            QDialog {{
                background: transparent;
            }}
            QWidget#title_bar {{
                background: rgba(40,40,40,0.95);
                border-top-left-radius: {self.RADIUS}px;
                border-top-right-radius: {self.RADIUS}px;
            }}
            QLabel {{
                color: #ddd;
            }}
            QPushButton {{
                background: transparent;
                color: #ddd;
            }}
            """
        self.setStyleSheet(qss)

    # --------------------------
    @Slot()
    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Choose Output Folder")
        if folder:
            # keep a small history in the combo
            items = [self.output_combo.itemText(i) for i in range(self.output_combo.count())]
            if folder not in items:
                self.output_combo.insertItem(0, folder)
            self.output_combo.setEditText(folder)

    # --------------------------
    def restore_defaults_ui(self):
        d = self.defaults
        self.reload_switch.setChecked(d.get("reload_previous", False))
        self.gpu_combo.setCurrentIndex(d.get("default_gpu_index", 0))
        folder = d.get("output_folder", "")
        if folder:
            items = [self.output_combo.itemText(i) for i in range(self.output_combo.count())]
            if folder not in items:
                self.output_combo.addItem(folder)
            self.output_combo.setEditText(folder)
        else:
            self.output_combo.setEditText("")
        self.log_switch.setChecked(d.get("always_show_log", False))
        self.dev_switch.setChecked(d.get("dev_mode", False))

    # --------------------------
    def _on_ok(self):
        self._collected = {
            "reload_previous": self.reload_switch.isChecked(),
            "default_gpu_index": self.gpu_combo.currentIndex(),
            "output_folder": self.output_combo.currentText(),
            "always_show_log": self.log_switch.isChecked(),
            "dev_mode": self.dev_switch.isChecked(),
        }
        # persist here if desired (QSettings, file, etc.)
        self.accept()

    def get_values(self):
        return self._collected

    # --------------------------
    # paint rounded background
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        bg = QColor(30, 30, 30, 245) if self.theme == "dark" else QColor(250, 250, 250, 245)
        painter.setBrush(bg)
        painter.setPen(Qt.transparent)
        painter.drawRoundedRect(self.rect(), self.RADIUS, self.RADIUS)
        super().paintEvent(event)

    # --------------------------
    # title bar dragging via eventFilter
    def eventFilter(self, obj, event):
        if obj is self.title_bar:
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self._title_bar_pressed = True
                # globalPosition() -> QPointF, convert to QPoint
                gp = event.globalPosition()
                self._mouse_offset = gp.toPoint() - self.frameGeometry().topLeft()
                return True
            elif event.type() == QEvent.MouseMove and self._title_bar_pressed:
                gp = event.globalPosition()
                new_pos = gp.toPoint() - self._mouse_offset
                self.move(new_pos)
                return True
            elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
                self._title_bar_pressed = False
                return True
        return super().eventFilter(obj, event)

    # --------------------------
    def showEvent(self, event):
        self._constrain_and_center()
        self.setWindowOpacity(0.0)
        self._show_anim.start()
        super().showEvent(event)

    def hide(self):
        # animate fade out then hide
        self._hide_anim.start()

    def _constrain_and_center(self):
        parent = self.parent()
        if parent:
            p_geom = parent.geometry()
            max_h = max(200, p_geom.height() - self.MARGIN_BOTTOM)
            max_w = max(360, p_geom.width() - 80)
            self.adjustSize()
            new_w = min(self.width(), max_w)
            new_h = min(self.height(), max_h)
            self.resize(new_w, new_h)
            parent_center = p_geom.center()
            top_left = parent_center - self.rect().center()
            self.move(top_left)
        else:
            self.adjustSize()
            screen_geom = QApplication.primaryScreen().availableGeometry()
            self.move(
                (screen_geom.width() - self.width()) // 2,
                (screen_geom.height() - self.height()) // 2,
            )

    # --------------------------
    # override exec to ensure animation plays on show
    def exec(self):
        super().show()
        return super().exec()


# -------------------------
# Minimal MainWindow demonstrating usage
# -------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.resize(900, 600)

        btn = QPushButton("Open Settings", clicked=self.open_settings)
        btn.setFixedSize(160, 40)
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addStretch()
        layout.addWidget(btn, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.setCentralWidget(container)

    def open_settings(self):
        dlg = SettingsDialog(self, theme="dark")
        # Example: toggle theme before showing:
        # dlg.toggle_theme()
        if dlg.exec() == QDialog.Accepted:
            vals = dlg.get_values()
            print("User accepted. Settings:", vals)
        else:
            print("User canceled.")


# -------------------------
# Run application
# -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
