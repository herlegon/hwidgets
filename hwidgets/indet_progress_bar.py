from typing import Type
from .style_manager import Theme
from .hstyle import (
    DEBUG_GEOMETRY,
    draw_widget_rect,
)

from PySide6.QtCore import (
    QEasingCurve,
    Qt,
    QPropertyAnimation,
    Property,
    QParallelAnimationGroup,
    QSequentialAnimationGroup,
    QPointF,
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

        self.set_colors(
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

        speed_r = 1.5
        last_pause = 435 * speed_r
        last_pause = 0


        if not m3:
            print("M2")
            # Duration of the head and tail animations for both lines
            # M2
            FirstLineHeadDuration = 750
            FirstLineTailDuration = 850
            SecondLineHeadDuration = 567
            SecondLineTailDuration = 533

            # Delay before the start of the head and tail animations for both lines
            FirstLineHeadDelay = 0
            FirstLineTailDelay = 333
            SecondLineHeadDelay = 1000
            SecondLineTailDelay = 1267

            FirstLineHeadEasing = ((0.5, 0), (0.9, 1))
            FirstLineTailEasing = ((0.4, 0), (1, 1))
            SecondLineHeadEasing = ((0, 0), (0.65, 1))
            SecondLineTailEasing = ((0.1, 0), (0.45, 1))
        else:
            print("M2")

            FirstLineHeadDelay = 0
            FirstLineTailDelay = 120
            SecondLineHeadDelay = 635
            SecondLineTailDelay = 870

            slow_factor = 1
            FirstLineHeadDelay  = slow_factor * FirstLineHeadDelay
            FirstLineTailDelay  = slow_factor * FirstLineTailDelay
            SecondLineHeadDelay = slow_factor * SecondLineHeadDelay
            SecondLineTailDelay = slow_factor * SecondLineTailDelay

            # web
            FirstLineHeadDelay  = ( 280 -280) * speed_r
            FirstLineTailDelay  = ( 400 -280) * speed_r
            SecondLineHeadDelay = ( 900 -280) * speed_r
            SecondLineTailDelay = (1150 -280) * speed_r
            last_pause = 435 * speed_r
            last_pause = 0


            FirstLineHeadDuration =  675 * speed_r
            FirstLineTailDuration =  715 * speed_r
            SecondLineHeadDuration = 515 * speed_r
            SecondLineTailDuration = 515 * speed_r

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
        self.animation_flh.setDuration(FirstLineHeadDuration)
        self.animation_flh.setEasingCurve(curve_flh)
        self.animation_flh.setStartValue(0.)
        self.animation_flh.setEndValue(1.)
        self.animation_flh_group = QSequentialAnimationGroup(self)
        self.animation_flh_group.addPause(FirstLineHeadDelay)
        self.animation_flh_group.addAnimation(self.animation_flh)

        self.animation_flt = QPropertyAnimation(self, b'flt', self)
        self.animation_flt.setDuration(FirstLineTailDuration)
        self.animation_flt.setEasingCurve(curve_flt)
        self.animation_flt.setStartValue(0.)
        self.animation_flt.setEndValue(1.)
        self.animation_flt_group = QSequentialAnimationGroup(self)
        self.animation_flt_group.addPause(FirstLineTailDelay)
        self.animation_flt_group.addAnimation(self.animation_flt)

        self.animation_slh = QPropertyAnimation(self, b'slh', self)
        self.animation_slh.setDuration(SecondLineHeadDuration)
        self.animation_slh.setEasingCurve(curve_slh)
        self.animation_slh.setStartValue(0.)
        self.animation_slh.setEndValue(1.)
        self.animation_slh_group = QSequentialAnimationGroup(self)
        self.animation_slh_group.addPause(SecondLineHeadDelay)
        self.animation_slh_group.addAnimation(self.animation_slh)

        self.animation_slt = QPropertyAnimation(self, b'slt', self)
        self.animation_slt.setDuration(SecondLineTailDuration)
        self.animation_slt.setEasingCurve(curve_slt)
        self.animation_slt.setStartValue(0.)
        self.animation_slt.setEndValue(1.)
        self.animation_slt_group = QSequentialAnimationGroup(self)
        self.animation_slt_group.addPause(SecondLineTailDelay)
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


    def set_colors(self, track: str, bar: str) -> None:
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


    # https://github.com/droiddevtips/droiddevtipsExample/blob/main/masteringcomposetheme/src/main/java/com/droiddevtips/masteringcomposetheme/feature/progress/ui/Material3Progress.kt
    # https://androidx.tech/artifacts/compose.material3/material3/1.0.0-beta02-source/androidx/compose/material3/ProgressIndicator.kt.html
    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        if DEBUG_GEOMETRY:
            draw_widget_rect(self, painter)

        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        thickness = self.thickness
        cap_offset: int = self.thickness // 2
        track_y: int = self.thickness // 2

        # track is widget width - 2 x margin - 2 x track thickness for rounded cap
        track_x0 = cap_offset
        track_x1 = float(self.width() - cap_offset)
        track_length = track_x1 - track_x0

        # For debug
        # pen = QPen()
        # pen.setWidth(2)
        # pen.setCapStyle(Qt.PenCapStyle.SquareCap)
        # pen.setColor(QColor("#ffffff"))
        # painter.setPen(pen)
        # painter.drawLine(0, 0, self.width(), 0)

        x_h1 = int(track_x0 + self.flh * track_length)
        x_t1 = int(track_x0 + self.flt * track_length)
        x_h2 = int(track_x0 + self.slh * track_length)
        x_t2 = int(track_x0 + self.slt * track_length)

        pen = QPen()
        pen.setWidth(thickness)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        # Track
        pen.setColor(self.track_color)
        painter.setPen(pen)
        painter.drawLine(track_x0, track_y, track_x1, track_y)

        # Progress bars
        if not all([x in (0, 1)  for x in [self.flh, self.flt, self.slh, self.slt]]):
            pen.setColor(self.bar_color)
            painter.setPen(pen)

            # 1st progress bar
            track_start = track_x0 + x_h1
            if track_start < track_x1:
                painter.drawLine(track_start, track_y, track_x1, track_y)

            if x_h2 <= track_x0:
                # Before progress2 is moving
                progress2_x0 = track_x0
                progress2_x1 = max(track_x0, x_t1  - track_x0)
                if progress2_x1 - progress2_x0:
                    painter.drawLine(progress2_x0, track_y, progress2_x1, track_y)

            else:
                # Progress 2 is moving
                progress2_x0 = track_x0
                progress2_x1 = max(track_x0, x_t2)
                if progress2_x1 - progress2_x0 >= 0:
                    painter.drawLine(progress2_x0, track_y, progress2_x1, track_y)

                progress2_x0 = x_h2
                progress2_x1 = min(x_t1, track_x1)
                if progress2_x1 > progress2_x0:
                    painter.drawLine(progress2_x0, track_y, progress2_x1, track_y)

        else:
            pen.setColor(self.bar_color)
            painter.setPen(pen)
            painter.drawLine(track_x0, track_y, track_x1, track_y)

        painter.end()




class HIndetProgressBarM3(HIndetProgressBar):

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
    ):
        super().__init__(
            parent=parent,
            theme=theme,
            minimum=minimum,
            maximum=maximum,
            text=text,
            value=value,
            alignment=alignment,
            textVisible=textVisible,
            orientation=orientation,
            invertedAppearance=invertedAppearance,
            textDirection=textDirection,
            format=format,
            m3=True
        )
        print("PROGRESS BATR M3")

