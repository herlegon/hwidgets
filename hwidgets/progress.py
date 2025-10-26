from .hstyle import (
    HStyle,
    TRACK_Y,
    CAP_OFFSET,
    TRACK_THICKNESS,
)

from PySide6.QtCore import (
    Qt,
    QPropertyAnimation,
    Property,
    QPoint,
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

        self.setFixedHeight(TRACK_THICKNESS)

        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.set_colors(track=hstyle.widget_bgd, bar=hstyle.selected)

        self._progress = 0
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)

        self.animation = QPropertyAnimation(self, b'progress', self)
        self.animation.setDuration(200)

        self.valueChanged.connect(self.value_changed)


    def set_colors(self, track: str, bar: str) -> None:
        self.track_color: QColor = QColor(track)
        self.bar_color: QColor = QColor(bar)


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
        pen.setColor(self.bar_color)
        painter.setPen(pen)

        # Active
        painter.drawLine(track_x0, TRACK_Y, track_x, TRACK_Y)

        # Inactive
        x = (track_x + CAP_OFFSET) + (4 + CAP_OFFSET)
        if x < track_x1:
            pen.setColor(self.track_color)
            painter.setPen(pen)
            painter.drawLine(
                x, TRACK_Y, track_x1 - int(TRACK_THICKNESS/2), TRACK_Y
            )

        pen.setWidth(TRACK_THICKNESS)
        pen.setColor(self.bar_color)
        painter.setPen(pen)
        painter.drawPoint(QPoint(track_x1, TRACK_Y))
        painter.drawPoint(QPoint(track_x0, TRACK_Y))

        painter.end()


