import signal
from PySide6.QtWidgets import QApplication, QWidget, QPlainTextEdit, QVBoxLayout
from PySide6.QtCore import Qt, QRect, Signal, Slot, QPoint
from PySide6.QtGui import QPainter, QColor, QBrush, QMouseEvent


class OverlayVScrollBar(QWidget):
    valueChanged = Signal(int)

    def __init__(self, parent=None, corner_radius=8, width=12):
        super().__init__(parent)
        self.corner_radius = corner_radius
        self._base_width = width
        self._hover_extra = 2
        self._hover_shift = 1
        self._hovered = False
        self._pressed = False
        self._press_offset = 0
        self._value = 0
        self._minimum = 0
        self._maximum = 100
        self._page_step = 10
        self.setMouseTracking(True)
        self.setFixedWidth(width)

    def setRange(self, minimum, maximum):
        self._minimum = minimum
        self._maximum = maximum
        self.update()

    def setPageStep(self, step):
        self._page_step = step
        self.update()

    def setValue(self, value):
        value = max(self._minimum, min(self._maximum, value))
        if self._value != value:
            self._value = value
            self.valueChanged.emit(value)
            self.update()

    def value(self):
        return self._value

    def enterEvent(self, event):
        self._hovered = True
        self.setFixedWidth(self._base_width + self._hover_extra)
        self.reposition_and_resize()
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        if not self._pressed:
            self.setFixedWidth(self._base_width)
            self.reposition_and_resize()
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            handle_rect = self._handle_rect()
            if handle_rect.contains(event.position().toPoint()):
                self._pressed = True
                self._press_offset = event.position().y() - handle_rect.top()
            else:
                # Jump handle to click position
                self._jump_to_click(event.position().y())
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._pressed:
            y = event.position().y() - self._press_offset
            self._move_handle_to(y)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._pressed = False
            if not self._hovered:
                self.setFixedWidth(self._base_width)
                self.reposition_and_resize()
        super().mouseReleaseEvent(event)

    def _jump_to_click(self, y):
        # Move handle center to click
        handle_height = max(20, int(self._page_step / (self._maximum - self._minimum + self._page_step) * self.height()))
        new_value = int(self._minimum + (y - handle_height // 2) / (self.height() - handle_height) * (self._maximum - self._minimum))
        self.setValue(new_value)

    def _move_handle_to(self, y):
        handle_height = max(20, int(self._page_step / (self._maximum - self._minimum + self._page_step) * self.height()))
        new_value = int(self._minimum + y / (self.height() - handle_height) * (self._maximum - self._minimum))
        self.setValue(new_value)

    def _handle_rect(self):
        if self._maximum == self._minimum:
            slider_height = self.height()
            slider_pos = 0
        else:
            slider_height = max(20, int(self._page_step / (self._maximum - self._minimum + self._page_step) * self.height()))
            slider_pos = int((self._value - self._minimum) / (self._maximum - self._minimum) * (self.height() - slider_height))
        rect = QRect(0, slider_pos, self.width(), slider_height)
        if self._hovered:
            rect.translate(-self._hover_shift, 0)
            rect.setLeft(max(0, rect.left()))
            rect.setRight(min(self.width(), rect.right()))
        return rect

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.transparent)
        handle_rect = self._handle_rect()
        color = QColor("#77f") if self._hovered else QColor("#66c")
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(handle_rect, 6, 6)

    def reposition_and_resize(self):
        parent = self.parent()
        if not parent:
            return
        pw = parent.width()
        ph = parent.height()
        cr = self.corner_radius
        w = self.width()
        h = max(0, ph - 2 * cr)
        x = pw - w
        y = cr
        self.setGeometry(QRect(x, y, w, h))


class CustomTextEdit(QPlainTextEdit):
    def __init__(self, corner_radius=8, overlay_width=12, parent=None):
        super().__init__(parent)
        self.corner_radius = corner_radius
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                border: 2px solid #66c;
                border-radius: {corner_radius}px;
                background: white;
                padding-right: 6px;
            }}
        """)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.overlay_vbar = OverlayVScrollBar(self, corner_radius=corner_radius, width=overlay_width)
        self.overlay_vbar.reposition_and_resize()

        native_vbar = super().verticalScrollBar()
        native_vbar.rangeChanged.connect(self._on_native_range_changed)
        native_vbar.valueChanged.connect(self._on_native_value_changed)
        self.overlay_vbar.valueChanged.connect(self._on_overlay_value_changed)
        self._sync_overlay_from_native()

    @Slot(int, int)
    def _on_native_range_changed(self, minimum, maximum):
        self._sync_overlay_from_native()

    @Slot(int)
    def _on_native_value_changed(self, value):
        if self.overlay_vbar.value() != value:
            self.overlay_vbar.setValue(value)

    @Slot(int)
    def _on_overlay_value_changed(self, value):
        native = super().verticalScrollBar()
        if native.value() != value:
            native.setValue(value)

    def _sync_overlay_from_native(self):
        native = super().verticalScrollBar()
        self.overlay_vbar.blockSignals(True)
        try:
            self.overlay_vbar.setRange(native.minimum(), native.maximum())
            self.overlay_vbar.setPageStep(native.pageStep())
            self.overlay_vbar.setValue(native.value())
        finally:
            self.overlay_vbar.blockSignals(False)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.overlay_vbar.reposition_and_resize()
        self._sync_overlay_from_native()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication([])

    win = QWidget()
    layout = QVBoxLayout(win)
    edit = CustomTextEdit(corner_radius=12, overlay_width=12)
    edit.setPlainText("\n".join(f"Line {i}" for i in range(200)))
    layout.addWidget(edit)

    win.resize(480, 360)
    win.show()
    app.exec()
