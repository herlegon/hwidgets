from hutils import (
    blue, lightcyan, lightgreen, lightgrey, orange, parent_directory, purple, yellow
)
from .hstyle import HStyle

from PySide6.QtCore import (
    QRectF,
    QSize,
    Qt,
    QSize,
    QPointF,

)
from PySide6.QtGui import (
    QPolygonF,
    QBrush,
    QColor,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPen,
)
from PySide6.QtWidgets import (
    QWidget,
    QCheckBox,
)



class HCheckBox(QCheckBox):

    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        hstyle: HStyle,
    ) -> None:

        size: int = 16
        radius: int = 3
        border_width: int = 2
        border_color: str = "#3a3d44"    # normal border
        disabled_color: str = "#4a4a4a"   # disabled tint

        super().__init__(parent)

        # geometry & style parameters
        self._size = size
        self._radius = radius
        self._border_width = border_width

        # Colors (QColor objects for speed)
        self._accent = QColor(hstyle.widget_bgd)
        self.checked = QColor(hstyle.selected)
        self._bg = QColor(hstyle.widget_bgd)
        self._border = QColor(border_color)
        self._disabled = QColor(disabled_color)
        self._hover = False
        self._pressed = False
        self.hstyle = hstyle

        # make widget small—sizeHint will be used by layouts
        self.setMinimumSize(self.sizeHint())

        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setMouseTracking(True)


    def setAccentColor(self, hexcolor: str):
        self._accent = QColor(hexcolor)
        self.update()


    def setBackgroundColor(self, hexcolor: str):
        self._bg = QColor(hexcolor)
        self.update()


    def sizeHint(self) -> QSize:
        # width reserves space for little box + spacing (no text, or can adapt)
        extra = 4
        return QSize(self._size + extra, self._size + extra)

    # ---- hit test: accept clicks inside the rounded rect (or a slightly larger area) ----
    def _inside_box(self, x: float, y: float) -> bool:
        # box rectangle
        r = QRectF(
            self._border_width/2 - 1,
            self._border_width/2 - 1,
            self._size + 2,
            self._size + 2
        )
        # simple bounding-box test first
        if not r.contains(x, y):
            return False
        # optional: allow rectangle hits (common) or do circular/rounded hit test
        # We'll just accept bounding rectangle for easier UX (you can tighten it)
        return True

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._pressed = True
            self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            # toggle only when released inside the box area
            pos = event.position()
            if self._inside_box(pos.x(), pos.y()):
                # call toggle through click() to emit signals normally
                self.click()
            self._pressed = False
            self.update()
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Checkbox
        x = self._border_width / 2
        y = (self.height() - self._size) / 2.0
        box = QRectF(x, y, self._size, self._size)

        if self.isEnabled():
            bgd_color = (
                self.hstyle.hover_bgd if self._hover else self.hstyle.widget_bgd
            )
            tick_color = self.checked if self.isChecked() else QColor("transparent")

        else:
            border_col = self._disabled
            bgd_color = QColor(self.hstyle.widget_bgd)
            tick_color = self.checked.darker(140)

        # Box
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(bgd_color)))
        painter.drawRoundedRect(box, self._radius, self._radius)

        # Tick
        if self.isChecked():
            painter.setPen(QPen(tick_color, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            p1 = QPointF(box.left()+box.width()*0.22, box.top()+box.height()*0.52)
            p2 = QPointF(box.left()+box.width()*0.45, box.top()+box.height()*0.75)
            p3 = QPointF(box.left()+box.width()*0.78, box.top()+box.height()*0.28)
            painter.drawPolyline(QPolygonF([p1, p2, p3]))

        painter.end()




# class HCheckBox(QWidget):

#     class _HCheckbox(QAbstractButton):

#         def __init__(self, parent: QWidget | None = ...) -> None:
#             super().__init__(parent)

#         def paintEvent(self, e: QPaintEvent) -> None:
#             return


#     def __init__(
#         self,
#         text: str,
#         /,
#         parent: QWidget | None = None,
#         *,
#         hstyle: HStyle,
#         tristate: bool = False,
#     ) -> None:

#         super().__init__(parent)
#         self.setCursor(Qt.CursorShape.PointingHandCursor)

#         self.is_tristate: bool = tristate
#         self.state: Qt.CheckState = Qt.CheckState.Unchecked

#         unchecked = "check_box_outline_blank_FILL0_wght500_GRAD0_opsz24.png"
#         partially = "indeterminate_check_box_FILL0_wght500_GRAD0_opsz24.png"
#         checked = "check_box_FILL0_wght500_GRAD0_opsz24.png"

#         self.pixmaps: dict[Qt.CheckState, dict[bool, QPixmap]] = {
#             Qt.CheckState.Unchecked: {
#                 True: self._generate_pixmap(filename=unchecked, color=hstyle.enabled),
#                 False: self._generate_pixmap(filename=unchecked, color=hstyle.disabled),
#             },
#             Qt.CheckState.PartiallyChecked: {
#                 True: self._generate_pixmap(filename=partially, color=hstyle.enabled),
#                 False: self._generate_pixmap(filename=partially, color=hstyle.disabled),
#             },
#             Qt.CheckState.Checked: {
#                 True: self._generate_pixmap(filename=checked, color=hstyle.enabled),
#                 False: self._generate_pixmap(filename=checked, color=hstyle.disabled),
#             },
#         }

#         self.setFixedSize(QSize(CHECKBOX_STATE_LAYER_SIZE, CHECKBOX_STATE_LAYER_SIZE))

#         layout = QHBoxLayout(self)
#         self.button = self._HCheckbox(self)
#         self.button.setFixedSize(QSize(CHECKBOX_BUTTON_SIZE, CHECKBOX_BUTTON_SIZE))
#         margins = [int((CHECKBOX_STATE_LAYER_SIZE - CHECKBOX_BUTTON_SIZE)/2) ] * 4
#         layout.setContentsMargins(*margins)
#         layout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
#         self.setLayout(layout)

#         origin = [int((CHECKBOX_STATE_LAYER_SIZE - CHECKBOX_ICON_SIZE)/2)] * 2
#         self.pixmap_origin = QPoint(*origin)
#         self.painter = QPainter()

#         self.button.clicked[bool].connect(self.clicked_event)
#         self.button.pressed.connect(self.pressed_event)
#         self.button.released.connect(self.released_event)
#         self.button.toggled[bool].connect(self.toggled_event)


#     def _generate_pixmap(self, filename: str, color: str) -> QPixmap:
#         filepath = os.path.join(TITLE_BAR_ICON_PATH, filename)
#         if not os.path.exists(filepath):
#             raise ValueError(f"image {filepath} does not exist")
#         qimage: QImage = QImage(filepath)
#         color = QColor(color)

#         painter: QPainter = QPainter()
#         painter.begin(qimage)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
#         painter.setBrush(color)
#         painter.setPen(color)
#         painter.drawRect(qimage.rect())
#         painter.end()
#         return QPixmap(qimage)


#     def checkState(self) -> Qt.CheckState:
#         return self.state


#     # def hitButton(self, pos: QPoint) -> bool:
#     #     return self.checkbox.hitButton(pos)


#     def setCheckState(self, state: Qt.CheckState) -> None:
#         self.state = state


#     def setTristate(self, enabled: bool) -> None:
#         self.is_tristate = enabled


#     def isTristate(self) -> bool:
#         return self.is_tristate


#     def clicked_event(self, state: bool) -> None:
#         pass


#     def pressed_event(self) -> None:
#         pass


#     def released_event(self) -> None:
#         state: int = self.state.value
#         state = (state + 1) % 3 if self.is_tristate else ~state & 0x2
#         self.state: Qt.CheckState = Qt.CheckState._value2member_map_[state]
#         self.repaint()


#     def toggled_event(self, state: bool) -> None:
#         pass


#     def paintEvent(self, event: QPaintEvent) -> None:
#         pixmap = self.pixmaps[self.checkState()][self.isEnabled()]
#         self.painter.begin(self)
#         self.painter.drawPixmap(self.pixmap_origin, pixmap)

#         # For debug:
#         # pen = QPen('red')
#         # pen.setWidth(1)
#         # self.painter.setPen(pen)
#         # layer_rect = QRect(0, 0, CHECKBOX_WIDGET_SIZE-1, CHECKBOX_WIDGET_SIZE-1)
#         # self.painter.drawRect(layer_rect)

#         self.painter.end()




