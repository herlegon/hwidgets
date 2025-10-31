
from PySide6.QtCore import (
    Qt, QRectF, Signal, QPointF,
)
from PySide6.QtGui import (
    QPainter, QColor, QPen, QPolygonF, QBrush, QKeyEvent,
)
from PySide6.QtWidgets import (
    QWidget,
)

# Great 1: arrows
# class TimelineBar(QWidget):
#     positionChanged = Signal(float)
#     inPointChanged = Signal(float)
#     outPointChanged = Signal(float)

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.duration = 100.0
#         self.position = 0.0
#         self.in_point = 10.0
#         self.out_point = 90.0

#         self.dragging = None
#         self.setMinimumHeight(60)  # extra height for arrows

#     def setDuration(self, duration: float):
#         self.duration = max(duration, 1e-6)
#         self.update()

#     def setPosition(self, pos: float):
#         self.position = max(0, min(pos, self.duration))
#         self.update()

#     def setInOut(self, in_point: float, out_point: float):
#         self.in_point = max(0, min(in_point, self.duration))
#         self.out_point = max(0, min(out_point, self.duration))
#         self.update()

#     def _x_from_time(self, t):
#         return (t / self.duration) * self.width()

#     def _time_from_x(self, x):
#         return (x / self.width()) * self.duration

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         w, h = self.width(), self.height()

#         # Background
#         painter.fillRect(self.rect(), QColor(40, 40, 40))

#         # Trimmed region
#         in_x = self._x_from_time(self.in_point)
#         out_x = self._x_from_time(self.out_point)
#         painter.fillRect(QRectF(in_x, h/4, out_x - in_x, h/2), QColor(90, 160, 240, 100))

#         # Border lines for in/out
#         pen = QPen(QColor(90, 160, 240))
#         pen.setWidth(2)
#         painter.setPen(pen)
#         painter.drawLine(in_x, h/4, in_x, 3*h/4)
#         painter.drawLine(out_x, h/4, out_x, 3*h/4)

#         # Current position marker
#         pos_x = self._x_from_time(self.position)
#         pen = QPen(QColor(255, 200, 0))
#         pen.setWidth(3)
#         painter.setPen(pen)
#         painter.drawLine(pos_x, h/4, pos_x, 3*h/4)

#         # Draw arrows
#         self._draw_arrow(painter, in_x, h/4, up=True, color=QColor(90, 160, 240))
#         self._draw_arrow(painter, out_x, h/4, up=True, color=QColor(90, 160, 240))
#         self._draw_arrow(painter, pos_x, 3*h/4, up=False, color=QColor(255, 200, 0))

#     def _draw_arrow(self, painter, x, y, up=True, color=QColor(255, 255, 255)):
#         size = 10
#         painter.setBrush(QBrush(color))
#         painter.setPen(QPen(color))
#         points = QPolygonF()
#         if up:
#             points.append(QPointF(x, y - size))
#             points.append(QPointF(x - size/2, y))
#             points.append(QPointF(x + size/2, y))
#         else:
#             points.append(QPointF(x, y + size))
#             points.append(QPointF(x - size/2, y))
#             points.append(QPointF(x + size/2, y))
#         painter.drawPolygon(points)

#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             x = event.position().x()
#             t = self._time_from_x(x)
#             # detect near which handle (5% of duration tolerance)
#             tol = self.duration * 0.02
#             if abs(t - self.in_point) < tol:
#                 self.dragging = "in"
#             elif abs(t - self.out_point) < tol:
#                 self.dragging = "out"
#             else:
#                 self.dragging = "pos"
#             self._update_drag(t)

#     def mouseMoveEvent(self, event):
#         if self.dragging:
#             t = self._time_from_x(event.position().x())
#             self._update_drag(t)

#     def mouseReleaseEvent(self, event):
#         self.dragging = None

#     def _update_drag(self, t):
#         if self.dragging == "pos":
#             self.setPosition(t)
#             self.positionChanged.emit(self.position)
#         elif self.dragging == "in":
#             self.in_point = min(t, self.out_point - 0.1)
#             self.inPointChanged.emit(self.in_point)
#         elif self.dragging == "out":
#             self.out_point = max(t, self.in_point + 0.1)
#             self.outPointChanged.emit(self.out_point)
#         self.update()


# Great 2
# class TimelineBar(QWidget):
#     positionChanged = Signal(float)
#     inPointChanged = Signal(float)
#     outPointChanged = Signal(float)

#     def __init__(self, parent=None, fps=30):
#         super().__init__(parent)
#         self.duration = 100.0
#         self.position = 0.0
#         self.in_point = 10.0
#         self.out_point = 90.0
#         self.fps = fps  # frames per second

#         self.dragging = None
#         self.setMinimumHeight(60)

#     def setDuration(self, duration: float):
#         self.duration = max(duration, 1e-6)
#         self.update()

#     def setPosition(self, pos: float):
#         self.position = max(0, min(pos, self.duration))
#         self.update()

#     def setInOut(self, in_point: float, out_point: float):
#         self.in_point = max(0, min(in_point, self.duration))
#         self.out_point = max(0, min(out_point, self.duration))
#         self.update()

