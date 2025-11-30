import signal
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QPolygonF, QMouseEvent
import sys


class VideoRangeSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.duration = 180  # 3 minutes in seconds
        self.current_time = 45
        self.range_start = 30
        self.range_end = 120
        self.is_dragging = None

        self.setMinimumSize(1000, 200)
        self.setStyleSheet("background-color: #1c1d20;")
        self.setMouseTracking(True)

    def format_time(self, seconds):
        mins = int(seconds // 60)
        secs = seconds % 60
        return f"{mins}:{secs:04.1f}"

    def get_position_percent(self, time):
        return (time / self.duration) * 100

    def get_time_from_position(self, x, timeline_rect):
        rel_x = max(0, min(x - timeline_rect.x(), timeline_rect.width()))
        return (rel_x / timeline_rect.width()) * self.duration

    def get_timeline_rect(self):
        margin = 50
        width = self.width() - 2 * margin
        y = self.height() // 2
        return QRectF(margin, y, width, 4)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        timeline_rect = self.get_timeline_rect()
        tick_y = timeline_rect.top()

        # Draw tick marks and labels
        painter.setPen(QPen(QColor("#d1d1d1")))
        font = painter.font()
        font.setFamily("Courier")
        font.setPointSize(9)
        painter.setFont(font)

        for i in range(0, self.duration + 1, 30):
            x_pos = timeline_rect.x() + (i / self.duration) * timeline_rect.width()

            # Draw tick label
            text = self.format_time(i)
            text_rect = painter.fontMetrics().boundingRect(text)
            painter.drawText(int(x_pos - text_rect.width() / 2), int(tick_y - 16), text)

            # Draw tick mark
            painter.setPen(QPen(QColor("#5a5a5a"), 1))
            painter.drawLine(int(x_pos), int(tick_y - 4), int(x_pos), int(tick_y - 12))

        # Draw intermediary ticks (every 5 seconds, excluding main ticks)
        painter.setPen(QPen(QColor("#4b4b4b"), 1))
        for i in range(5, self.duration, 5):
            if i % 30 != 0:  # Skip main tick positions
                x_pos = timeline_rect.x() + (i / self.duration) * timeline_rect.width()
                painter.drawLine(int(x_pos), int(tick_y - 4), int(x_pos), int(tick_y - 8))

        # Draw timeline background
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#5a5a5a"))
        painter.drawRoundedRect(timeline_rect, 2, 2)

        # Draw selected range
        start_x = timeline_rect.x() + (self.range_start / self.duration) * timeline_rect.width()
        end_x = timeline_rect.x() + (self.range_end / self.duration) * timeline_rect.width()
        range_rect = QRectF(start_x, timeline_rect.y(), end_x - start_x, timeline_rect.height())
        painter.setBrush(QColor("#8a9eff"))
        painter.drawRoundedRect(range_rect, 2, 2)

        # Draw start handle (◢)
        start_x = timeline_rect.x() + (self.range_start / self.duration) * timeline_rect.width()
        start_triangle = QPolygonF([
            QPointF(start_x, timeline_rect.bottom() + 12),
            QPointF(start_x, timeline_rect.bottom()),
            QPointF(start_x - 12, timeline_rect.bottom() + 12)
        ])
        painter.setBrush(QColor("#5e7ce0"))
        painter.drawPolygon(start_triangle)

        # Draw end handle (◣)
        end_x = timeline_rect.x() + (self.range_end / self.duration) * timeline_rect.width()
        end_triangle = QPolygonF([
            QPointF(end_x, timeline_rect.bottom()),
            QPointF(end_x + 12, timeline_rect.bottom() + 12),
            QPointF(end_x, timeline_rect.bottom() + 12)
        ])
        painter.drawPolygon(end_triangle)

        # Draw playhead (▼)
        playhead_x = timeline_rect.x() + (self.current_time / self.duration) * timeline_rect.width()
        playhead_triangle = QPolygonF([
            QPointF(playhead_x - 6, timeline_rect.top() - 10),
            QPointF(playhead_x + 6, timeline_rect.top() - 10),
            QPointF(playhead_x, timeline_rect.top())
        ])
        painter.setBrush(QColor("red"))
        painter.drawPolygon(playhead_triangle)




    def mousePressEvent(self, event: QMouseEvent):
        timeline_rect = self.get_timeline_rect()
        x = event.position().x()
        y = event.position().y()

        handle_margin = 15  # Margin around handles to prevent accidental playhead moves

        # Check start handle first
        start_x = timeline_rect.x() + (self.range_start / self.duration) * timeline_rect.width()
        if abs(x - start_x) < handle_margin and timeline_rect.bottom() < y < timeline_rect.bottom() + 20:
            self.is_dragging = 'start'
            return

        # Check end handle
        end_x = timeline_rect.x() + (self.range_end / self.duration) * timeline_rect.width()
        if abs(x - end_x) < handle_margin and timeline_rect.bottom() < y < timeline_rect.bottom() + 20:
            self.is_dragging = 'end'
            return

        # Check playhead (for dragging)
        playhead_x = timeline_rect.x() + (self.current_time / self.duration) * timeline_rect.width()
        if abs(x - playhead_x) < 10 and timeline_rect.top() - 15 < y < timeline_rect.top() + 5:
            self.is_dragging = 'playhead'
            return

        # Click anywhere else within reasonable bounds moves playhead
        # Allow clicks in a larger vertical area around the timeline
        if (timeline_rect.left() <= x <= timeline_rect.right() and
            timeline_rect.top() - 30 <= y <= timeline_rect.bottom() + 30):
            self.current_time = self.get_time_from_position(x, timeline_rect)
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_dragging is None:
            return

        timeline_rect = self.get_timeline_rect()
        time = self.get_time_from_position(event.position().x(), timeline_rect)

        if self.is_dragging == 'start':
            self.range_start = max(0, min(time, self.range_end - 1))
        elif self.is_dragging == 'end':
            self.range_end = max(self.range_start + 1, min(time, self.duration))
        elif self.is_dragging == 'playhead':
            self.current_time = max(0, min(time, self.duration))

        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.is_dragging = None

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    window = VideoRangeSelector()
    window.setWindowTitle("Video Range Selector")
    window.show()
    sys.exit(app.exec())
