from pprint import pprint
from string import Template
import sys
from typing import TYPE_CHECKING, Literal, Type

from PySide6.QtCore import (
    QSize,
    Qt,
    QEvent,
    QTimer,
    QRect,
    QSize,
    QSizeF,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPixmap,
    QPainterPath,
    QPen,
)
from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QSizePolicy,
    QAbstractSpinBox,
    QSpinBox,
)

from hytils import red
from .style_manager import Theme
from .utils import load_qss


class HSpinBoxButton(QPushButton):
    hovered = Signal(bool)  # True when entered, False when left

    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        kind: Literal['plus', 'minus'],
        theme: Type[Theme],
        size: QSize,
        autoDefault: bool | None = None,
        default: bool | None = None,
        flat: bool | None = None
    ) -> None:
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.kind = kind
        radius = theme.common.radius
        button_width, button_height = size.toTuple()
        self.setFixedSize(button_width, button_height)
        # symbol
        x, y = button_width // 2 - 1, button_height // 2
        length = min(button_width, button_height) // 4

        self.setFlat(True)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setCheckable(False)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)

        default_style = theme.common
        sb_style = theme.spinbox
        # background, text
        states = {
            'normal': (default_style.bgd, sb_style.font_color),
            'hover': (sb_style.button_hover, sb_style.font_color),
            'pressed': (sb_style.button_pressed, sb_style.font_color),
            'disabled': (sb_style.disabled, sb_style.font_color_disabled),
        }

        self.pixmaps = {}
        for state, (bgd_color, font_color) in states.items():
            pixmap = QPixmap(button_width, button_height)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Draw the background
            path = QPainterPath()
            rect = QRect(0, 0, button_width, button_height)
            top = 0
            bottom, right = rect.bottom(), rect.right() + 1
            path.moveTo(0, top)
            offset = 5
            if kind == "plus":
                path.lineTo(right - radius - offset, top)
                path.arcTo(
                    right - radius - offset, top, radius + offset, radius + offset, 90, -90
                )
                path.lineTo(right, bottom)

            else:
                right -= 1
                path.lineTo(right, top)
                path.lineTo(right, bottom - radius//2)
                path.arcTo(right - radius, bottom - radius, radius, radius, 0, -90)

            path.lineTo(0, bottom)
            path.closeSubpath()
            painter.fillPath(path, QColor(bgd_color))

            # Draw symbol
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
            pen = QPen(QColor(font_color))
            pen.setWidth(1)
            painter.setPen(pen)
            if kind == 'minus':
                painter.drawLine(x - length, y - 1, x + length, y - 1)
            else:
                painter.drawLine(x - length, y, x + length, y)
                painter.drawLine(x, y - length, x, y + length)

            painter.end()

            self.pixmaps[f"{self.kind}_{state}"] = pixmap

        self.read_only: bool = False


    def setReadOnly(self, b: bool) -> None:
        self.read_only = b


    def isReadOnly(self) -> bool:
        return self.read_only


    def enterEvent(self, event: QEvent):
        if self.isEnabled() and not self.isReadOnly():
            self.hovered.emit(True)
        super().enterEvent(event)


    def leaveEvent(self, event: QEvent):
        if self.isEnabled() and not self.isReadOnly():
            self.hovered.emit(False)
        super().leaveEvent(event)


    def paintEvent(self, event: QEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        state = 'normal'
        if not self.isEnabled():
            state = 'disabled'
        elif self.isDown() and not self.isReadOnly():
            state = 'pressed'
        elif self.underMouse() and not self.isReadOnly():
            state = 'hover'

        pixmap = self.pixmaps[f"{self.kind}_{state}"]
        # top = 1 if self.kind == "plus" else 0
        painter.drawPixmap(0, 0, pixmap)
        painter.end()


class HCommonSpinBox:
    if TYPE_CHECKING:
        self: "QAbstractSpinBox"

    def __init__(
        self: QAbstractSpinBox,
        /,
        parent: QWidget | None = None,
        *,
        theme: Type[Theme],
        prefix: str | None = None,
        suffix: str | None = None,
        cleanText: str | None = None,
        decimals: int | None = None,
        minimum: float | int | None = None,
        maximum: float | int | None = None,
        singleStep: float | int | None = None,
        stepType: QAbstractSpinBox.StepType | None = None,
        value: float | int | None = 0,
        displayIntegerBase: int | None = None,
        **kwargs,
    ) -> None:
        # super().__init__(parent, **kwargs)
        self.theme = theme
        radius = theme.common.radius
        height = theme.common.height

        self.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.lineEdit().setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(height)

        self.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.addStretch(1)

        button_size = QSize(height//2 + radius, height//2)
        self.plus_button = HSpinBoxButton(self, kind='plus', theme=theme, size=button_size)
        self.plus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.plus_button.setFlat(True)
        self.plus_button.setFixedSize(button_size)
        self.plus_button.setAutoRepeat(True)

        self.minus_button = HSpinBoxButton(self, kind='minus', theme=theme, size=button_size)
        self.minus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.minus_button.setFlat(True)
        self.minus_button.setFixedSize(button_size)
        self.minus_button.setAutoRepeat(True)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(0)
        button_layout.setContentsMargins(0,1,1,2)
        button_layout.addWidget(
            self.plus_button, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
        button_layout.addWidget(
            self.minus_button, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )

        self.main_layout.addLayout(button_layout)
        self.setLayout(self.main_layout)

        qss_template = Template(load_qss("spinbox.qss"))
        sb_style = theme.spinbox
        le_style = theme.line_edit
        default_style = theme.common
        qss = qss_template.substitute(
            radius=f"{radius}px",
            padding_right=f"{radius + 12}px",
            # padding=f"{radius}px",
            margin_right=f"{radius + 12}px",
            # button_width=f"{20}px",

            widget_bgd=f"{default_style.bgd}",
            hover=f"{le_style.selection}",
            border_color=f"{default_style.border}",
            border_edition=f"{le_style.selection}",

            selection=f"{le_style.selection}",
            disabled=f"{le_style.disabled}",

            font_family=f"\"{sb_style.font.family}\"",
            font_size=f"{sb_style.font.size}pt",
            font_color=f"{sb_style.font_color}",
            font_color_disabled=f"{sb_style.font_color_disabled}",
        )
        self.setStyleSheet(qss)

        self._last_valid_value = self.value()
        self._editing = False
        self.lineEdit().deselect()
        self._saved_value = self.value()
        # When focus in/out happens the QLineEdit will emit signals and generate events.
        self._hovered = None
        self._pressed = None

        self.lineEdit().installEventFilter(self)

        self._user_selecting = False
        if sys.platform == 'win32':
            fct = self.deselect_and_clear_focus_delayed
        else:
            fct = self.event_value_changed
        self.plus_button.pressed.connect(fct)
        self.minus_button.pressed.connect(fct)
        self.plus_button.released.connect(fct)
        self.minus_button.released.connect(fct)

        self._button_hover = False
        # self.setMouseTracking(True)
        # # self.setMouseTracking(True)
        # ensure we get hover events even when children are under the cursor
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        for btn in (self.plus_button, self.minus_button):
            btn.hovered.connect(self._on_button_hover_changed)

        self.signals_connected = True
        self.plus_button.clicked.connect(self.stepUp)
        self.minus_button.clicked.connect(self.stepDown)


    def setButtonSymbols(self: QAbstractSpinBox, bs: QAbstractSpinBox.ButtonSymbols) -> None:
        # warn(f"{__class__.__name__} Ignoring \'setButtonSymbols\'")
        super().setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)


    def setEnabled(self, b: bool) -> None:
        self.plus_button.setEnabled(b)
        self.minus_button.setEnabled(b)
        super().setEnabled(b)


    def setReadOnly(self, b: bool) -> None:
        self.blockSignals(True)
        if not b:
            if not self.signals_connected:
                self.plus_button.clicked.connect(self.stepUp)
                self.minus_button.clicked.connect(self.stepDown)
                self.signals_connected = True
        else:
            if self.signals_connected:
                self.plus_button.clicked.disconnect(self.stepUp)
                self.minus_button.clicked.disconnect(self.stepDown)
                self.signals_connected = False

        self.plus_button.setReadOnly(b)
        self.minus_button.setReadOnly(b)
        self.blockSignals(False)
        super().setReadOnly(b)


    def enterEvent(self, event):
        self._set_hover(True)
        super().enterEvent(event)


    def leaveEvent(self, event):
        self._set_hover(False)
        super().leaveEvent(event)


    def _on_button_hover_changed(self, hovered: bool):
        if self.isEnabled() and not self.isReadOnly():
            self._button_hover = hovered
            if hovered:
                self._set_hover(True)
        else:
            self._button_hover = False


    def _set_hover(self, hover: bool):
        if self.isReadOnly() or not self.isEnabled():
            hover = False
        elif hover == self.property("hover"):
            return
        self.setProperty("hover", hover)
        style = self.style()
        style.unpolish(self)
        style.polish(self)
        self.update()


    def event_value_changed(self, value: float | int = 0):
        # print(f"{__class__.__name__} event_value_changed ({value})")
        if sys.platform == 'win32':
            # QTimer.singleShot(0, self.deselect_and_clear_focus)
            QTimer.singleShot(0, self.deselect_value)
        elif sys.platform == 'linux':
            QTimer.singleShot(0, self.deselect_value)


    def wheelEvent(self, event):
        super().wheelEvent(event)
        if sys.platform == 'win32':
            QTimer.singleShot(0, self.deselect_and_clear_focus)
        elif sys.platform == 'linux':
            QTimer.singleShot(0, self.deselect_value)


    def deselect_value(self) -> None:
        # print(f"{__class__.__name__}   deselect value")
        line_edit = self.lineEdit()
        line_edit.blockSignals(True)
        cursor_pos = len(line_edit.text())
        line_edit.setSelection(cursor_pos, 0)
        line_edit.setCursorPosition(cursor_pos)
        line_edit.deselect()
        line_edit.blockSignals(False)


    def deselect_and_clear_focus(self):
        # print(f"{__class__.__name__} deselect and clear focus")
        self.deselect_value()
        self.lineEdit().clearFocus()


    def deselect_and_clear_focus_delayed(self):
        # print(f"{__class__.__name__} deselect and clear focus delayed")
        QTimer.singleShot(0, self.deselect_and_clear_focus)


    def _validate_value(self):
        try:
            self.interpretText()
        except ValueError:
            self.lineEdit().setText(str(self._last_valid_value))
        else:
            self._last_valid_value = self.value()


    def discard(self):
        self.blockSignals(True)
        self.setValue(self._last_valid_value)
        self.blockSignals(False)
        self.deselect_value()
        self._editing = False


    def keyPressEvent(self, event: QEvent) -> None:
        key = event.key()

        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if self.lineEdit().hasFocus():
                self._editing = False
                # print(f"{__class__.__name__} keyPressEvent: enter/return")
                QTimer.singleShot(0, self.deselect_and_clear_focus)
                event.accept()
                return

        elif key == Qt.Key.Key_Escape:
            if self.lineEdit().hasFocus():
                self._editing = False
                # print(f"{__class__.__name__} keyPressEvent: escape")
                QTimer.singleShot(0, self.deselect_and_clear_focus)
                event.accept()
                return

        super().keyPressEvent(event)



class HDoubleSpinBox(HCommonSpinBox, QDoubleSpinBox):

    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        theme: Type[Theme],
        prefix: str | None = None,
        suffix: str | None = None,
        cleanText: str | None = None,
        decimals: int | None = None,
        minimum: float | None = None,
        maximum: float | None = None,
        singleStep: float | None = None,
        stepType: QAbstractSpinBox.StepType | None = None,
        value: float | None = 0,
        **kwargs,
    ) -> None:
        QDoubleSpinBox.__init__(self, parent)
        HCommonSpinBox.__init__(
            self,
            theme=theme,
            prefix=prefix,
            suffix=suffix,
            cleanText=cleanText,
            decimals=decimals,
            minimum=minimum,
            maximum=maximum,
            singleStep=singleStep,
            stepType=stepType,
            value=value,
            **kwargs,
        )

        if decimals is not None:
            self.setDecimals(decimals)

        self.valueChanged.connect(self.event_value_changed)



class HSpinBox(HCommonSpinBox, QSpinBox):

    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        theme: Type[Theme],
        prefix: str | None = None,
        suffix: str | None = None,
        cleanText: str | None = None,
        minimum: int | None = None,
        maximum: int | None = None,
        singleStep: int | None = None,
        stepType: QAbstractSpinBox.StepType | None = None,
        value: int | None = 0,
        displayIntegerBase: int | None = None,
        **kwargs,
    ) -> None:
        QSpinBox.__init__(self, parent)
        HCommonSpinBox.__init__(
            self,
            theme=theme,
            prefix=prefix,
            suffix=suffix,
            cleanText=cleanText,
            minimum=minimum,
            maximum=maximum,
            singleStep=singleStep,
            stepType=stepType,
            value=value,
            **kwargs,
        )

        if displayIntegerBase is not None:
            self.setDisplayIntegerBase(displayIntegerBase)

        self.valueChanged.connect(self.event_value_changed)



