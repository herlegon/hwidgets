import os
from PySide6.QtCore import (
    QEvent,
    QObject,
    Qt,
    QSize,
    QPoint,
)
from PySide6.QtGui import (
    QPaintEvent,
    QPainter,
    QColor,
    QImage,
    QPixmap,
)
from PySide6.QtWidgets import (
    QWidget,
    QAbstractButton,
)

from .utils import (
    TITLE_BAR_ICON_PATH,
    dp_to_px,
    CheckboxColor,
)

# M3 material (use CHeckboxe dimensions)
#   Container width     18dp
#   Container height    18dp
#   Container shape     2dp
#   Icon size           18dp
#   Icon alignment      Center-aligned
#   Target size         48dp
#   State-layer size    40dp
STATE_LAYER_SIZE: int = round(36/(2 * dp_to_px)) * 2
# Icons are from Material website
ICON_SIZE: int = 24
# blank margin in Material icons -> real button size in icon is 18x18
BUTTON_SIZE: int = 18



class RadioButton(QAbstractButton):

    def __init__(
        self,
        parent: QWidget,
    ) -> None:
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.checked: bool = False
        self.setChecked(False)

        unchecked = "radio_button_unchecked_FILL0_wght500_GRAD0_opsz24.png"
        checked = "radio_button_checked_FILL0_wght500_GRAD0_opsz24.png"

        self.pixmaps: dict[bool, dict[bool, QPixmap]] = {
            False: {
                True: self._generate_pixmap(filename=unchecked, color=CheckboxColor.enabled),
                False: self._generate_pixmap(filename=unchecked, color=CheckboxColor.disabled),
            },
            True: {
                True: self._generate_pixmap(filename=checked, color=CheckboxColor.enabled),
                False: self._generate_pixmap(filename=checked, color=CheckboxColor.disabled),
            },
        }
        self.setFixedSize(QSize(STATE_LAYER_SIZE, STATE_LAYER_SIZE))
        origin = [int((STATE_LAYER_SIZE - ICON_SIZE)/2)] * 2
        self.pixmap_origin = QPoint(*origin)
        self.painter = QPainter()
        self.setText("")

        self.released.connect(self.released_event)
        # self.toggled[bool].connect(self.toggled_event)
        # self.clicked[bool].connect(self.clicked_event)
        # self.pressed.connect(self.pressed_event)


    # def toggled_event(self, state):
    #     print("toggled_event")

    # def clicked_event(self, state):
    #     print("clicked_event")

    # def pressed_event(self):
    #     print("pressed_event")


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
        painter.drawRect(qimage.rect().adjusted(1,1,-1,-1))
        painter.end()
        return QPixmap(qimage)


    def setText(self, text: str) -> None:
        pass


    def released_event(self) -> None:
        self.setChecked(not self.checked)


    def setChecked(self, checked: bool) -> None:
        self.checked = checked
        super().setChecked(self.checked)
        self.update()


    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        event_type = event.type()
        # print(f"{self.id}: 0x{event_type:02x}")
        return super().eventFilter(watched, event)


    def paintEvent(self, event: QPaintEvent) -> None:
        pixmap = self.pixmaps[self.checked][self.isEnabled()]
        self.painter.begin(self)
        self.painter.drawPixmap(self.pixmap_origin, pixmap)

        # For debug:
        # pen = QPen('red')
        # pen.setWidth(1)
        # self.painter.setPen(pen)
        # layer_rect = QRect(0, 0, STATE_LAYER_SIZE-1, STATE_LAYER_SIZE-1)
        # self.painter.drawRect(layer_rect)

        self.painter.end()