#     def setFPS(self, fps: int):
#         self.fps = fps

#     def _x_from_time(self, t):
#         return (t / self.duration) * self.width()

#     def _time_from_x(self, x):
#         t = (x / self.width()) * self.duration
#         return self._snap_to_frame(t)  # snap to nearest frame

#     def _snap_to_frame(self, t):
#         frame = round(t * self.fps)
#         return frame / self.fps

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         w, h = self.width(), self.height()

#         # Background
#         painter.fillRect(self.rect(), QColor(40, 40, 40))

#         # Trimmed region
#         in_x = self._x_from_time(self.in_point)
#         out_x = self._x_from_time(self.out_point)
#         painter.fillRect(QRectF(in_x, h/4, out_x - in_x, h/2), QColor(90, 160, 240, 100))

#         # Border lines for in/out
#         pen = QPen(QColor(90, 160, 240))
#         pen.setWidth(2)
#         painter.setPen(pen)
#         painter.drawLine(in_x, h/4, in_x, 3*h/4)
#         painter.drawLine(out_x, h/4, out_x, 3*h/4)

#         # Current position marker
#         pos_x = self._x_from_time(self.position)
#         pen = QPen(QColor(255, 200, 0))
#         pen.setWidth(3)
#         painter.setPen(pen)
#         painter.drawLine(pos_x, h/4, pos_x, 3*h/4)

#         # Draw arrows
#         self._draw_arrow(painter, in_x, h/4, up=True, color=QColor(90, 160, 240))
#         self._draw_arrow(painter, out_x, h/4, up=True, color=QColor(90, 160, 240))
#         self._draw_arrow(painter, pos_x, 3*h/4, up=False, color=QColor(255, 200, 0))

#         # Draw frame ticks
#         self._draw_frame_ticks(painter, h)

#     def _draw_arrow(self, painter, x, y, up=True, color=QColor(255, 255, 255)):
#         size = 10
#         painter.setBrush(QBrush(color))
#         painter.setPen(QPen(color))
#         points = QPolygonF()
#         if up:
#             points.append(QPointF(x, y - size))
#             points.append(QPointF(x - size/2, y))
#             points.append(QPointF(x + size/2, y))
#         else:
#             points.append(QPointF(x, y + size))
#             points.append(QPointF(x - size/2, y))
#             points.append(QPointF(x + size/2, y))
#         painter.drawPolygon(points)

#     def _draw_frame_ticks(self, painter, height):
#         pen = QPen(QColor(180, 180, 180))
#         pen.setWidth(1)
#         painter.setPen(pen)
#         tick_h = 5
#         for f in range(int(self.duration * self.fps) + 1):
#             x = self._x_from_time(f / self.fps)
#             painter.drawLine(x, height/4 - tick_h, x, height/4)

#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             x = event.position().x()
#             t = self._time_from_x(x)
#             tol = self.duration * 0.02
#             if abs(t - self.in_point) < tol:
#                 self.dragging = "in"
#             elif abs(t - self.out_point) < tol:
#                 self.dragging = "out"
#             else:
#                 self.dragging = "pos"
#             self._update_drag(t)

#     def mouseMoveEvent(self, event):
#         if self.dragging:
#             t = self._time_from_x(event.position().x())
#             self._update_drag(t)

#     def mouseReleaseEvent(self, event):
#         self.dragging = None

#     def _update_drag(self, t):
#         if self.dragging == "pos":
#             self.setPosition(t)
#             self.positionChanged.emit(self.position)
#         elif self.dragging == "in":
#             self.in_point = min(t, self.out_point - 1/self.fps)
#             self.inPointChanged.emit(self.in_point)
#         elif self.dragging == "out":
#             self.out_point = max(t, self.in_point + 1/self.fps)
#             self.outPointChanged.emit(self.out_point)
#         self.update()

