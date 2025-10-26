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
    TRACK_Y,
    CAP_OFFSET,
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

        self.setFixedHeight(TRACK_THICKNESS)
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
        track_x0 = CAP_OFFSET
        track_x1 = float(self.width() - CAP_OFFSET)
        track_length = track_x1 - track_x0

        track_x = CAP_OFFSET + int(self._progress * track_length / 100)

        pen = QPen()
        pen.setWidth(TRACK_THICKNESS)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setColor(self.active_color)
        painter.setPen(pen)

        # Active
        painter.drawLine(track_x0, TRACK_Y, track_x, TRACK_Y)

        # Inactive
        x = (track_x + CAP_OFFSET) + (4 + CAP_OFFSET)
        if x < track_x1:
            pen.setColor(self.track_color)
            painter.setPen(pen)
            painter.drawLine(
                x,
                TRACK_Y,
                track_x1 - int(TRACK_THICKNESS/2),
                TRACK_Y
            )

        pen.setWidth(TRACK_THICKNESS)
        pen.setColor(self.active_color)
        painter.setPen(pen)
        painter.drawPoint(QPoint(track_x1, TRACK_Y))
        painter.drawPoint(QPoint(track_x0, TRACK_Y))

        painter.end()


