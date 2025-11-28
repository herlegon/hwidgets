import time
from typing import Type
from .style_manager import Theme

from PySide6.QtCore import (
    QEasingCurve,
    Qt,
    QPropertyAnimation,
    Property,
    QParallelAnimationGroup,
    QSequentialAnimationGroup,
    QPointF,
    QTimer,
)
from PySide6.QtGui import (
    QPaintEvent,
    QPainter,
    QColor,
    QPen,
)
from PySide6.QtWidgets import (
    QProgressBar,
    QWidget,
)


class HIndetProgressBar(QProgressBar):
    # M2 Animation timing constants (in milliseconds)
    # Reference: Material Design M2 Progress Indicators spec
    M2_FIRST_LINE_HEAD_DURATION = 750
    M2_FIRST_LINE_TAIL_DURATION = 850
    M2_SECOND_LINE_HEAD_DURATION = 567
    M2_SECOND_LINE_TAIL_DURATION = 533

    M2_FIRST_LINE_HEAD_DELAY = 0
    M2_FIRST_LINE_TAIL_DELAY = 333
    M2_SECOND_LINE_HEAD_DELAY = 1000
    M2_SECOND_LINE_TAIL_DELAY = 1267

    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        theme: Type[Theme],
        minimum: int | None = None,
        maximum: int | None = None,
        text: str | None = None,
        value: int | None = None,
        alignment: Qt.AlignmentFlag | None = None,
        textVisible: bool | None = None,
        orientation: Qt.Orientation | None = None,
        invertedAppearance: bool | None = None,
        textDirection: QProgressBar.Direction | None = None,
        format: str | None = None,
        m3: bool = False
    ):
        super().__init__(parent)
        pb_style = theme.indet_progress_bar
        self.thickness = pb_style.thickness
        self.setFixedHeight(self.thickness)
        self.setMinimumWidth(self.thickness*4)

        self.setColors(
            track=pb_style.track,
            bar=pb_style.bar
        )

        self._progress = 0
        self.setMinimum(0)
        self.setMaximum(1.0)
        self.setValue(0)

        self._flh: float = 0.
        self._flt: float = 0.
        self._slh: float = 0.
        self._slt: float = 0.

        LinearAnimationDuration = 1800

        last_pause = 435
        last_pause = 0

        FirstLineHeadEasing = ((0.5, 0), (0.9, 1))
        FirstLineTailEasing = ((0.4, 0), (1, 1))
        SecondLineHeadEasing = ((0, 0), (0.65, 1))
        SecondLineTailEasing = ((0.1, 0), (0.45, 1))


        curve_flh = QEasingCurve(QEasingCurve.Type.BezierSpline)
        curve_flh.addCubicBezierSegment(
            QPointF(*FirstLineHeadEasing[0]),
            QPointF(*FirstLineHeadEasing[1]),
            QPointF(1, 1)
        )

        curve_flt = QEasingCurve(QEasingCurve.Type.BezierSpline)
        curve_flt.addCubicBezierSegment(
            QPointF(*FirstLineTailEasing[0]),
            QPointF(*FirstLineTailEasing[1]),
            QPointF(1, 1)
        )

        curve_slh = QEasingCurve(QEasingCurve.Type.BezierSpline)
        curve_slh.addCubicBezierSegment(
            QPointF(*SecondLineHeadEasing[0]),
            QPointF(*SecondLineHeadEasing[1]),
            QPointF(1, 1)
        )

        curve_slt = QEasingCurve(QEasingCurve.Type.BezierSpline)
        curve_slt.addCubicBezierSegment(
            QPointF(*SecondLineTailEasing[0]),
            QPointF(*SecondLineTailEasing[1]),
            QPointF(1, 1)
        )

        self.animation_flh = QPropertyAnimation(self, b'flh', self)
        self.animation_flh.setDuration(self.M2_FIRST_LINE_HEAD_DURATION)
        self.animation_flh.setEasingCurve(curve_flh)
        self.animation_flh.setStartValue(0.)
        self.animation_flh.setEndValue(1.)
        self.animation_flh_group = QSequentialAnimationGroup(self)
        self.animation_flh_group.addPause(self.M2_FIRST_LINE_HEAD_DELAY)
        self.animation_flh_group.addAnimation(self.animation_flh)

        self.animation_flt = QPropertyAnimation(self, b'flt', self)
        self.animation_flt.setDuration(self.M2_FIRST_LINE_TAIL_DURATION)
        self.animation_flt.setEasingCurve(curve_flt)
        self.animation_flt.setStartValue(0.)
        self.animation_flt.setEndValue(1.)
        self.animation_flt_group = QSequentialAnimationGroup(self)
        self.animation_flt_group.addPause(self.M2_FIRST_LINE_TAIL_DELAY)
        self.animation_flt_group.addAnimation(self.animation_flt)

        self.animation_slh = QPropertyAnimation(self, b'slh', self)
        self.animation_slh.setDuration(self.M2_SECOND_LINE_HEAD_DURATION)
        self.animation_slh.setEasingCurve(curve_slh)
        self.animation_slh.setStartValue(0.)
        self.animation_slh.setEndValue(1.)
        self.animation_slh_group = QSequentialAnimationGroup(self)
        self.animation_slh_group.addPause(self.M2_SECOND_LINE_HEAD_DELAY)
        self.animation_slh_group.addAnimation(self.animation_slh)

        self.animation_slt = QPropertyAnimation(self, b'slt', self)
        self.animation_slt.setDuration(self.M2_SECOND_LINE_TAIL_DURATION)
        self.animation_slt.setEasingCurve(curve_slt)
        self.animation_slt.setStartValue(0.)
        self.animation_slt.setEndValue(1.)
        self.animation_slt_group = QSequentialAnimationGroup(self)
        self.animation_slt_group.addPause(self.M2_SECOND_LINE_TAIL_DELAY)
        self.animation_slt_group.addAnimation(self.animation_slt)
        self.animation_slt_group.addPause(last_pause)


        self.animations = QParallelAnimationGroup(self)
        self.animations.addAnimation(self.animation_flh_group)
        self.animations.addAnimation(self.animation_flt_group)
        self.animations.addAnimation(self.animation_slh_group)
        self.animations.addAnimation(self.animation_slt_group)

        self.timer_start = 0
        self._should_restart = True
        self.animations.finished.connect(self.animations_finished)
        self.animations.setLoopCount(1)
        self.animations.start()


    def setColors(self, track: str, bar: str) -> None:
        self.track_color: QColor = QColor(track)
        self.bar_color: QColor = QColor(bar)


    def animations_finished(self):
        if self._should_restart:
            self._flh = 0.
            self._flt = 0.
            self._slh = 0.
            self._slt = 0.
            self.animations.start()
        else:
            self._flh = 1.0
            self._flt = 1.0
            self._slh = 1.0
            self._slt = 1.0
            self.setValue(1.0)
            self.repaint()


    def stop(self) -> None:
        """Stop animation after current loop finishes and fill the bar."""
        self._should_restart = False

        # Jump all sequential groups to end immediately
        for i in range(self.animations.animationCount()):
            group = self.animations.animationAt(i)
            if isinstance(group, QSequentialAnimationGroup):
                group.setCurrentTime(group.duration())  # jump to end
            elif isinstance(group, QPropertyAnimation):
                group.setCurrentTime(group.duration())

        # Ensure all progress values are fully filled
        self._flh = self._flt = self._slh = self._slt = 1.0
        self.setValue(1)
        self.repaint()


    def start(self) -> None:
        """Start or restart the indeterminate animation."""
        self._should_restart = True
        self._flh = self._flt = self._slh = self._slt = 0.
        self.repaint()
        self.animations.start()


    @Property(float)
    def flh(self) -> float:
        return self._flh


    @flh.setter
    def flh(self, value: float) -> None:
        self._flh = value
        self.repaint()


    @Property(float)
    def flt(self) -> float:
        return self._flt


    @flt.setter
    def flt(self, value: float) -> None:
        self._flt = value
        self.repaint()


    @Property(float)
    def slh(self) -> float:
        return self._slh


    @slh.setter
    def slh(self, value: float) -> None:
        self._slh = value
        self.repaint()


    @Property(float)
    def slt(self) -> float:
        return self._slt


    @slt.setter
    def slt(self, value: float) -> None:
        self._slt = value
        self.repaint()


    # def enterEvent(self, event):
    #     self.animations.pause()
    #     return super().enterEvent(event)


    # def leaveEvent(self, event):
    #     self.animations.resume()
    #     return super().leaveEvent(event)


    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, on=True)

        thickness = self.thickness
        cy = thickness // 2

        x0 = thickness // 2
        x1 = self.width() - thickness // 2
        L = x1 - x0

        # Clear track
        pen = QPen(self.track_color)
        pen.setWidth(thickness)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(x0, cy, x1, cy)

        # Draw a single moving segment
        def draw_segment(head, tail):
            """head/tail are 0-1 floats"""

            if head <= tail:
                return  # segment has reversed or zero-length

            sx = x0 + tail * L
            ex = x0 + head * L

            if ex <= x0 or sx >= x1:
                return  # off screen

            sx = max(sx, x0)
            ex = min(ex, x1)

            pen.setColor(self.bar_color)
            painter.setPen(pen)
            painter.drawLine(int(sx), cy, int(ex), cy)

        # First segment (always visible)
        draw_segment(self.flh, self.flt)

        # Second segment (starts later)
        draw_segment(self.slh, self.slt)

        painter.end()





