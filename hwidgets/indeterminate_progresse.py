import math
import time
from typing import Final
from PySide6.QtCore import (
    QEasingCurve,
    Qt,
    QPropertyAnimation,
    Property,
    QParallelAnimationGroup,
    QSequentialAnimationGroup,
    QPoint,
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

from .hstyle import (
    HStyle,
    TRACK_MARGIN,
    TRACK_POSITION_Y,
    TRACK_START_X,
    TRACK_THICKNESS,
)


class HIndeterminateProgress(QProgressBar):
    """A linear progress bar from 0 to 100
    """

    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        hstyle: HStyle,
        is_m2: bool = False,
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
        super().__init__(parent)
        # self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self._progress = 0

        self.hstyle = hstyle
        is_m2 = True

        self.setFixedHeight(4)
        self.setFixedWidth(240+16*2)
        self.track_color = QColor(hstyle.widget_bgd)
        self.active_color = QColor("green")
        self.setMinimum(0)
        self.setMaximum(1.0)
        self.setValue(0)

        self._flh: float = 0.
        self._flt: float = 0.
        self._slh: float = 0.
        self._slt: float = 0.

        LinearAnimationDuration = 1800

        if is_m2:
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

            speed_r = 1
            last_pause = 435 * speed_r
            last_pause = 0
        else:

            FirstLineHeadDelay = 0
            FirstLineTailDelay = 120
            SecondLineHeadDelay = 635
            SecondLineTailDelay = 870

            # web
            speed_r = 1
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
        self.animations.setLoopCount(1)
        self.animations.start()


        self.animations.finished.connect(self.animations_finished)

    def animations_finished(self):
        self._flh = 0.
        self._flt = 0.
        self._slh = 0.
        self._slt = 0.
        # self.animation_flh.setCurrentTime(0)
        # self.animation_flt.setCurrentTime(0)
        # self.animation_slh.setCurrentTime(0)
        # self.animation_slt.setCurrentTime(0)
        self.animations.start()

    # def timerEvent(self, event: QTimerEvent) -> None:
    #     self.animations[self.timer_no].stop()
    #     self.timer_no = (self.timer_no + 1) % 4
    #     animation = self.animations[self.timer_no]
    #     animation.setEndValue(1.)
    #     animation.start()
    #     msec = self.timer_start + self.timings[self.timer_no] - int(time.time() * 1000)
    #     print(f"start animation no. {self.timer_no}, {msec}ms")
    #     self.timer.start(msec, self)


    def stop(self) -> bool:
        animation: QPropertyAnimation
        for animation in self.animations:
            animation.stop()
        self.setValue(0)


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






    def drawLinearIndicator(self,
        painter: QPainter,
        pen: QPen,
        startFraction: float,
        endFraction: float,
    ):
        track_length = float(self.width() - (2 * TRACK_MARGIN + TRACK_THICKNESS))
        barStart = int(startFraction * track_length + TRACK_START_X)
        barEnd = int(endFraction * track_length + TRACK_START_X)

        if abs(endFraction - startFraction) > 0:
            if True:
                if self.timer_start == 0: self.timer_start = int(time.time() * 1000)
            #     # print(f"{int(time.time()*1000) - self.timer_start}: {self.flh:.03f}\t{self.flt:.03f}\t{self.slh:.03f}\t{self.slt:.03f}")
                print(f"{int(time.time()*1000) - self.timer_start}: ({startFraction:.02f}, {endFraction:.02f}){barStart} ({abs(barEnd - barStart)})")

            pen.setColor(QColor("red"))
            painter.setPen(pen)
            painter.drawLine(
                barStart, TRACK_POSITION_Y,
                barEnd, TRACK_POSITION_Y
            )

            if barEnd >= TRACK_MARGIN + TRACK_THICKNESS + TRACK_START_X:
                track_end = barEnd - (TRACK_MARGIN + TRACK_THICKNESS)
                track_start = TRACK_START_X
                pen.setColor(QColor(self.hstyle.widget_bgd))
                painter.setPen(pen)
                painter.drawLine(
                    track_start, TRACK_POSITION_Y,
                    track_end, TRACK_POSITION_Y
                )

            if barStart < track_length:
                track_start = barStart + TRACK_MARGIN + TRACK_THICKNESS
                track_end = track_length
                pen.setColor(QColor(self.hstyle.widget_bgd))
                painter.setPen(pen)
                painter.drawLine(
                    track_start, TRACK_POSITION_Y,
                    track_end, TRACK_POSITION_Y
                )




    # https://androidx.tech/artifacts/compose.material3/material3/1.0.0-beta02-source/androidx/compose/material3/ProgressIndicator.kt.html
    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        track_length = float(self.width() - (2 * TRACK_MARGIN + TRACK_THICKNESS))
        # progress = self._progress
        # progress -= 100 if self._progress >= 100 else 0

        # current_position = int(progress * track_length / 100)
        # print(f"{progress} -> {current_position}")
        if False:
            if self.timer_start == 0: self.timer_start = int(time.time() * 1000)
            # print(f"{int(time.time()*1000) - self.timer_start}: {self.flh:.03f}\t{self.flt:.03f}\t{self.slh:.03f}\t{self.slt:.03f}")
            print(f"{int(time.time()*1000) - self.timer_start}: {self.flh-self.flt:.03f}\t{self.slh-self.slt:.03f}")

        pen = QPen()
        pen.setWidth(TRACK_THICKNESS)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        # pen.setColor(QColor('grey'))
        # painter.setPen(pen)
        # painter.drawLine(
        #     TRACK_START_X,
        #     TRACK_POSITION_Y,
        #     self.width() - TRACK_START_X,
        #     TRACK_POSITION_Y
        # )

        pen.setWidth(TRACK_THICKNESS)


        x0 = int(self.flh * track_length + TRACK_START_X)
        x1 = int(self.flt * track_length + TRACK_START_X)
        x2 = int(self.slh * track_length + TRACK_START_X)
        x3 = int(self.slt * track_length + TRACK_START_X)



        if all([x == 0 or x == 1  for x in [self.flh, self.flt, self.slh, self.slt]]):
            pen.setColor(self.track_color)
            painter.setPen(pen)
            painter.drawLine(TRACK_START_X, TRACK_POSITION_Y, TRACK_START_X + track_length, TRACK_POSITION_Y)

        else:
            pen.setColor(self.active_color)
            painter.setPen(pen)
            if x0 - x1 > 0:
                painter.drawLine(x1, TRACK_POSITION_Y, x0, TRACK_POSITION_Y)
            if x2 - x3 > 0:
                painter.drawLine(x2, TRACK_POSITION_Y, x3, TRACK_POSITION_Y)
            pen.setColor(QColor(self.hstyle.widget_bgd))
            painter.setPen(pen)


            if x2 <= TRACK_START_X:
                # tail
                track_start = TRACK_START_X
                track_end = max(TRACK_START_X, x1 - TRACK_MARGIN - TRACK_THICKNESS)
                # print(f"tail: ({x0}, {x1}) {track_start} -> {track_end} ({track_end - track_start})")
                if track_end - track_start:
                    # print(f"\tpaint {track_start} -> {track_end}")
                    painter.drawLine(track_start, TRACK_POSITION_Y, track_end, TRACK_POSITION_Y)
                # if x1 - TRACK_MARGIN - TRACK_THICKNESS == TRACK_START_X:
                #     painter.drawLine(track_start - TRACK_THICKNESS, TRACK_POSITION_Y, track_end, TRACK_POSITION_Y)

                if False:
                    if self.timer_start == 0: self.timer_start = int(time.time() * 1000)
                    # print(f"{int(time.time()*1000) - self.timer_start}: {self.flh:.03f}\t{self.flt:.03f}\t{self.slh:.03f}\t{self.slt:.03f}")
                    print(f"{int(time.time()*1000) - self.timer_start}: ({x1} -> {x0}) {track_start} -> {track_end}")

                track_start = x0 + TRACK_MARGIN + TRACK_THICKNESS
                track_end = TRACK_START_X + track_length
                if track_end > track_start:
                    painter.drawLine(track_start, TRACK_POSITION_Y, track_end, TRACK_POSITION_Y)


                # elif track_end - track_start - TRACK_THICKNESS / 2> 0:
                #     painter.drawLine(track_start - TRACK_THICKNESS / 2, TRACK_POSITION_Y, track_end, TRACK_POSITION_Y)
                # # head
                # track_start = x0 + (TRACK_MARGIN + TRACK_THICKNESS)
                # track_end = track_length + TRACK_START_X
                # if track_end > track_start:
                #     painter.drawLine(track_start, TRACK_POSITION_Y, track_end, TRACK_POSITION_Y)

            else:
                # 2nd

                # tail
                track_start = TRACK_START_X
                track_end = max(TRACK_START_X, x3 - TRACK_MARGIN - TRACK_THICKNESS)
                if track_end - track_start >= 0:
                    painter.drawLine(track_start, TRACK_POSITION_Y, track_end, TRACK_POSITION_Y)

                track_start = x2 + TRACK_MARGIN + TRACK_THICKNESS
                track_end = min(x1 - (TRACK_MARGIN + TRACK_THICKNESS), TRACK_START_X + track_length)
                if track_end > track_start:
                    painter.drawLine(track_start, TRACK_POSITION_Y, track_end, TRACK_POSITION_Y)



            # # track_start = max(x3, TRACK_START_X)
            # # track_end = min(x1, TRACK_START_X + track_length)
            # # painter.drawLine(track_start, TRACK_POSITION_Y, track_end, TRACK_POSITION_Y)
            # if x2 >= TRACK_START_X:
            #     track_start = max(x2, TRACK_START_X) + TRACK_MARGIN + TRACK_THICKNESS
            #     track_end = min(x1, track_length + TRACK_START_X)
            # else:
            #     track_start = max(x0, TRACK_START_X) + TRACK_MARGIN + TRACK_THICKNESS
            #     track_end = track_length + TRACK_START_X

            # if track_end > track_start and x3 > TRACK_START_X:
            #     painter.drawLine(track_start, TRACK_POSITION_Y, track_end, TRACK_POSITION_Y)

                if False:
                    if self.timer_start == 0: self.timer_start = int(time.time() * 1000)
                    # print(f"{int(time.time()*1000) - self.timer_start}: {self.flh:.03f}\t{self.flt:.03f}\t{self.slh:.03f}\t{self.slt:.03f}")
                    print(f"{int(time.time()*1000) - self.timer_start}: ({track_length}) {track_start} -> {track_end}")

            # if x3 > TRACK_START_X:
            #     track_start = TRACK_START_X
            #     track_end = max(x2 - (TRACK_MARGIN + TRACK_THICKNESS), track_length + TRACK_START_X)
            # else:
            #     track_start = TRACK_START_X
            #     track_end = x1 - (TRACK_START_X + TRACK_MARGIN)

            # if track_end > track_start:
            #     painter.drawLine(track_start, TRACK_POSITION_Y, track_end, TRACK_POSITION_Y)

        # pen = QPen()
        # pen.setWidth(TRACK_THICKNESS)
        # pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        # pen.setColor(self.active_color)
        # painter.setPen(pen)
        # painter.drawLine(
        #     TRACK_START_X,
        #     TRACK_POSITION_Y,
        #     TRACK_START_X + current_position,
        #     TRACK_POSITION_Y
        # )

        painter.end()




