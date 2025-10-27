from dataclasses import dataclass
import math
from typing import overload

from .hstyle import (
    DEBUG_GEOMETRY,
    HStyle,
    TRACK_THICKNESS,
    draw_widget_rect,
)

from PySide6.QtCore import (
    Qt,
    QPropertyAnimation,
    Property,
    QRect,
    QSize,
)
from PySide6.QtGui import (
    QColor,
    QPaintEvent,
    QPainter,
    QPen,
    QFont,
    QFontMetrics,
)

from PySide6.QtWidgets import (
    QProgressBar,
    QWidget,
)



MC_COLORS: dict = {
    'yellow800': "#F9A825",
    'deep_orange800': "#D84315",
    'green800': "#2E7D32",
    'green600': "#43A047",
    'green700': "#388E3C",
    'green900': "#1B5E20",

    'grey400': "#BDBDBD",
    'grey500': "#9E9E9E",
    'grey600': "#757575",
    'grey800': "#616161",

    'grey': "#909090",

}

OPACITY_DISABLED = 97
OPACITY_READ_ONLY = 97


@dataclass
class RadialProgressTriggerStyle:
    warning: tuple[int, QColor | None] = (101, None)
    danger: tuple[int, QColor | None] = (101, None)
    normal: tuple[int, QColor | None] = (0, None)


# @dataclass
class RpText:
    text: str = ""
    font: QFont = QFont("Roboto-Bold", pointSize=8)
    color: QColor = QColor("#9E9E9E")