class TimelineBar(QWidget):
    positionChanged = Signal(float)
    inPointChanged = Signal(float)
    outPointChanged = Signal(float)

    def __init__(self, parent=None, fps=30):
        super().__init__(parent)
        self.duration = 100.0
        self.position = 0.0
        self.in_point = 10.0
        self.out_point = 90.0
        self.fps = fps

        self.dragging = None
        self.setFocusPolicy(Qt.StrongFocus)  # allow key events
        self.setMinimumHeight(80)

    # --- Setters ---
    def setDuration(self, duration: float):
        self.duration = max(duration, 1e-6)
        self.update()

    def setFPS(self, fps: int):
        self.fps = fps
        self.update()

    def setPosition(self, pos: float):
        self.position = self._snap_to_frame(max(0, min(pos, self.duration)))
        self.update()

    def setInOut(self, in_point: float, out_point: float):
        self.in_point = self._snap_to_frame(max(0, min(in_point, self.duration)))
        self.out_point = self._snap_to_frame(max(0, min(out_point, self.duration)))
        self.update()

    # --- Helpers ---
    def _x_from_time(self, t):
        return (t / self.duration) * self.width()

    def _time_from_x(self, x):
        t = (x / self.width()) * self.duration
        return self._snap_to_frame(t)

    def _snap_to_frame(self, t):
        frame = round(t * self.fps)
        return frame / self.fps

    # --- Painting ---
    def paintEvent(self, event):
        painter = QPainter(self)
        w, h = self.width(), self.height()

        # Background
        painter.fillRect(self.rect(), QColor(40, 40, 40))

        # Highlighted trimmed region
        in_x = self._x_from_time(self.in_point)
        out_x = self._x_from_time(self.out_point)
        painter.fillRect(QRectF(in_x, h/4, out_x - in_x, h/2), QColor(90, 160, 240, 120))

        # In/out lines
        pen = QPen(QColor(90, 160, 240))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(in_x, h/4, in_x, 3*h/4)
        painter.drawLine(out_x, h/4, out_x, 3*h/4)

        # Current position marker
        pos_x = self._x_from_time(self.position)
        pen = QPen(QColor(255, 200, 0))
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawLine(pos_x, h/4, pos_x, 3*h/4)

        # Arrows
        self._draw_arrow(painter, in_x, h/4, up=True, color=QColor(90, 160, 240))
        self._draw_arrow(painter, out_x, h/4, up=True, color=QColor(90, 160, 240))
        self._draw_arrow(painter, pos_x, 3*h/4, up=False, color=QColor(255, 200, 0))

        # Frame ticks
        self._draw_frame_ticks(painter, h)

    def _draw_arrow(self, painter, x, y, up=True, color=QColor(255, 255, 255)):
        size = 10
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(color))
        points = QPolygonF()
        if up:
            points.append(QPointF(x, y - size))
            points.append(QPointF(x - size/2, y))
            points.append(QPointF(x + size/2, y))
        else:
            points.append(QPointF(x, y + size))
            points.append(QPointF(x - size/2, y))
            points.append(QPointF(x + size/2, y))
        painter.drawPolygon(points)

    def _draw_frame_ticks(self, painter, height):
        pen = QPen(QColor(180, 180, 180))
        pen.setWidth(1)
        painter.setPen(pen)
        tick_h = 5
        for f in range(int(self.duration * self.fps) + 1):
            x = self._x_from_time(f / self.fps)
            painter.drawLine(x, height/4 - tick_h, x, height/4)

    # --- Mouse events ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.position().x()
            # Pixel tolerance (~5 pixels)
            tol = 5
            # Prioritize in/out handles
            if abs(x - self._x_from_time(self.in_point)) < tol:
                self.dragging = "in"
            elif abs(x - self._x_from_time(self.out_point)) < tol:
                self.dragging = "out"
            elif abs(x - self._x_from_time(self.position)) < tol:
                self.dragging = "pos"
            else:
                # Click elsewhere moves playhead
                self.setPosition(self._time_from_x(x))
                self.positionChanged.emit(self.position)
                self.dragging = "pos"

    def mouseMoveEvent(self, event):
        if self.dragging:
            t = self._time_from_x(event.position().x())
            self._update_drag(t)

    def mouseReleaseEvent(self, event):
        self.dragging = None

    def _update_drag(self, t):
        if self.dragging == "pos":
            self.setPosition(t)
            self.positionChanged.emit(self.position)
        elif self.dragging == "in":
            self.in_point = min(t, self.out_point - 1/self.fps)
            self.inPointChanged.emit(self.in_point)
        elif self.dragging == "out":
            self.out_point = max(t, self.in_point + 1/self.fps)
            self.outPointChanged.emit(self.out_point)
        self.update()

    # --- Keyboard control ---
    def keyPressEvent(self, event: QKeyEvent):
        step = 1 / self.fps
        if event.key() == Qt.Key_Left:
            if event.modifiers() & Qt.ShiftModifier:
                # Shift + Left: move in point
                self.in_point = max(0, self.in_point - step)
                self.inPointChanged.emit(self.in_point)
            elif event.modifiers() & Qt.ControlModifier:
                # Ctrl + Left: move out point
                self.out_point = max(self.in_point + step, self.out_point - step)
                self.outPointChanged.emit(self.out_point)
            else:
                # Move playhead
                self.position = max(0, self.position - step)
                self.positionChanged.emit(self.position)
        elif event.key() == Qt.Key_Right:
            if event.modifiers() & Qt.ShiftModifier:
                self.in_point = min(self.out_point - step, self.in_point + step)
                self.inPointChanged.emit(self.in_point)
            elif event.modifiers() & Qt.ControlModifier:
                self.out_point = min(self.duration, self.out_point + step)
                self.outPointChanged.emit(self.out_point)
            else:
                self.position = min(self.duration, self.position + step)
                self.positionChanged.emit(self.position)
        self.update()









from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel
import sys

app = QApplication(sys.argv)

window = QWidget()
layout = QVBoxLayout(window)

timeline = TimelineBar()
label = QLabel("Position: 0")

def on_pos_changed(pos):
    label.setText(f"Position: {pos:.2f}")

timeline.positionChanged.connect(on_pos_changed)
layout.addWidget(timeline)
layout.addWidget(label)

window.resize(600, 100)
window.show()
app.exec()
