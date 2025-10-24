import signal
from PySide6.QtWidgets import (
    QApplication, QWidget, QPlainTextEdit, QScrollBar, QVBoxLayout
)
from PySide6.QtCore import Qt, QRect, Slot, QEvent
from PySide6.QtGui import QPainter, QColor, QBrush


class OverlayVScrollBar(QScrollBar):
    def __init__(self, parent=None, corner_radius=8, base_width=12):
        super().__init__(Qt.Vertical, parent)
        self.corner_radius = corner_radius
        self._base_width = base_width
        self._hover_extra = 2  # widget widens by this amount on hover
        self._hover_shift = 1  # handle shifts left by this amount
        self._handle_color = QColor("#66c")
        self._hover_color = QColor("#77f")
        self._hovered = False
        self.setMouseTracking(True)
        self.setFixedWidth(base_width)

    def enterEvent(self, event):
        self._hovered = True
        self.setFixedWidth(self._base_width + self._hover_extra)
        self.reposition_and_resize()
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.setFixedWidth(self._base_width)
        self.reposition_and_resize()
        self.update()
        super().leaveEvent(event)

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
        if self._hovered:
            x -= self._hover_shift  # shift left on hover
        y = cr
        self.setGeometry(QRect(x, y, w, h))


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # compute handle rect manually, same as paintEvent
            handle_height = max(20, int(self.pageStep() / (self.maximum() - self.minimum() + self.pageStep()) * self.height()))
            handle_pos = 0 if self.maximum() == self.minimum() else int((self.value() - self.minimum()) / (self.maximum() - self.minimum()) * (self.height() - handle_height))
            handle_rect = QRect(0, handle_pos, self.width(), handle_height)
            if self._hovered:
                handle_rect.translate(-self._hover_shift, 0)
            # if click inside handle, start dragging
            if handle_rect.contains(event.position().toPoint()):
                super().mousePressEvent(event)
            else:
                # move handle to click position (optional: center handle)
                val_range = self.maximum() - self.minimum()
                new_val = self.minimum() + int(event.position().toPoint().y() / (self.height() - handle_height) * val_range)
                self.setValue(new_val)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # normal drag works
        super().mouseMoveEvent(event)



    def paintEvent(self, event):
        """Draw handle manually, full range top-to-bottom."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.transparent)

        # Compute handle height
        if self.maximum() == self.minimum():
            slider_height = self.height()
            slider_pos = 0
        else:
            slider_height = max(
                20,
                int(self.pageStep() / (self.maximum() - self.minimum() + self.pageStep()) * self.height())
            )
            slider_pos = int((self.value() - self.minimum()) / (self.maximum() - self.minimum()) * (self.height() - slider_height))

        handle_rect = QRect(0, slider_pos, self.width(), slider_height)
        if self._hovered:
            handle_rect.translate(-self._hover_shift, 0)
            # clamp handle inside widget
            handle_rect.setLeft(max(0, handle_rect.left()))
            handle_rect.setRight(min(self.width(), handle_rect.right()))

        color = self._hover_color if self._hovered else self._handle_color
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(handle_rect, 6, 6)


class CustomTextEdit(QPlainTextEdit):
    def __init__(self, corner_radius=8, overlay_width=12, parent=None):
        super().__init__(parent)
        self.corner_radius = corner_radius
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                border: 2px solid #66c;
                border-radius: {corner_radius}px;
                background: white;
                padding-right: 6px; /* leave space so text doesn't collide with overlay */
            }}
        """)
        # hide native scrollbar completely
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # create overlay scrollbar
        self.overlay_vbar = OverlayVScrollBar(self, corner_radius=corner_radius, base_width=overlay_width)
        self.overlay_vbar.reposition_and_resize()

        # sync overlay with native scrollbar
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
            self.overlay_vbar.setSingleStep(max(1, native.singleStep()))
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
