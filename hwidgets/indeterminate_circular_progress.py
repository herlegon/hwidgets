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
    TRACK_MARGIN,
    TRACK_POSITION_Y,
    TRACK_START_X,
    TRACK_THICKNESS,
)






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



class IndeterminateCircularProgress(QProgressBar):
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
