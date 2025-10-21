import math
import time
from typing import Final, Optional
from PySide6.QtCore import (
    QEasingCurve,
    QTimerEvent,
    Qt,
    QPropertyAnimation,
    Property,
    QParallelAnimationGroup,
    QSequentialAnimationGroup,
    QPoint,
    QPointF,
    QBasicTimer,
    QRect,

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


TRACK_THICKNESS: Final[int] = 4
TRACK_MARGIN: Final[int] = 4
TRACK_POSITION_Y: Final[int] = int(TRACK_THICKNESS/2)
TRACK_START_X: Final[int] = int(TRACK_MARGIN + TRACK_THICKNESS/2)






# Indeterminate linear indicator transition specs

# Total duration for one cycle
LinearAnimationDuration = 1800

# Duration of the head and tail animations for both lines
FirstLineHeadDuration = 750
FirstLineTailDuration = 850
SecondLineHeadDuration = 567
SecondLineTailDuration = 533

# Delay before the start of the head and tail animations for both lines
FirstLineHeadDelay = 0
FirstLineTailDelay = 333
SecondLineHeadDelay = 1000
SecondLineTailDelay = 1267

# FirstLineHeadEasing = CubicBezierEasing(0.2, 0, 0.8, 1)
# FirstLineTailEasing = CubicBezierEasing(0.4, 0, 1, 1)
# SecondLineHeadEasing = CubicBezierEasing(0, 0, 0.65, 1)
# SecondLineTailEasing = CubicBezierEasing(0.1, 0, 0.45, 1)

FirstLineHeadEasing = ((0.2, 0), (0.8, 1))
FirstLineTailEasing = ((0.4, 0), (1, 1))
SecondLineHeadEasing = ((0, 0), (0.65, 1))
SecondLineTailEasing = ((0.1, 0), (0.45, 1))




class ProgressIndicator(QProgressBar):
    """A linear progress bar from 0 to 100
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self._progress = 0

        self.setFixedHeight(4)
        self.set_colors('green', 'red')

        self.animation = QPropertyAnimation(self, b'progress', self)
        self.animation.setDuration(200)

        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)
        self.valueChanged.connect(self.value_changed)


    @Property(int)
    def progress(self) -> int:
        return self._progress


    @progress.setter
    def progress(self, value: int) -> None:
        self._progress = value
        self.repaint()


    def value_changed(self, value: int) -> None:
        self.animation.stop()
        self.animation.setEndValue(value)
        self.animation.start()
        super().setValue(value)


    def set_colors(self, track: str, active: str) -> None:
        self.track_color = QColor(track)
        self.active_color = QColor(active)


    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        track_length = self.width() - (2 * TRACK_MARGIN + TRACK_THICKNESS)
        current_position = int(self._progress * track_length / 100)

        pen = QPen()
        pen.setWidth(TRACK_THICKNESS)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setColor(self.active_color)
        painter.setPen(pen)
        painter.drawLine(
            TRACK_START_X,
            TRACK_POSITION_Y,
            TRACK_START_X + current_position,
            TRACK_POSITION_Y
        )

        x = current_position + 2 * TRACK_MARGIN + int(3*TRACK_THICKNESS/2)
        track_stop_point_x = self.width() - TRACK_START_X
        if x < track_stop_point_x:
            pen.setColor(self.track_color)
            painter.setPen(pen)
            if current_position == 0: x = TRACK_START_X
            painter.drawLine(
                x,
                TRACK_POSITION_Y,
                track_stop_point_x - int(TRACK_THICKNESS/2),
                TRACK_POSITION_Y
            )

        pen.setWidth(TRACK_THICKNESS)
        pen.setColor(self.active_color)
        painter.setPen(pen)
        painter.drawPoint(QPoint(track_stop_point_x, TRACK_POSITION_Y))

        painter.end()




class IndeterminateProgressIndicator(QProgressBar):
    """A linear progress bar from 0 to 100
    """

    def __init__(self, parent: QWidget, is_m2: bool = False):
        super().__init__(parent)
        # self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self._progress = 0

        self.setFixedHeight(4)
        self.setFixedWidth(240+16*2)
        self.set_colors('green', 'red')
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


    def set_colors(self, track: str, active: str) -> None:
        self.track_color = QColor(track)
        self.active_color = QColor(active)



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

            pen.setColor(QColor(80,240,80))
            painter.setPen(pen)
            painter.drawLine(
                barStart, TRACK_POSITION_Y,
                barEnd, TRACK_POSITION_Y
            )

            if barEnd >= TRACK_MARGIN + TRACK_THICKNESS + TRACK_START_X:
                track_end = barEnd - (TRACK_MARGIN + TRACK_THICKNESS)
                track_start = TRACK_START_X
                pen.setColor(QColor('grey'))
                painter.setPen(pen)
                painter.drawLine(
                    track_start, TRACK_POSITION_Y,
                    track_end, TRACK_POSITION_Y
                )

            if barStart < track_length:
                track_start = barStart + TRACK_MARGIN + TRACK_THICKNESS
                track_end = track_length
                pen.setColor(QColor('grey'))
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
            pen.setColor(QColor('grey'))
            painter.setPen(pen)
            painter.drawLine(TRACK_START_X, TRACK_POSITION_Y, TRACK_START_X + track_length, TRACK_POSITION_Y)

        else:
            pen.setColor(QColor(80,240,80))
            painter.setPen(pen)
            if x0 - x1 > 0:
                painter.drawLine(x1, TRACK_POSITION_Y, x0, TRACK_POSITION_Y)
            if x2 - x3 > 0:
                painter.drawLine(x2, TRACK_POSITION_Y, x3, TRACK_POSITION_Y)
            pen.setColor(QColor('grey'))
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





# internal object CircularProgressIndicatorTokens {
#     val ActiveIndicatorColor = ColorSchemeKeyTokens.Primary
#     val ActiveShape = ShapeKeyTokens.CornerNone
#     val ActiveIndicatorWidth = 4.0.dp
#     val FourColorActiveIndicatorFourColor = ColorSchemeKeyTokens.TertiaryContainer
#     val FourColorActiveIndicatorOneColor = ColorSchemeKeyTokens.Primary
#     val FourColorActiveIndicatorThreeColor = ColorSchemeKeyTokens.Tertiary
#     val FourColorActiveIndicatorTwoColor = ColorSchemeKeyTokens.PrimaryContainer
#     val Size = 48.0.dp
# }

# Indeterminate circular indicator transition specs
# CircularProgressIndicator Material specs
# Diameter of the indicator circle
CircularProgressIndicatorTokens_Size = 48
CircularProgressIndicatorTokens_ActiveIndicatorWidth = 4
CircularIndicatorDiameter = CircularProgressIndicatorTokens_Size - CircularProgressIndicatorTokens_ActiveIndicatorWidth * 2

# The animation comprises of 5 rotations around the circle forming a 5 pointed star.
# After the 5th rotation, we are back at the beginning of the circle.
RotationsPerCycle = 5

# Each rotation is 1 and 1/3 seconds, but 1332ms divides more evenly
RotationDuration = 1332

# When the rotation is at its beginning (0 or 360 degrees) we want it to be drawn at 12 o clock,
# which means 270 degrees when drawing.
StartAngleOffset = -90

# How far the base point moves around the circle
BaseRotationAngle = 286

# How far the head and tail should jump forward during one rotation past the base point
JumpRotationAngle = 290

# Each rotation we want to offset the start position by this much, so we continue where
# the previous rotation ended. This is the maximum angle covered during one rotation.
RotationAngleOffset = (BaseRotationAngle + JumpRotationAngle) % 360

# The head animates for the first half of a rotation, then is static for the second half
# The tail is static for the first half and then animates for the second half
HeadAndTailAnimationDuration = int(RotationDuration * 0.5)
HeadAndTailDelayDuration = HeadAndTailAnimationDuration

# The easing for the head and tail jump
CircularEasing = ((0.4, 0), (0.2, 1))



stroke_width = 4
size_width = 4



class IndeterminateCircularProgressIndicator(QProgressBar):
    """A circular progress bar from 0 to 100
    """

    def __init__(self, parent: QWidget, is_m2: bool = False):
        super().__init__(parent)
        # self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self._progress = 0

        self.setFixedHeight(4)
        self.setFixedWidth(240+16*2)
        self.set_colors('green', 'red')
        self.setMinimum(0)
        self.setMaximum(1.0)
        self.setValue(0)

        self._startAngle = StartAngleOffset
        self._endAngle = 0
        self._baseRotation = BaseRotationAngle
        self._currentRotation = 0


    def set_colors(self, track: str, active: str) -> None:
        self.track_color = QColor(track)
        self.active_color = QColor(active)



    @Property(float)
    def startAngle(self) -> float:
        return self._startAngle

    @startAngle.setter
    def startAngle(self, value: float) -> None:
        self._startAngle = value
        self.repaint()

    @Property(float)
    def endAngle(self) -> float:
        return self._endAngle

    @endAngle.setter
    def endAngle(self, value: float) -> None:
        self._endAngle = value
        self.repaint()

    @Property(float)
    def baseRotation(self) -> float:
        return self._baseRotation

    @baseRotation.setter
    def baseRotation(self, value: float) -> None:
        self._baseRotation = value
        self.repaint()

    @Property(float)
    def currentRotation(self) -> float:
        return self._currentRotation

    @currentRotation.setter
    def currentRotation(self, value: float) -> None:
        self._currentRotation = value
        self.repaint()


    def drawCircularIndicator(self,
        painter: QPainter,
        startAngle: float,
        sweep: float,
    ):
        # To draw this circle we need a rect with edges that line up with the midpoint of the stroke.
        # To do this we need to remove half the stroke width from the total diameter for both sides.
        diameterOffset = stroke_width / 2
        arcDimen = self.width() - 2 * diameterOffset
        painter.drawArc(
            diameterOffset, diameterOffset,arcDimen,arcDimen,
            startAngle,
            sweep,
        )
        # painter.drawArc(
        #     startAngle = startAngle,
        #     sweepAngle = sweep,
        #     useCenter = False,
        #     topLeft = Offset(diameterOffset, diameterOffset),
        #     size = Size(arcDimen, arcDimen),
        # )


    def drawIndeterminateCircularIndicator(self,
        startAngle: float,
        sweep: float,
    ):
        # Length of arc is angle * radius
        # Angle (radians) is length / radius
        # The length should be the same as the stroke width for calculating the min angle
        strokeCapOffset = float(180.0 / math.pi) * (TRACK_THICKNESS / (CircularIndicatorDiameter / 2.)) / 2.


        # Adding a stroke cap draws half the stroke width behind the start point, so we want to
        # move it forward by that amount so the arc visually appears in the correct place
        adjustedStartAngle = startAngle + strokeCapOffset

        # When the start and end angles are in the same place, we still want to draw a small sweep, so
        # the stroke caps get added on both ends and we draw the correct minimum length arc
        adjustedSweep = max(sweep, 0.1)

        self.drawCircularIndicator(adjustedStartAngle, adjustedSweep)



    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)


        pen = QPen()
        pen.setWidth(TRACK_THICKNESS)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setWidth(TRACK_THICKNESS)

        pen.setColor(QColor(80,240,80))
        painter.setPen(pen)

        # self.drawCircularIndicatorTrack(trackColor, stroke)

        currentRotationAngleOffset = (self.currentRotation * RotationAngleOffset) % 360

        # How long a line to draw using the start angle as a reference point
        sweep = abs(self.endAngle - self.startAngle)

        # Offset by the constant offset and the per rotation offset
        offset = StartAngleOffset + currentRotationAngleOffset + self.baseRotation
        self.drawIndeterminateCircularIndicator(
            self.startAngle + offset,
            sweep,
        )


        painter.end()