class HIndetProgressBarR(QWidget):
    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        theme: Type[Theme],
    ):
        super().__init__(parent)
        pb_style = theme.indet_progress_bar
        self.thickness = pb_style.thickness + 2
        self.setFixedHeight(self.thickness)
        self.setMinimumWidth(self.thickness*4)

        self.setColors(
            track=pb_style.track,
            bar=pb_style.bar
        )

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # ~60 FPS
        self.start_time = time.perf_counter()


    def setColors(self, track: str, bar: str) -> None:
        self.track_color: QColor = QColor(track)
        self.bar_color: QColor = QColor(bar)


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

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

        # Compute pulse position
        t = (time.perf_counter() - self.start_time) % 1.2  # period ~1.2s
        center = -0.2 + 1.4 * t  # moves from slightly before start to slightly past end
        pulse_width = 0.25  # fraction of track

        # Draw gradient tail with multiple sub-segments
        for i, alpha in enumerate([0.1, 0.25, 0.5, 0.75, 1.0][::-1]):
            # Narrower segments toward the center
            width_factor = self.thickness * (0.6 + 0.1 * i)
            offset = i * 0.02
            tail = center - pulse_width / 2 + offset
            head = center + pulse_width / 2 - offset
            # clamp within 0..1
            tail = max(0.0, tail)
            head = min(1.0, head)
            if head > tail:
                pen.setColor(QColor(self.bar_color.red(),
                                    self.bar_color.green(),
                                    self.bar_color.blue(),
                                    int(alpha * 255)))
                pen.setWidth(int(width_factor))
                painter.setPen(pen)
                painter.drawLine(int(x0 + tail * L), h // 2, int(x0 + head * L), h // 2)

        painter.end()