class HRadialProgress(QProgressBar):
    """Radial Progress bar in %"""

    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        hstyle: HStyle,
        bar_width: int = 32,
        bar_thickness: int = TRACK_THICKNESS,
        angle_start: int = 60,
        smooth: bool = True,
        smooth_duration_ms: int = 300,
        standard_triggers: bool = False,
    ):
        super().__init__(parent)

        self._percent = 0
        self.setValue(0)
        super().setMinimum(0)
        super().setMaximum(100)
        self.setTextVisible(False)

        bgd_color: str = MC_COLORS['grey800']
        bar_color: str = MC_COLORS['green700']

        self.bar_width = bar_width
        self.bar_thickness = bar_thickness
        self.bar_color = QColor(bar_color)
        self.track_color = QColor(bgd_color)
        self.track_color_disable = self.track_color.setAlpha(OPACITY_DISABLED)

        self.start = (270 - angle_start) * 16
        self.span  = (2 * angle_start - 360) * 16
        self.angle = angle_start

        trigger_style: RadialProgressTriggerStyle = RadialProgressTriggerStyle()
        if standard_triggers:
            # 800
            trigger_style.warning = (75, MC_COLORS['yellow800'])
            trigger_style.danger = (90, MC_COLORS['deep_orange800'])
        trigger_style.normal = (0, self.bar_color)
        self.set_trigger_style(trigger_style)

        self.legend: RpText = RpText()
        self.legend.font = QFont("Roboto-Bold", pointSize=10)
        self.legend.font.setBold(False)
        self.legend.text = ""
        self.legend_fh = QFontMetrics(self.legend.font).boundingRect('[g|$§').height()

        self.label: RpText = RpText()
        self.label.font = QFont("Roboto-Bold", pointSize=10)
        self.label.font.setBold(False)
        self.label.text = ""

        self.smooth = smooth
        self.smooth_ms: float = smooth_duration_ms / 100
        self.animation = QPropertyAnimation(self, b'percent')

        self._update_geometry()

        self.valueChanged.connect(self.percent_changed_event)


    @overload
    def setFixedSize(self, size: QSize) -> None: ...
    @overload
    def setFixedSize(self, w: int, h: int) -> None: ...

    def setFixedSize(self, *args) -> None:
        if len(args) == 1 and isinstance(args[0], QSize):
            super().setFixedSize(args[0])
        elif len(args) == 2:
            w, h = args
            super().setFixedSize(w, h)
        else:
            raise TypeError("Invalid arguments to setFixedSize()")
        self.bar_width = self.width()
        self._update_geometry()


    def setFixedWidth(self, w: int) -> None:
        super().setFixedSize(QSize(w, w))
        self.bar_width = w
        self._update_geometry()


    def setFixedHeight(self, w: int, h: int) -> None:
        super().setFixedSize(QSize(h, h))
        self.bar_width = h
        self._update_geometry()




    def set_standard_triggers(self) -> None:
        trigger_style: RadialProgressTriggerStyle = RadialProgressTriggerStyle()
        trigger_style.warning = (75, MC_COLORS['yellow800'])
        trigger_style.danger = (90, MC_COLORS['deep_orange800'])
        trigger_style.normal = (0, self.bar_color)
        self.set_trigger_style(trigger_style)


    def set_colors(self, track: str, bar: str) -> None:
        self.track_color = QColor(track)
        self.bar_color = QColor(bar)


    def setRange(self, minimum: int, maximum: int) -> None:
        pass

    def setMinimum(self, minimum: int) -> None:
        pass

    def setMaximum(self, maximum: int) -> None:
        pass


    def setValue(self, value: int, initial: bool = False) -> None:
        if initial:
            self.blockSignals(True)
            self.percent = value
            super().setValue(value)
            self.blockSignals(False)
            self.update()
            return
        super().setValue(value)


    def set_initial_value(self, value: int):
        self.setValue(value, initial=True)


    def _update_geometry(self) -> None:
        widget_width = max(
            self.bar_width,
            QFontMetrics(self.legend.font).boundingRect(self.legend.text).width() + 2
        )
        height = int(
            self.bar_width * (1 + math.cos(math.radians(self.angle))) / 2
            + self.bar_thickness
        )
        height = self.legend_fh + height if self.legend.text != "" else height
        self.bar_rect = QRect(
            int((widget_width - self.bar_width + self.bar_thickness) / 2) + 1,
            int(self.bar_thickness / 2) + 1,
            self.bar_width - self.bar_thickness - 2,
            self.bar_width - self.bar_thickness - 2
        )
        w = max(widget_width, height)
        super().setFixedSize(QSize(w, w))


    def set_bar_width(self, width: int) -> None:
        self.bar_width = width
        self._update_geometry()


    def set_thickness(self, point: int) -> None:
        self.bar_thickness = point
        self._update_geometry()


    def set_trigger_style(self, triggers: RadialProgressTriggerStyle) -> None:
        self.value_warning, color_warning = triggers.warning
        if self.value_warning > 100 or color_warning is None:
            self.value_warning = 101
        elif not isinstance(color_warning, QColor):
            color_warning = QColor(color_warning)
        self.color_warning = color_warning

        self.value_danger, color_danger = triggers.danger
        if self.value_danger > 100 or color_danger is None:
            self.value_danger = 101
        elif not isinstance(color_danger, QColor):
            color_danger = QColor(color_danger)
        self.color_danger = color_danger


    def set_legend_text(self, text: str) -> None:
        self.legend.text = text
        self._update_geometry()
        self.update()


    def set_label_text(self, text: str) -> None:
        self.label.text = text
        self._update_geometry()
        self.update()


    @Property(int)
    def percent(self):
        return self._percent


    @percent.setter
    def percent(self, value: int) -> None:
        self._percent = value
        self.setToolTip(f"{value}%")
        self.update()


    def percent_changed_event(self, value: int) -> None:
        if not self.smooth:
            self._percent = value
        self.animation.stop()
        self.animation.setStartValue(self._percent)
        self.animation.setEndValue(value)
        self.animation.setDuration(int(abs(value - self._percent) * self.smooth_ms))
        self.animation.start()
        super().setValue(value)


    def paintEvent(self, event: QPaintEvent) -> None:
        percent = self.percent
        painter = QPainter(self)
        if DEBUG_GEOMETRY:
            draw_widget_rect(self, painter)

        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        pen = QPen(
            self.track_color if self.isEnabled() else self.track_color_disable,
            self.bar_thickness,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin
        )
        painter.setPen(pen)
        painter.drawArc(self.bar_rect, self.start, self.span)

        if self.isEnabled():
            if percent > self.value_danger:
                pen.setColor(self.color_danger)
            elif percent > self.value_warning:
                pen.setColor(self.color_warning)
            else:
                pen.setColor(self.bar_color)
            painter.setPen(pen)
            painter.drawArc(self.bar_rect, self.start, int(self.span * percent / 100))

        if self.legend.text != "":
            painter.setFont(self.legend.font)
            painter.setPen(self.legend.color)
            painter.drawText(
                self.rect(),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,
                self.legend.text
            )

        if self.label.text != "":
            painter.setFont(self.label.font)
            painter.setPen(self.label.color)
            painter.drawText(
                self.bar_rect,
                Qt.AlignmentFlag.AlignCenter,
                self.label.text
            )

        painter.end()
