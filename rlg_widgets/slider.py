import time
from PySide6.QtCore import (
    Qt,
    QPoint,
    QEvent,
    QObject,
    QRect,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QMouseEvent,
    QMoveEvent,
    QPaintEvent,
    QPainter,
    QPen,
    QResizeEvent,
    QEnterEvent,
)
from PySide6.QtWidgets import (
    QSlider,
    QGraphicsSceneHoverEvent,
    QWidget,
    QSizePolicy,
)
from .utils import (
    dp_to_px
)

factor = 1.5
SLIDER_TRACK_THICKNESS = 2 * int(16 / (2 * factor * dp_to_px))
SLIDER_HANDLE_MARGIN = 2 * int(6 / (2*factor))
SLIDER_HANDLE_HEIGHT = 2 * int(44 / (2* dp_to_px))
SLIDER_HANDLE_THICKNESS = 4
SLIDER_HANDLE_MARGIN = 6


class Slider(QSlider):
    # TODO:
    # - set color style
    # - clean
    # - Add vertical slider
    # - Add intermediary ticks
    # - Add minimum and maximum value
    FACTOR: int = 1000

    # Replace valueChanged by sliderValueChanged
    sliderValueChanged = Signal(float)

    def __init__(self, parent: QWidget, background_color: str) -> None:
        # Background color is used to fasten drawing
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        # self.setCursor(Qt.CursorShape.ArrowCursor)

        self.handle_color = QColor(0,0,255)
        self.bgd_color = QColor(background_color)
        self.track_color_l = QColor(150,80,80)
        self.track_color_r = QColor(80,80,150)
        self.tick_color = QColor(240,240,240)

        self.range: float = 100
        self.setMinimum(-100)
        self.setMaximum(100)
        self.setValue(0)
        self.setSingleStep(1)
        self.setPageStep(10)

        self.handle_position = 0
        self.track_length: int = 2 * SLIDER_HANDLE_THICKNESS
        self.track_width: int = self.track_length - SLIDER_HANDLE_THICKNESS
        self.setTrackWidth(self.track_length)
        self.x0: int = 0
        self._calculate_origin()

        self.is_moving: bool = False

        self.handle_position = self.value_to_position(self.value())
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )
        self.setFixedHeight(SLIDER_HANDLE_HEIGHT)
        self.track_position = int(SLIDER_HANDLE_HEIGHT/2)

        self.valueChanged.connect(self.value_changed)
        self.setTrackWidth(self.width())
        # self.installEventFilter(self)


    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        return


    def enterEvent(self, event: QEnterEvent) -> None:
        return


    def minimum(self) -> float:
        return super().minimum() / self.FACTOR


    def maximum(self) -> float:
        return super().maximum() / self.FACTOR


    def setMaximum(self, value: int | float) -> None:
        super().setMaximum(value * self.FACTOR)
        self.range = self.maximum() - self.minimum()


    def setMinimum(self, value: int | float) -> None:
        super().setMinimum(value * self.FACTOR)
        self.range = self.maximum() - self.minimum()


    def setValue(self, value: int | float) -> None:
        super().setValue(value * self.FACTOR)
        self.sliderValueChanged.emit(self.value())


    def setSingleStep(self, step: int | float) -> None:
        super().setSingleStep(int(step * self.FACTOR))


    def setPageStep(self, step: int | float) -> None:
        super().setPageStep(int(step * self.FACTOR))


    def value(self) -> float:
        return super().value() / self.FACTOR


    def mousePressEvent(self, event: QMouseEvent):
        cursor = event.pos().x() - self.x0 + int(SLIDER_HANDLE_THICKNESS/2)
        if cursor < 0:
            value = self.minimum()
            self.handle_position = self.value_to_position(value)
            self.is_moving = False
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        elif cursor > self.track_width:
            value = self.maximum()
            self.handle_position = self.value_to_position(value)
            self.is_moving = False
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            value = self.position_to_value(cursor)
            self.handle_position = cursor
            self.is_moving = True
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        self.setValue(value)


    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.is_moving:
            return
        cursor = event.pos().x() - self.x0 + int(SLIDER_HANDLE_THICKNESS/2)
        self.handle_position = cursor
        value = self.position_to_value(cursor)
        self.is_moving = True
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        self.setValue(value)
        print(f"value: {value}")


    def mouseReleaseEvent(self, event: QMouseEvent):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.is_moving = False


    def _calculate_origin(self) -> int:
        self.x0 = int((self.width() - self.track_width ) / 2)


    def value_changed(self) -> None:
        if not self.is_moving:
            self.handle_position = self.value_to_position(self.value())


    def position_to_value(self, position: int | float) -> float:
        position = max(0, min(position - SLIDER_HANDLE_THICKNESS/2, self.track_width))
        return self.minimum() + (position * self.range) / self.track_width


    def value_to_position(self, value: int | float) -> float:
        position = (
            SLIDER_HANDLE_THICKNESS/2
            + ((value - self.minimum()) * (self.track_width)) / self.range
        )
        return position


    def setTrackWidth(self, w: int) -> None:
        self.track_width = w
        self._calculate_origin()
        self.handle_position = self.value_to_position(self.value())


    def resizeEvent(self, event: QResizeEvent) -> None:
        self.setTrackWidth(self.width())
        super().resizeEvent(event)


    def paintEvent(self, event: QPaintEvent) -> None:
        # start_time = time.time()
        x0 = self.x0
        current_position = self.handle_position
        y = self.track_position
        half = SLIDER_TRACK_THICKNESS / 2
        handle_half = SLIDER_HANDLE_THICKNESS/2
        handle_position = min(max(current_position, 1), self.track_width)
        x_handle = x0 + handle_position - handle_half
        x_handle = min(max(x_handle, x0 + handle_half), x0 + self.track_width)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen()
        pen.setWidth(SLIDER_TRACK_THICKNESS)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        # Track
        t_x_min = x0 + half
        t_x_max = x0 + self.track_width - half

        # Lower
        t_x = min(x0 + current_position - SLIDER_HANDLE_THICKNESS, t_x_max)
        if t_x > t_x_min:
            pen.setColor(self.track_color_l)
            painter.setPen(pen)
            painter.drawLine(t_x_min, y, t_x, y)

        # Higher
        t_x = max(t_x_min, x0 + current_position)
        if t_x < t_x_max:
            pen.setColor(self.track_color_r)
            painter.setPen(pen)
            painter.drawLine(t_x, y, t_x_max, y)

        # Ticks
        pen.setWidth(half)
        pen.setColor(self.tick_color)
        painter.setPen(pen)
        points = [
            QPoint(x0 + half, y),
            QPoint(x0 + self.track_width - half, y)
        ]
        painter.drawPoints(points)

        # Margins around handle
        pen.setWidth(SLIDER_TRACK_THICKNESS)
        pen.setColor(self.bgd_color)
        pen.setCapStyle(Qt.PenCapStyle.SquareCap)
        painter.setPen(pen)
        painter.drawLine(
            max(x0, x_handle - SLIDER_HANDLE_MARGIN),
            y,
            min(x0 + self.track_width, x_handle + SLIDER_HANDLE_MARGIN),
            y
        )

        # Handle
        pen = QPen(self.handle_color, SLIDER_HANDLE_THICKNESS)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(x_handle, 0, x_handle, SLIDER_HANDLE_HEIGHT)

        # painter.setRenderHint(QPainter.Antialiasing, False)
        # pen = QPen(QColor(255,255,250))
        # pen.setWidth(1)
        # pen.setStyle(Qt.SolidLine)
        # painter.setPen(pen)
        # painter.drawRect(self.rect().adjusted(0,0,-1,-1))


        # painter.setRenderHint(QPainter.Antialiasing, False)
        # pen = QPen(QColor(50,255,50))
        # pen.setWidth(1)
        # pen.setStyle(Qt.SolidLine)
        # painter.setPen(pen)
        # painter.drawRect(QRect(
        #     x0,
        #     0,
        #     self.track_width,
        #     self.height()

        # ).adjusted(0,0,-1,-1))

        painter.end()
