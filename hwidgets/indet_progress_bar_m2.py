import time
from typing import Type
from .style_manager import Theme

from PySide6.QtCore import (
    QEasingCurve,
    Qt,
    QPointF,
    QTimer,
    Signal,
)
from PySide6.QtGui import (
    QPainter,
    QPen,
    QColor,
)
from PySide6.QtWidgets import (
    QWidget,
)


class HIndetProgressBarM2(QWidget):
    finished = Signal()

    # M2 animation constants (ms)
    FIRST_LINE_HEAD_DURATION = 750
    FIRST_LINE_TAIL_DURATION = 850
    SECOND_LINE_HEAD_DURATION = 567
    SECOND_LINE_TAIL_DURATION = 533

    FIRST_LINE_HEAD_DELAY = 0
    FIRST_LINE_TAIL_DELAY = 333
    SECOND_LINE_HEAD_DELAY = 1000
    SECOND_LINE_TAIL_DELAY = 1267

    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        theme: Type[Theme],
    ):
        super().__init__(parent)
        pb_style = theme.indet_progress_bar
        self.thickness = pb_style.thickness
        self.setFixedHeight(self.thickness)
        self.setMinimumWidth(self.thickness * 4)

        self.setColors(
            track=pb_style.track,
            bar=pb_style.bar
        )


        # Easing curves
        self.curve_flh = self._make_curve((0.5, 0), (0.9, 1))
        self.curve_flt = self._make_curve((0.4, 0), (1.0, 1))
        self.curve_slh = self._make_curve((0.0, 0), (0.65, 1))
        self.curve_slt = self._make_curve((0.1, 0), (0.45, 1))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.running = False

        # Stop logic
        self._stop_requested = False
        self._stop_start_time = 0.0
        self._stop_duration = 0.25  # seconds to smoothly fill bar
        self._stop_start_values = (0.0, 0.0, 0.0, 0.0)  # flh, flt, slh, slt

        self.start_time = 0.0

        # New state variables
        self._wait_for_next_loop_stop = False
        self._stop_mode = 'smooth'  # 'smooth' or 'fill'
        self._last_t = 0.0



    def setColors(self, track: str, bar: str) -> None:
        self.track_color: QColor = QColor(track)
        self.bar_color: QColor = QColor(bar)

    def enterEvent(self, event):
        self.stop(wait_for_next=True)
        return super().enterEvent(event)


    def leaveEvent(self, event):
        self.start()
        return super().leaveEvent(event)


    def _make_curve(self, p0, p1):
        curve = QEasingCurve(QEasingCurve.Type.BezierSpline)
        curve.addCubicBezierSegment(QPointF(*p0), QPointF(*p1), QPointF(1, 1))
        return curve

    def _compute_value(self, t, duration, delay, curve):
        t_adj = max(0.0, t - delay) / duration
        t_adj = min(t_adj, 1.0)
        return curve.valueForProgress(t_adj)

    def start(self):
        """Start or restart the animation"""
        self.start_time = time.perf_counter()
        self.running = True
        self._stop_requested = False
        self._wait_for_next_loop_stop = False
        self._last_t = 0.0
        if not self.timer.isActive():
            self.timer.start(16)

    def stop(self, wait_for_next=False):
        """Stop animation smoothly and fill bar completely.

        Args:
            wait_for_next (bool): If True, waits for the current animation loop to finish
                                  before filling the bar from 0 to 1 (fast fill).
        """
        if not self.running or self._stop_requested:
            return

        if wait_for_next:
            self._wait_for_next_loop_stop = True
            return

        self._stop_requested = True
        self._stop_mode = 'smooth'
        self._stop_start_time = time.perf_counter()

        # capture current segment values at stop time
        elapsed = (time.perf_counter() - self.start_time) * 1000.0  # ms
        loop_duration = max(self.FIRST_LINE_TAIL_DELAY + self.FIRST_LINE_TAIL_DURATION,
                            self.SECOND_LINE_TAIL_DELAY + self.SECOND_LINE_TAIL_DURATION)
        t = elapsed % loop_duration

        flh = self._compute_value(t, self.FIRST_LINE_HEAD_DURATION, self.FIRST_LINE_HEAD_DELAY, self.curve_flh)
        flt = self._compute_value(t, self.FIRST_LINE_TAIL_DURATION, self.FIRST_LINE_TAIL_DELAY, self.curve_flt)
        slh = self._compute_value(t, self.SECOND_LINE_HEAD_DURATION, self.SECOND_LINE_HEAD_DELAY, self.curve_slh)
        slt = self._compute_value(t, self.SECOND_LINE_TAIL_DURATION, self.SECOND_LINE_TAIL_DELAY, self.curve_slt)
        self._stop_start_values = (flh, flt, slh, slt)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        cx = self.thickness // 2
        x0 = cx
        x1 = w - cx
        L = x1 - x0

        # Draw track
        pen = QPen(self.track_color)
        pen.setWidth(self.thickness)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawLine(x0, h // 2, x1, h // 2)

        segments = []

        # Compute segment positions
        if self._stop_requested:
            elapsed = time.perf_counter() - self._stop_start_time
            t_ratio = min(elapsed / self._stop_duration, 1.0)

            # Apply easing for smooth deceleration
            eased_t = self._ease_out_cubic(t_ratio)

            if self._stop_mode == 'fill':
                # Fast fill from 0 to 1
                segments.append((eased_t, 0.0))
            else:
                # Smooth catch-up logic
                v = self._stop_start_values
                # v = (flh, flt, slh, slt)

                # Identify active segments and find the leftmost tail
                active_tails = []
                if v[0] > v[1] + 0.001:  # Use small epsilon for float comparison
                    active_tails.append(v[1])
                if v[2] > v[3] + 0.001:
                    active_tails.append(v[3])

                if not active_tails:
                    min_tail = 1.0
                else:
                    min_tail = min(active_tails)

                # 1. Fill from left (0 to min_tail)
                segments.append((min_tail * eased_t, 0.0))

                # 2. Extend existing ACTIVE segments to right
                # First line
                if v[0] > v[1] + 0.001:
                    new_head = v[0] + (1.0 - v[0]) * eased_t
                    segments.append((new_head, v[1]))

                # Second line
                if v[2] > v[3] + 0.001:
                    new_head = v[2] + (1.0 - v[2]) * eased_t
                    segments.append((new_head, v[3]))

            if t_ratio >= 1.0:
                self._stop_requested = False
                self.running = False
                self.timer.stop()
                self.finished.emit()
        else:
            elapsed = (time.perf_counter() - self.start_time) * 1000.0  # ms
            loop_duration = max(self.FIRST_LINE_TAIL_DELAY + self.FIRST_LINE_TAIL_DURATION,
                                self.SECOND_LINE_TAIL_DELAY + self.SECOND_LINE_TAIL_DURATION)
            t = elapsed % loop_duration

            # Check for wait_for_next trigger
            if self._wait_for_next_loop_stop and t < self._last_t:
                self._wait_for_next_loop_stop = False
                self._stop_requested = True
                self._stop_mode = 'fill'
                self._stop_start_time = time.perf_counter()
                # We are now in stop mode, so we skip the rest of this block in next frame
                # For this frame, we can just draw empty or start the fill.
                # Let's start fill immediately to avoid flicker.
                # Recursive call or just fall through?
                # Simplest is to let next frame handle it, but we might have a 1-frame glitch.
                # Let's just set t_ratio=0 manually for this frame if we want.
                # But 't' is already calculated for normal run.
                # Let's just continue with normal run for this one frame (it's the start of loop anyway)
                # and next frame will pick up _stop_requested.

            self._last_t = t

            flh = self._compute_value(t, self.FIRST_LINE_HEAD_DURATION, self.FIRST_LINE_HEAD_DELAY, self.curve_flh)
            flt = self._compute_value(t, self.FIRST_LINE_TAIL_DURATION, self.FIRST_LINE_TAIL_DELAY, self.curve_flt)
            slh = self._compute_value(t, self.SECOND_LINE_HEAD_DURATION, self.SECOND_LINE_HEAD_DELAY, self.curve_slh)
            slt = self._compute_value(t, self.SECOND_LINE_TAIL_DURATION, self.SECOND_LINE_TAIL_DELAY, self.curve_slt)

            segments.append((flh, flt))
            segments.append((slh, slt))

        # Draw segments
        pen.setColor(self.bar_color)
        painter.setPen(pen)

        for head, tail in segments:
            if head <= tail:
                continue
            sx = x0 + tail * L
            ex = x0 + head * L
            sx = max(sx, x0)
            ex = min(ex, x1)
            if ex <= sx:
                continue
            painter.drawLine(int(sx), h // 2, int(ex), h // 2)

        painter.end()

    def _ease_out_cubic(self, t):
        """Easing function for smooth deceleration"""
        return 1 - pow(1 - t, 3)

