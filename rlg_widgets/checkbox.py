import os
from typing import Optional
from PySide6.QtCore import (
    Qt,
    QRect,
    QSize,
    QPoint,
)
from PySide6.QtGui import (
    QPaintEvent,
    QPainter,
    QColor,
    QImage,
    QPixmap,
    QPen,
)
from PySide6.QtWidgets import (
    QWidget,
    QAbstractButton,
    QHBoxLayout,
)

from .utils import (
    TITLE_BAR_ICON_PATH,
    dp_to_px,
    CheckboxColor,
)

# M3 material
#   Container width     18dp
#   Container height    18dp
#   Container shape     2dp
#   Icon size           18dp
#   Icon alignment      Center-aligned
#   Target size         48dp
#   State-layer size    40dp
STATE_LAYER_SIZE: int = round(48/(2 * dp_to_px)) * 2
# Icons are from Material website
ICON_SIZE: int = 24
# blank margin in Material icons -> real button size in icon is 18x18
BUTTON_SIZE: int = 18

class Checkbox(QWidget):

    class _Checkbox(QAbstractButton):
        def __init__(self, parent: QWidget | None = ...) -> None:
            super().__init__(parent)
        def paintEvent(self, e: QPaintEvent) -> None:
            return

    def __init__(
        self,
        parent: Optional[QWidget],
        tristate: bool = False,
    ) -> None:
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.is_tristate: bool = tristate
        self.state: Qt.CheckState = Qt.CheckState.Unchecked

        unchecked = "check_box_outline_blank_FILL0_wght500_GRAD0_opsz24.png"
        partially = "indeterminate_check_box_FILL0_wght500_GRAD0_opsz24.png"
        checked = "check_box_FILL0_wght500_GRAD0_opsz24.png"

        self.pixmaps: dict[Qt.CheckState, dict[bool, QPixmap]] = {
            Qt.CheckState.Unchecked: {
                True: self._generate_pixmap(filename=unchecked, color=CheckboxColor.enabled),
                False: self._generate_pixmap(filename=unchecked, color=CheckboxColor.disabled),
            },
            Qt.CheckState.PartiallyChecked: {
                True: self._generate_pixmap(filename=partially, color=CheckboxColor.enabled),
                False: self._generate_pixmap(filename=partially, color=CheckboxColor.disabled),
            },
            Qt.CheckState.Checked: {
                True: self._generate_pixmap(filename=checked, color=CheckboxColor.enabled),
                False: self._generate_pixmap(filename=checked, color=CheckboxColor.disabled),
            },
        }

        self.setFixedSize(QSize(STATE_LAYER_SIZE, STATE_LAYER_SIZE))

        layout = QHBoxLayout(self)
        self.button = self._Checkbox(self)
        self.button.setFixedSize(QSize(BUTTON_SIZE, BUTTON_SIZE))
        margins = [int((STATE_LAYER_SIZE - BUTTON_SIZE)/2) ] * 4
        layout.setContentsMargins(*margins)
        layout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setLayout(layout)

        origin = [int((STATE_LAYER_SIZE - ICON_SIZE)/2)] * 2
        self.pixmap_origin = QPoint(*origin)
        self.painter = QPainter()

        self.button.clicked[bool].connect(self.clicked_event)
        self.button.pressed.connect(self.pressed_event)
        self.button.released.connect(self.released_event)
        self.button.toggled[bool].connect(self.toggled_event)


    def _generate_pixmap(self, filename: str, color: str) -> QPixmap:
        filepath = os.path.join(TITLE_BAR_ICON_PATH, filename)
        if not os.path.exists(filepath):
            raise ValueError(f"image {filepath} does not exist")
        qimage: QImage = QImage(filepath)
        color = QColor(color)

        painter: QPainter = QPainter()
        painter.begin(qimage)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.setBrush(color)
        painter.setPen(color)
        painter.drawRect(qimage.rect())
        painter.end()
        return QPixmap(qimage)


    def checkState(self) -> Qt.CheckState:
        return self.state


    # def hitButton(self, pos: QPoint) -> bool:
    #     return self.checkbox.hitButton(pos)


    def setCheckState(self, state: Qt.CheckState) -> None:
        self.state = state


    def setTristate(self, enabled: bool) -> None:
        self.is_tristate = enabled


    def isTristate(self) -> bool:
        return self.is_tristate


    def clicked_event(self, state: bool) -> None:
        pass


    def pressed_event(self) -> None:
        pass


    def released_event(self) -> None:
        state: int = self.state.value
        state = (state + 1) % 3 if self.is_tristate else ~state & 0x2
        self.state: Qt.CheckState = Qt.CheckState._value2member_map_[state]
        self.repaint()


    def toggled_event(self, state: bool) -> None:
        pass


    def paintEvent(self, event: QPaintEvent) -> None:
        pixmap = self.pixmaps[self.checkState()][self.isEnabled()]
        self.painter.begin(self)
        self.painter.drawPixmap(self.pixmap_origin, pixmap)

        # For debug:
        # pen = QPen('red')
        # pen.setWidth(1)
        # self.painter.setPen(pen)
        # layer_rect = QRect(0, 0, STATE_LAYER_SIZE-1, STATE_LAYER_SIZE-1)
        # self.painter.drawRect(layer_rect)

        self.painter.end()

