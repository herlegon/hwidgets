from pprint import pprint
from typing import Type

from .hstyle import (
    DEBUG_GEOMETRY,
    draw_widget_rect,
)
from .style_manager import Theme

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



class HProgressBar(QProgressBar):
    """A linear progress bar from 0 to 100
    """
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

        self.m3: bool = m3

        self.thickness = theme.progress_bar.thickness
        self.setFixedHeight(self.thickness)
        self.setMinimumWidth(self.thickness*4)

        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.set_colors(
            track=theme.progress_bar.track,
            bar=theme.progress_bar.bar,
        )

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
        if DEBUG_GEOMETRY:
            draw_widget_rect(self, painter)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        thickness = self.thickness
        cap_offset: int = self.thickness // 2
        track_y: int = self.thickness // 2

        track_x0 = cap_offset
        track_x1 = float(self.width() - cap_offset)
        track_length = track_x1 - track_x0

        track_x = cap_offset + int(self._progress * track_length / 100)

        pen = QPen()
        pen.setWidth(thickness)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        # Inactive: not M3
        if not self.m3:
            pen.setColor(self.track_color)
            painter.setPen(pen)
            painter.drawLine(track_x0, track_y, track_x1, track_y)

        # Active
        pen.setColor(self.bar_color)
        painter.setPen(pen)
        painter.drawLine(track_x0, track_y, track_x, track_y)

        # Inactive: M3
        if self.m3:
            x = (track_x + cap_offset) + (4 + cap_offset)
            if x < track_x1:
                pen.setColor(self.track_color)
                painter.setPen(pen)
                painter.drawLine(
                    x, track_y, track_x1 - int(thickness/2), track_y
                )

        pen.setWidth(thickness)
        pen.setColor(self.bar_color)
        painter.setPen(pen)
        if self.m3:
            painter.drawPoint(QPoint(track_x1, track_y))
            painter.drawPoint(QPoint(track_x0, track_y))

        painter.end()



class HProgressBarM3(HProgressBar):
    """A linear progress bar from 0 to 100
    """
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
            parent,
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
