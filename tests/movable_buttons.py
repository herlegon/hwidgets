from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFrame,
    QLabel, QHBoxLayout, QSizePolicy, QSlider, QCheckBox
)
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QColor
import sys


class SettingsPanel(QFrame):
    """Expandable settings section below each item."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #e2e8f0;
                border-radius: 8px;
            }
            QLabel {
                color: #1e293b;
                font-size: 13px;
            }
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Volume:"))
        slider = QSlider(Qt.Horizontal)
        slider.setValue(50)
        layout.addWidget(slider)

        enable_check = QCheckBox("Enable advanced")
        layout.addWidget(enable_check)
        layout.addStretch()


class ButtonItem(QFrame):
    """A draggable, removable, disable-able item with expandable settings."""
    def __init__(self, text, parent):
        super().__init__(parent)
        self.dragging = False
        self.offset = QPoint()
        self.original_index = None
        self.expanded = False
        self.settings = None
        self.disabled = False

        self.setStyleSheet("""
            QFrame {
                background-color: #3b82f6;
                color: white;
                border-radius: 8px;
            }
            QLabel {
                color: white;
                font-size: 14px;
                padding: 4px 8px;
            }
            QPushButton {
                background: transparent;
                color: white;
                border: none;
                font-weight: bold;
                padding: 4px 6px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
                border-radius: 4px;
            }
        """)

        # --- Main Layout ---
        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.outer_layout.setSpacing(0)

        self.header = QFrame()
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(6, 4, 6, 4)
        header_layout.setSpacing(4)

        # --- Arrow button ---
        self.arrow_btn = QPushButton("▶")
        self.arrow_btn.setFixedWidth(22)
        self.arrow_btn.clicked.connect(self.toggle_settings)
        header_layout.addWidget(self.arrow_btn)

        self.label = QLabel(text)
        header_layout.addWidget(self.label, 1)

        # Disable button
        self.disable_btn = QPushButton("🚫")
        self.disable_btn.setToolTip("Disable/Enable")
        self.disable_btn.clicked.connect(self.toggle_disabled)
        header_layout.addWidget(self.disable_btn)

        # Remove button
        self.remove_btn = QPushButton("❌")
        self.remove_btn.setToolTip("Remove")
        self.remove_btn.clicked.connect(self.remove_self)
        header_layout.addWidget(self.remove_btn)

        self.outer_layout.addWidget(self.header)

        # --- Settings container ---
        self.settings_container = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_container)
        self.settings_layout.setContentsMargins(0, 0, 0, 0)
        self.settings_container.setFixedHeight(0)
        self.outer_layout.addWidget(self.settings_container)

    # === Settings toggle ===
    def toggle_settings(self):
        if self.disabled:
            return
        if not self.expanded:
            self.show_settings()
        else:
            self.hide_settings()

    def show_settings(self):
        if self.settings is None:
            self.settings = SettingsPanel()
            self.settings_layout.addWidget(self.settings)

        self.animate_settings_height(100)
        self.arrow_btn.setText("▼")
        self.expanded = True

    def hide_settings(self):
        self.animate_settings_height(0)
        self.arrow_btn.setText("▶")
        self.expanded = False

    def animate_settings_height(self, target_height):
        animation = QPropertyAnimation(self.settings_container, b"maximumHeight")
        animation.setDuration(250)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.setStartValue(self.settings_container.height())
        animation.setEndValue(target_height)
        animation.start()
        self._anim = animation  # Keep reference to prevent GC

    # === Disable / Remove ===
    def toggle_disabled(self):
        self.disabled = not self.disabled
        if self.disabled:
            self.setStyleSheet("""
                QFrame {
                    background-color: #9ca3af;
                    color: #f1f5f9;
                    border-radius: 8px;
                }
                QLabel {
                    color: #f1f5f9;
                    font-size: 14px;
                    padding: 4px 8px;
                }
                QPushButton {
                    background: transparent;
                    color: #f1f5f9;
                    border: none;
                    font-weight: bold;
                    padding: 4px 6px;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: #3b82f6;
                    color: white;
                    border-radius: 8px;
                }
                QLabel {
                    color: white;
                    font-size: 14px;
                    padding: 4px 8px;
                }
                QPushButton {
                    background: transparent;
                    color: white;
                    border: none;
                    font-weight: bold;
                    padding: 4px 6px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.15);
                    border-radius: 4px;
                }
            """)

    def remove_self(self):
        self.parent().removeItem(self)

    # === Dragging ===
    def mousePressEvent(self, event):
        # Avoid dragging when clicking on small buttons (arrow, remove, disable)
        if event.button() == Qt.LeftButton and event.pos().x() > 30 and not self.disabled:
            self.dragging = True
            self.offset = event.position().toPoint()
            self.raise_()
            self.original_index = self.parent().layout.indexOf(self)
            self.parent().startDragging(self)
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging:
            pos = self.mapToParent(event.position().toPoint() - self.offset)
            self.move(0, pos.y())
            self.parent().updateDropIndicator(self)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.dragging:
            self.dragging = False
            self.parent().finishDragging(self)
            event.accept()
        else:
            super().mouseReleaseEvent(event)


class ReorderableWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setStyleSheet("""
            QFrame {
                background-color: #f1f5f9;
                border: 2px dashed #94a3b8;
                border-radius: 10px;
            }
        """)
        self.drop_indicator_y = None
        self.dragged_widget = None

    def addItem(self, text):
        item = ButtonItem(text, self)
        self.layout.addWidget(item)

    def removeItem(self, widget):
        self.layout.removeWidget(widget)
        widget.deleteLater()
        self.relayout()

    # --- Drag Management ---
    def startDragging(self, widget):
        self.dragged_widget = widget
        self.layout.removeWidget(widget)
        widget.setParent(self)
        widget.show()

    def updateDropIndicator(self, widget):
        y = widget.y() + widget.height() / 2
        self.drop_indicator_y = None
        for i in range(self.layout.count()):
            w = self.layout.itemAt(i).widget()
            if y < w.y() + w.height() / 2:
                self.drop_indicator_y = w.y()
                break
        else:
            if self.layout.count() > 0:
                last = self.layout.itemAt(self.layout.count() - 1).widget()
                self.drop_indicator_y = last.y() + last.height() + 5
        self.update()

    def finishDragging(self, widget):
        index = self.layout.count()
        if self.drop_indicator_y is not None:
            for i in range(self.layout.count()):
                w = self.layout.itemAt(i).widget()
                if widget.y() < w.y() + w.height() / 2:
                    index = i
                    break
        self.layout.insertWidget(index, widget)
        self.dragged_widget = None
        self.drop_indicator_y = None
        self.relayout()
        self.update()

    def relayout(self):
        for i in range(self.layout.count()):
            w = self.layout.itemAt(i).widget()
            w.move(0, i * (w.height() + self.layout.spacing()))

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.drop_indicator_y is not None:
            painter = QPainter(self)
            pen = painter.pen()
            pen.setWidth(3)
            pen.setColor(QColor("#2563eb"))
            painter.setPen(pen)
            painter.drawLine(5, self.drop_indicator_y, self.width() - 5, self.drop_indicator_y)
            painter.end()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📦 Draggable Buttons with Arrow + Settings")
        self.resize(380, 520)

        layout = QVBoxLayout(self)
        self.reorderable = ReorderableWidget()
        layout.addWidget(self.reorderable)

        add_button = QPushButton("+ Add Button")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border-radius: 8px;
                padding: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        add_button.clicked.connect(self.add_new_button)
        layout.addWidget(add_button)

        for i in range(3):
            self.reorderable.addItem(f"Button {i+1}")

    def add_new_button(self):
        count = self.reorderable.layout.count()
        self.reorderable.addItem(f"Button {count+1}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
