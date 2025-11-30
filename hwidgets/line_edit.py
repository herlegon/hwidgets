from pprint import pprint
from string import Template
from typing import Type

from PySide6.QtCore import (
    QSize,
    Qt,
    QSize,
    QTimer,
)
from PySide6.QtGui import (
    QIcon,
    QKeyEvent,
    QPainter,
    QPaintEvent,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
    QLineEdit,
)

from .debug import DEBUG_GEOMETRY, draw_widget_rect
from hytils import red, yellow

from .style_manager import (
    Theme,
    LineEditStyle,
)
from .utils import (
    load_png_icon,
    load_png_image,
    load_qss,
    make_tinted_pixmap,
)



class ClearButton(QPushButton):
    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        style: LineEditStyle,
    ):
        super().__init__(parent)
        # size_hint = QSize(theme.default.height, theme.default.height)
        # self.setFixedSize(size_hint)
        self.setFlat(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        icon_filename: str = "cancel_16dp_000000_FILL0_wght400_GRAD-25_opsz20.png"
        self.normal_pixmap = make_tinted_pixmap(load_png_image(icon_filename), style.button)
        # self.hover_pixmap = make_tinted_pixmap(load_png_image(icon_filename), btn_style.button_hover)
        self.hover_pixmap = make_tinted_pixmap(load_png_image(icon_filename), style.button_hover)
        self.disabled_pixmap = make_tinted_pixmap(load_png_image(icon_filename), style.button_disabled)

        self.setFixedSize(QSize(self.normal_pixmap.size()))

        # qss = """
        #     QPushButton {{
        #         background-color: red;
        #         border: solid 1px white;
        #         margin-right: {margin_right}px;
        #     }}
        # """.format(margin_right=margin_right)
        # self.setStyleSheet(qss)


    def sizeHint(self):
        return super().sizeHint()


    def enterEvent(self, event):
        if not self.isEnabled():
            return
        # self.setIcon(self.hover_icon)
        super().enterEvent(event)


    def leaveEvent(self, event):
        if not self.isEnabled():
            return
        # self.setIcon(self.normal_icon)
        super().leaveEvent(event)


    def setEnabled(self, b: bool):
        super().setEnabled(b)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, not b)


    def paintEvent(self, event: QPaintEvent) -> None:
        if not self.isVisible():
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if DEBUG_GEOMETRY:
            draw_widget_rect(self, painter)


        # Draw background (transparent)
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent)

        # Determine which icon to use based on parent state
        if not self.isEnabled():
            pixmap = self.disabled_pixmap
        elif self.underMouse() and self.isEnabled():
            pixmap = self.hover_pixmap
        else:
            pixmap = self.normal_pixmap

        # Calculate centered position
        button_rect = self.rect()
        pixmap_rect = pixmap.rect()
        x = (button_rect.width() - pixmap_rect.width()) // 2
        y = (button_rect.height() - pixmap_rect.height()) // 2
        # Draw pixmap at centered position
        painter.drawPixmap(x, y, pixmap)
        painter.end()



