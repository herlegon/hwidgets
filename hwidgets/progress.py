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
    HStyle,
)


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




class HProgress(QProgressBar):
    """A linear progress bar from 0 to 100
    """
    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        hstyle: HStyle,
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
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self._progress = 0

        self.setFixedHeight(4)
        self.set_colors(
            hstyle.widget_bgd,
            hstyle.selected
        )

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


