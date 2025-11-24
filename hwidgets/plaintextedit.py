from string import Template
from typing import Type

from PySide6.QtCore import (
    QSize,
    Qt,
    QSize,
    QRect,
    QPoint,
    Signal,
    Slot,
    QTimer,
)
from PySide6.QtGui import (
    QIcon,
    QMouseEvent,
    QPainter,
    QColor,
    QBrush,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
    QPlainTextEdit,
)

from hwidgets.scrollbar import HScrollBar

from .style_manager import Theme
from .lineedit import ClearButton
from .utils import (
    load_png_icon,
    load_qss,
)





class OverlayVScrollBar(QWidget):
    valueChanged = Signal(int)

    def __init__(self, parent=None, radius=8, width=12):
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
        self.setFixedWidth(width)

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
        painter.fillRect(self.rect(), Qt.transparent)
        handle_rect = self._handle_rect()
        color = QColor("#77f") if self._hovered else QColor("#66c")
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        radius = round(self.width() /2)
        # print(f"radius= {radius}")
        painter.drawRoundedRect(handle_rect, radius, radius)


    def reposition_and_resize(self):
        parent: QWidget = self.parent()
        if not parent:
            return
        pw = parent.width()
        cr = self.corner_radius
        x = pw - self.width() - self.padding_right
        y = cr + 1
        h = max(cr, parent.height() - 2 * cr - 2)
        self.setGeometry(
            QRect(x, y, self.width(), h)
        )




class HPlainTextEdit(QPlainTextEdit):

    def __init__(
        self,
        text: str,
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
        super().__init__(parent)
        self.theme = theme

        self.setCursor(Qt.CursorShape.ArrowCursor)

        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)


        # Replace the default scrollbars
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)


        self.overlay_vbar: OverlayVScrollBar = None
        self._update_timer: QTimer = None

        radius: int = theme.common.radius
        self.overlay_vbar = OverlayVScrollBar(self, radius=radius, width=radius)

        # use QTimer to throttle updates for smoother scrolling
        self._update_timer = QTimer(self)
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._do_sync_overlay)

        native_vbar = super().verticalScrollBar()
        native_vbar.rangeChanged.connect(self._on_native_range_changed)
        native_vbar.valueChanged.connect(self._on_native_value_changed)
        self.overlay_vbar.valueChanged.connect(self._on_overlay_value_changed)
        self._sync_overlay_from_native()

        self.clear_button = ClearButton(self, hstyle=theme)

        self.viewport().setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.viewport().setStyleSheet("background: transparent;")

        self.is_clear_button_enabled: bool = False
        if readOnly is not None and readOnly:
            self.setReadOnly(True)

        elif clearButtonEnabled is not None and clearButtonEnabled:
            self.is_clear_button_enabled = True
            self.setClearButtonEnabled(self.is_clear_button_enabled)

        else:
            self.setClearButtonEnabled(self.is_clear_button_enabled)

        self.clear_button.setVisible(False)
        self._update_stylesheet()

        # print(f"{__class__.__name__} Instanciate: ro={readOnly}, button={clearButtonEnabled}")
        self.signals_connected = False
        if readOnly is not None and readOnly:
            self.setReadOnly(True)

        elif clearButtonEnabled is not None and clearButtonEnabled:
            self.setClearButtonEnabled(True)

        else:
            self.setClearButtonEnabled(False)

        self.clear_button.released.connect(self.clear_button_released)

        # Connect scrollbar events
        # vertical_scrollbar = self.verticalScrollBar()
        # vertical_scrollbar.rangeChanged.connect(self.on_scrollbar_changed)
        # vertical_scrollbar.valueChanged.connect(self.on_scrollbar_changed)

        # horitical_scrollbar = self.horizontalScrollBar()
        # horitical_scrollbar.rangeChanged.connect(self.on_scrollbar_changed)
        # horitical_scrollbar.valueChanged.connect(self.on_scrollbar_changed)

        self.overlay_vbar.leaveEvent(None)
        self.update_clear_button_position()


    def _update_stylesheet(self) -> None:
        theme: Theme = self.theme
        le_theme = theme.line_edit
        radius = theme.common.radius

        if not self.is_clear_button_enabled:
            self.clear_button.setFixedWidth(0)
            self.clear_button.hide()
            # self.main_layout.invalidate()
            padding_left, padding_right = radius, radius

        else:
            self.clear_button.show()
            self.clear_button.setFixedWidth(radius)
            # self.main_layout.invalidate()
            padding_left, padding_right = radius, theme.common.height

        # Use line_edit style
        qss_template = Template(load_qss("plaintextedit.qss"))
        qss = qss_template.substitute(
            padding_right=f"{padding_right}px",
            padding_left=f"{padding_left}px",

            widget_bgd=f"{theme.common}",
            font_color=f"{le_theme.font_color}",
            radius=f"{radius}px",
            hover_bgd=f"{le_theme.hover}",
            border_color=f"{theme.common.border}",
            disabled_bgd=f"{le_theme.disabled}",
            font_color_disabled=f"{le_theme.font_color_disabled}",
            editing_border=f"{le_theme.selected}",
            selected_text=f"{le_theme.font_color_selection}",
            selected=f"{le_theme.selected}",
            font_family=f"\"{le_theme.font.family}\"",
            font_size=f"{le_theme.font.size}pt",
        )
        self.setStyleSheet(qss)

        # for HLineEdit, it's set in the qss file. here because the button has
        #   to be moved, it can't be done in the stylesheet
        self.margin = 6



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
            if native.maximum() == native.minimum():
                self.overlay_vbar.hide()
            else:
                self.overlay_vbar.show()
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


    def clear_button_released(self):
        self.clear()
        self.clear_button.hide()


    def update_clear_button_position(self):
        v_scrollbar = self.overlay_vbar
        adjust: int = v_scrollbar.width() if v_scrollbar.isVisible() else 0
        x = self.width() - self.clear_button.width() - adjust - self.margin

        h_scrollbar = self.horizontalScrollBar()
        adjust: int = h_scrollbar.height() if h_scrollbar.isVisible() else 0
        y = self.height() - self.clear_button.height() - adjust - self.margin

        x0, y0 = self.clear_button.pos().toTuple()
        if x != x0 or y != y0:
            self.clear_button.move(x, y)


    def event_text_changed(self) -> None:
        if self.toPlainText():
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
        # print(f"{__class__.__name__} set ro={enable}")
        super().setReadOnly(enable)
        if self.isEnabled():
            self.setClearButtonEnabled(not enable)
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            self.setClearButtonEnabled(False)
            self.setCursor(Qt.CursorShape.IBeamCursor)


    def setEnabled(self, enable: bool) -> bool:
        # print(f"{__class__.__name__} set enabled={enable}")
        super().setEnabled(enable)
        if self.isReadOnly():
            self.setClearButtonEnabled(False)

        else:
            self.setClearButtonEnabled(enable)


    def setDisabled(self, enable: bool) -> bool:
        # print(f"{__class__.__name__} set disabled={enable}")
        self.setEnabled(not enable)