class HLineEdit(QLineEdit):

    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        theme: Type[Theme],
        inputMask: str | None = None,
        text: str | None = None,
        maxLength: int | None = None,
        frame: bool | None = None,
        echoMode: QLineEdit.EchoMode | None = None,
        displayText: str | None = None,
        cursorPosition: int | None = None,
        alignment:Qt.AlignmentFlag | None = None,
        modified: bool | None = None,
        hasSelectedText: bool | None = None,
        selectedText: str | None = None,
        dragEnabled: bool | None = None,
        readOnly: bool | None = None,
        undoAvailable: bool | None = None,
        redoAvailable: bool | None = None,
        acceptableInput: bool | None = None,
        placeholderText: str | None = None,
        cursorMoveStyle: Qt.CursorMoveStyle | None = None,
        clearButtonEnabled: bool | None = None
    ) -> None:
        super().__init__(parent)
        self.theme = theme
        self.le_theme = theme.line_edit

        self.setFixedHeight(theme.default.height)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # Replace the clear button
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, theme.default.radius, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.addStretch(1)
        self.clear_button = ClearButton(self, style=theme.line_edit)
        self.main_layout.addWidget(
            self.clear_button, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        self.signals_connected = False
        self.clear_button_enabled: bool = False
        if readOnly is not None and readOnly:
            self.setReadOnly(True)
        if clearButtonEnabled is not None and clearButtonEnabled:
            self.clear_button_enabled = True
        self.setClearButtonEnabled(self.clear_button_enabled)

        self._update_stylesheet()
        self.setLayout(self.main_layout)

        self.clear_button.clicked.connect(self.clear_button_clicked)


    def _update_stylesheet(self) -> None:
        theme: Theme = self.theme
        default_style = theme.default
        le_style = self.le_theme
        radius = theme.default.radius

        if self.clear_button_enabled:
            self.clear_button.show()
            self.main_layout.invalidate()
            padding_left, padding_right = radius, default_style.height

        else:
            self.clear_button.hide()
            self.main_layout.invalidate()
            padding_left, padding_right = radius, radius

        qss_template = Template(load_qss("line_edit.qss"))
        qss = qss_template.substitute(
            radius=f"{radius}px",
            padding_right=f"{padding_right}px",
            padding_left=f"{padding_left}px",

            widget_bgd=f"{le_style.bgd}",
            hover=f"{le_style.hover}",
            disabled=f"{le_style.disabled}",

            border_color=f"{le_style.border}",
            border_read_only_color=f"{le_style.border_read_only}",
            border_edition=f"{le_style.selection}",

            selection=f"{le_style.selection}",

            font_color=f"{le_style.font_color}",
            font_color_disabled=f"{le_style.font_color_disabled}",
        )
        self.setStyleSheet(qss)
        self.setFont(le_style.font.make_font())


    def clear_button_clicked(self):
        self.clear()
        self.clear_button.hide()


    def event_text_changed(self, text: str) -> None:
        if len(text) > 0 and not self.isReadOnly() and self.clear_button_enabled:
            self.clear_button.show()
        else:
            self.clear_button.hide()


    def clear(self) -> None:
        self.clear_button.hide()
        return super().clear()


    def setText(self, text: str) -> None:
        self.event_text_changed(text)
        return super().setText(text)


    def setClearButtonEnabled(self, enable: bool) -> None:
        # Always remove native clear button
        super().setClearButtonEnabled(False)
        self.clear_button_enabled = enable

        # print(f"{self.objectName()} set clear button to {enable} (ro: {self.isReadOnly()}, enabled: {self.isEnabled()}")
        # self.blockSignals(True)

        # Do not show if read only
        if self.isReadOnly():
            self.clear_button_enabled = False
            self.clear_button.hide()

        # Connect/disconnect signals
        if self.clear_button_enabled:
            self.clear_button.show()
            if not self.signals_connected:
                for signal in (self.textChanged, self.textEdited):
                    try:
                        signal.connect(self.event_text_changed)
                    except (TypeError, RuntimeError):
                        pass
                self.signals_connected = True
        else:
            self.clear_button.hide()
            if self.signals_connected:
                for signal in (self.textChanged, self.textEdited):
                    try:
                        signal.disconnect(self.event_text_changed)
                    except (TypeError, RuntimeError):
                        pass
                self.signals_connected = False

        self._update_stylesheet()
        self.main_layout.invalidate()
        # self.blockSignals(False)


    def setReadOnly(self, enable: bool=True) -> None:
        # print(f"{__class__.__name__} set ro={enable}")
        super().setReadOnly(enable)
        self.setClearButtonEnabled(not enable)


    def setEnabled(self, enable: bool) -> None:
        super().setEnabled(enable)
        self.clear_button_enabled = (
            enable if not self.isReadOnly() else False
        )
        self.clear_button.setEnabled(enable)
        self.setClearButtonEnabled(self.clear_button_enabled)


    def setDisabled(self, enable: bool) -> None:
        self.setEnabled(not enable)


    def deselect_and_clear_focus(self):
        # print(f"{__class__.__name__} deselect and clear focus")
        self.blockSignals(True)
        cursor_pos = len(self.text())
        self.setSelection(cursor_pos, 0)
        self.setCursorPosition(cursor_pos)
        self.deselect()
        self.blockSignals(False)
        self.clearFocus()


    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()

        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if self.hasFocus():
                self._editing = False
                # print(f"{__class__.__name__} keyPressEvent: enter/return")
                QTimer.singleShot(0, self.deselect_and_clear_focus)
                event.accept()
                return

        elif key == Qt.Key.Key_Escape:
            if self.hasFocus():
                self._editing = False
                # print(f"{__class__.__name__} keyPressEvent: escape")
                QTimer.singleShot(0, self.deselect_and_clear_focus)
                event.accept()
                return

        super().keyPressEvent(event)


    # def paintEvent(self, event: QPaintEvent) -> None:
    #     super().paintEvent(event)
    #     painter = QPainter(self)
    #     if DEBUG_GEOMETRY:
    #         draw_widget_rect(self, painter)
    #     painter.end()
