from string import Template
from typing import Type

from PySide6.QtCore import (
    Qt,
    QSize,
    QRect,
    Signal,
    Slot,
    QTimer,
)
from PySide6.QtGui import (
    QMouseEvent,
    QPainter,
    QColor,
    QBrush,
)
from PySide6.QtWidgets import (
    QWidget,
    QPlainTextEdit,
)

from .style_manager import Theme, ScrollBarStyle
from .line_edit import ClearButton
from .utils import (
    load_png_icon,
    load_qss,
)





class OverlayVScrollBar(QWidget):
    valueChanged = Signal(int)

    def __init__(self, parent, scrollbar_style: ScrollBarStyle, radius=8, thickness=12):
        super().__init__(parent)
        self.corner_radius = radius
        self._base_width = 3
        self.padding_right: int = 3

        self._hover_extra = 4
        self._hover_shift = 0
        self._hovered = False
        self._pressed = False
        self._press_offset = 0
        self._value = 0
        self._minimum = 0
        self._maximum = 100
        self._page_step = 10
        self.setMouseTracking(True)
        self.setFixedWidth(thickness)

        self.normal_brush = QBrush(QColor(scrollbar_style.normal))
        self.hover_brush = QBrush(QColor(scrollbar_style.hover))
        self.pressed_brush = QBrush(QColor(scrollbar_style.pressed))


    def setRange(self, minimum, maximum):
        self._minimum = minimum
        self._maximum = maximum
        self.update()


    def setPageStep(self, step):
        self._page_step = step
        self.update()


    def setValue(self, value):
        value = max(self._minimum, min(self._maximum, value))
        if self._value != value:
            self._value = value
            self.valueChanged.emit(value)
            self.update()


    def value(self):
        return self._value


    def enterEvent(self, event):
        self._hovered = True
        self.setFixedWidth(self._base_width + self._hover_extra)
        self.reposition_and_resize()
        self.update()
        super().enterEvent(event)


    def leaveEvent(self, event):
        self._hovered = False
        if not self._pressed:
            self.setFixedWidth(self._base_width)
            self.reposition_and_resize()
        self.update()
        super().leaveEvent(event)


    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            handle_rect = self._handle_rect()
            if handle_rect.contains(event.position().toPoint()):
                self._pressed = True
                self._press_offset = event.position().y() - handle_rect.top()
            else:
                self._pressed = True
                self._jump_to_click(event.position().y())
        super().mousePressEvent(event)


    def mouseMoveEvent(self, event: QMouseEvent):
        if self._pressed:
            y = event.position().y() - self._press_offset
            self._move_handle_to(y)
        super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressed = False
            if not self._hovered:
                self.setFixedWidth(self._base_width)
                self.reposition_and_resize()
        super().mouseReleaseEvent(event)


    def _jump_to_click(self, y):
        handle_height = max(25, int(self._page_step / (self._maximum - self._minimum + self._page_step) * self.height()))
        new_value = int(self._minimum + (y - handle_height // 2) / (self.height() - handle_height) * (self._maximum - self._minimum))
        self.setValue(new_value)


    def _move_handle_to(self, y):
        handle_height = max(25, int(self._page_step / (self._maximum - self._minimum + self._page_step) * self.height()))
        new_value = int(self._minimum + y / (self.height() - handle_height) * (self._maximum - self._minimum))
        self.setValue(new_value)


    def _handle_rect(self):
        if self._maximum == self._minimum:
            slider_height = self.height()
            slider_pos = 0
        else:
            slider_height = max(25, int(self._page_step / (self._maximum - self._minimum + self._page_step) * self.height()))
            slider_pos = int((self._value - self._minimum) / (self._maximum - self._minimum) * (self.height() - slider_height))
        rect = QRect(0, slider_pos, self.width(), slider_height)
        if self._hovered:
            rect.translate(-self._hover_shift, 0)
            rect.setLeft(max(0, rect.left()))
            rect.setRight(min(self.width(), rect.right()))
        return rect


    def paintEvent(self, event):
        painter = QPainter(self)
        # anti-aliasing off for performance
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)
        handle_rect = self._handle_rect()
        if self._pressed:
            brush = self.pressed_brush
        elif self._hovered:
            brush = self.hover_brush
        else:
            brush = self.normal_brush

        painter.setBrush(brush)
        painter.setPen(Qt.PenStyle.NoPen)
        radius = round(self.width() /2)
        painter.drawRoundedRect(handle_rect, radius, radius)


    def reposition_and_resize(self):
        parent: QWidget = self.parent()
        if not parent:
            return
        pw = parent.width()
        corner_radius = self.corner_radius
        corner_radius = self.corner_radius // 2
        x = pw - self.width() - self.padding_right
        y = corner_radius + 1
        h = max(corner_radius, parent.height() - 2 * corner_radius - 2)
        self.setGeometry(
            QRect(x, y, self.width(), h)
        )




class HPlainTextEdit(QPlainTextEdit):

    def __init__(
        self,
        text: str | QWidget | None = None,
        /,
        parent: QWidget | None = None,
        *,
        theme: Type[Theme],
        tabChangesFocus: bool | None = None,
        documentTitle: str | None = None,
        undoRedoEnabled: bool | None = None,
        lineWrapMode: QPlainTextEdit.LineWrapMode | None = None,
        readOnly: bool | None = None,
        plainText: str | None = None,
        overwriteMode: bool | None = None,
        tabStopDistance: float | None = None,
        cursorWidth: int | None = None,
        textInteractionFlags: Qt.TextInteractionFlag | None = None,
        blockCount: int | None = None,
        maximumBlockCount: int | None = None,
        backgroundVisible: bool | None = None,
        centerOnScroll: bool | None = None,
        placeholderText: str | None = None,
        clearButtonEnabled: bool = True,
    ) -> None:
        if isinstance(text, QWidget):
            parent = text
            text = ""
        elif text is None:
            text = ""

        super().__init__(parent)
        self.theme = theme
        self.pte_style = theme.plain_text_edit
        self.signals_connected = False

        # self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # Replace the default scrollbars
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)

        self.overlay_vbar: OverlayVScrollBar = None
        self._update_timer: QTimer = None

        radius: int = theme.default.radius
        self.overlay_vbar = OverlayVScrollBar(
            self,
            scrollbar_style=theme.scrollbar,
            radius=radius,
            thickness=radius,
        )

        # use QTimer to throttle updates for smoother scrolling
        self._update_timer = QTimer(self)
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._do_sync_overlay)

        native_vbar = super().verticalScrollBar()
        native_vbar.rangeChanged.connect(self._on_native_range_changed)
        native_vbar.valueChanged.connect(self._on_native_value_changed)
        self.overlay_vbar.valueChanged.connect(self._on_overlay_value_changed)
        self._sync_overlay_from_native()

        self.clear_button = ClearButton(self, style=self.pte_style)

        self.viewport().setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.viewport().setStyleSheet("background: transparent;")

        self.signals_connected = False
        self.clear_button_enabled: bool = False
        if readOnly is not None and readOnly:
            self.setReadOnly(True)
        if clearButtonEnabled is not None and clearButtonEnabled:
            self.clear_button_enabled = True
        self.setClearButtonEnabled(self.clear_button_enabled)

        self._update_stylesheet()

        # print(f"{__class__.__name__} Instanciate: ro={readOnly}, button={clearButtonEnabled}")

        if readOnly is not None and readOnly:
            self.setReadOnly(True)

        elif clearButtonEnabled is not None and clearButtonEnabled:
            self.setClearButtonEnabled(True)

        else:
            self.setClearButtonEnabled(False)

        self.clear_button.clicked.connect(self.clear_button_clicked)

        # Connect scrollbar events
        # vertical_scrollbar = self.verticalScrollBar()
        # vertical_scrollbar.rangeChanged.connect(self.on_scrollbar_changed)
        # vertical_scrollbar.valueChanged.connect(self.on_scrollbar_changed)

        # horitical_scrollbar = self.horizontalScrollBar()
        # horitical_scrollbar.rangeChanged.connect(self.on_scrollbar_changed)
        # horitical_scrollbar.valueChanged.connect(self.on_scrollbar_changed)


        native_vbar = super().verticalScrollBar()
        native_vbar.rangeChanged.connect(self._on_native_range_changed)
        native_vbar.valueChanged.connect(self._on_native_value_changed)

        # Connect the visibility change for native scrollbar
        native_vbar.sliderMoved.connect(self._on_scrollbar_visibility_changed)
        native_vbar.valueChanged.connect(self._on_scrollbar_visibility_changed)

        self.overlay_vbar.valueChanged.connect(self._on_overlay_value_changed)
        self._sync_overlay_from_native()

        self.overlay_vbar.leaveEvent(None)
        self.setPlainText(text)
        self.update_clear_button_position()

        self.textChanged.connect(self.on_text_changed)

        # Initial update when the widget is created
        self.on_text_changed()

        self.update_clear_button_position()


    def setPlainText(self, text):
        super().setPlainText(text)
        self.update_clear_button_position()


    def on_text_changed(self):
        # After text changes, update the clear button position
        self.update_clear_button_position()


    @Slot()
    def _on_scrollbar_visibility_changed(self):
        self.update_clear_button_position()

    def _update_stylesheet(self) -> None:
        theme: Theme = self.theme
        pte_style = self.pte_style
        radius = theme.default.radius

        padding_left, padding_right = radius, radius
        if self.clear_button_enabled:
            self.clear_button.show()

        else:
            self.clear_button.hide()

        # Same style sheet as line edit
        qss_template = Template(load_qss("plain_text_edit.qss"))
        qss = qss_template.substitute(
            radius=f"{radius}px",
            padding_right=f"{padding_right}px",
            padding_left=f"{padding_left}px",

            widget_bgd=f"{pte_style.bgd}",
            hover=f"{pte_style.hover}",
            disabled=f"{pte_style.disabled}",

            border_color=f"{pte_style.border}",
            border_read_only_color=f"{pte_style.border_read_only}",
            border_edition=f"{pte_style.selection}",

            selection=f"{pte_style.selection}",

            font_family=f"{pte_style.font.family}",
            font_size=f"{pte_style.font.size}pt",
            font_color=f"{pte_style.font_color}",
            font_color_disabled=f"{pte_style.font_color_disabled}",
        )
        self.setStyleSheet(qss)


    @Slot(int, int)
    def _on_native_range_changed(self, minimum, maximum):
        if not self._update_timer.isActive():
            self._update_timer.start(0)


    @Slot(int)
    def _on_native_value_changed(self, value):
        if not self._update_timer.isActive():
            self._update_timer.start(0)


    @Slot(int)
    def _on_overlay_value_changed(self, value):
        native = super().verticalScrollBar()
        if native.value() != value:
            native.setValue(value)


    def _do_sync_overlay(self):
        self._sync_overlay_from_native()


    def _sync_overlay_from_native(self):
        native = super().verticalScrollBar()
        self.overlay_vbar.blockSignals(True)
        try:
            self.overlay_vbar.setRange(native.minimum(), native.maximum())
            self.overlay_vbar.setPageStep(native.pageStep())
            self.overlay_vbar.setValue(native.value())
            # Auto-hide if not needed
            was_visible = self.overlay_vbar.isVisible()
            if native.maximum() == native.minimum():
                self.overlay_vbar.hide()
            else:
                self.overlay_vbar.show()

            if self.overlay_vbar.isVisible() != was_visible:
                self.update_clear_button_position()
        finally:
            self.overlay_vbar.blockSignals(False)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.overlay_vbar is not None:
            self.overlay_vbar.reposition_and_resize()
            if not self._update_timer.isActive():
                self._update_timer.start(0)
        self.update_clear_button_position()


    def on_scrollbar_changed(self, *args):
        self.update_clear_button_position()


    def clear_button_clicked(self):
        self.clear()
        self.clear_button.hide()


    def update_clear_button_position(self):
        v_scrollbar = self.overlay_vbar
        scrollbar_width: int = (
            self.theme.scrollbar.thickness + 4
            if v_scrollbar.isVisible()
            else 4
        )
        x = self.width() - self.clear_button.width() - scrollbar_width

        h_scrollbar = self.horizontalScrollBar()
        adjust: int = h_scrollbar.height() if h_scrollbar.isVisible() else 0
        y = self.height() - self.clear_button.height() - adjust - 4

        x0, y0 = self.clear_button.pos().toTuple()
        if x != x0 or y != y0:
            self.clear_button.move(x, y)


    def event_text_changed(self) -> None:
        if self.toPlainText() and not self.isReadOnly():
            self.clear_button.show()
        else:
            self.clear_button.hide()


    def setClearButtonEnabled(self, enable: bool) -> None:
        # print(f"{__class__.__name__} set clear button={enable} (ro: {self.isReadOnly()}, enabled: {self.isVisible()})")
        self.blockSignals(True)
        if enable and not self.isReadOnly() and self.isEnabled():
            self.clear_button.show()
            if not self.signals_connected:
                # print(f"{__class__.__name__}   connect signals")
                for signal in (
                    self.textChanged,
                ):
                    signal.connect(self.event_text_changed)
                self.signals_connected = True
        else:
            self.clear_button.hide()
            if self.signals_connected:
                for signal in (
                    self.textChanged,
                ):
                    try:
                        # print(f"{__class__.__name__}   disconnect signal {signal}")
                        signal.disconnect(self.event_text_changed)
                    except (TypeError, RuntimeError):
                        pass
                self.signals_connected = False
        self.blockSignals(False)


    def setReadOnly(self, enable: bool=True) -> None:
        super().setReadOnly(enable)
        if self.isEnabled():
            self.setClearButtonEnabled(not enable)
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            self.setClearButtonEnabled(False)
            self.setCursor(Qt.CursorShape.IBeamCursor)


    def setEnabled(self, enable: bool) -> bool:
        super().setEnabled(enable)
        if self.isReadOnly():
            self.setClearButtonEnabled(False)

        else:
            self.setClearButtonEnabled(enable)


    def setDisabled(self, enable: bool) -> bool:
        self.setEnabled(not enable)
