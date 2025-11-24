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
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
    QLineEdit,
)

from .style_manager import Theme
from .utils import (
    load_png_icon,
    load_qss,
)


class ClearButton(QPushButton):
    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        theme: Theme
    ):
        super().__init__(parent)

        self.setFixedSize(
            QSize(theme.common.height, theme.common.height)
        )
        self.setFlat(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_theme = theme.icon_button
        self.normal_icon = QIcon(load_png_icon(
            "cancel_22dp_000000_FILL0_wght400_GRAD0_opsz24.png", btn_theme.normal
        ))
        self.hover_icon = QIcon(load_png_icon(
            "cancel_22dp_000000_FILL0_wght400_GRAD0_opsz24.png", btn_theme.hover
        ))
        self.setIcon(self.normal_icon)

        qss_template = Template(load_qss("icon_button.qss"))
        qss = qss_template.substitute(
            radius=f"{theme.common.radius}px",
            # hover_bgd=f"{btn_theme.hover}",
            # selection_bgd=f"{btn_theme.selected}",
            # selected=f"{btn_theme.font_color_selection}",
            margin_right="4px"
        )
        self.setStyleSheet(qss)


    def enterEvent(self, event):
        self.setIcon(self.hover_icon)
        super().enterEvent(event)


    def leaveEvent(self, event):
        self.setIcon(self.normal_icon)
        super().leaveEvent(event)



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

        self.setCursor(Qt.CursorShape.ArrowCursor)

        self.setFixedHeight(theme.common.height)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # Replace the clear button
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.addStretch(1)
        self.clear_button = ClearButton(self, theme=theme)
        self.main_layout.addWidget(
            self.clear_button, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.setLayout(self.main_layout)


        # print(f"{__class__.__name__} Instanciate: ro={readOnly}, button={clearButtonEnabled}")
        self.signals_connected = False
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

        self.clear_button.released.connect(self.clear_button_released)
        # print(f"{__class__.__name__} Instanciated")


    def _update_stylesheet(self) -> None:
        theme: Theme = self.theme
        le_theme = theme.line_edit
        radius = theme.common.radius

        if not self.is_clear_button_enabled:
            self.clear_button.setFixedWidth(0)
            self.clear_button.hide()
            self.main_layout.invalidate()
            padding_left, padding_right = radius, radius

        else:
            self.clear_button.show()
            self.clear_button.setFixedWidth(radius)
            self.main_layout.invalidate()
            padding_left, padding_right = radius, theme.common.height

        qss_template = Template(load_qss("lineedit.qss"))
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



    def clear_button_released(self):
        self.clear()
        self.clear_button.hide()


    def event_text_changed(self, text: str) -> None:
        if len(text) > 0:
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
        # print(f"{self.objectName()} set clear button={enable} (ro: {self.isReadOnly()}, enabled: {self.isVisible()})")
        self.blockSignals(True)
        super().setClearButtonEnabled(False)

        if enable and not self.isReadOnly() and self.isEnabled():
            self.is_clear_button_enabled = True
            self._update_stylesheet()
            self.main_layout.invalidate()
            if not self.signals_connected:
                # print(f"{__class__.__name__}   connect signals")
                self.textChanged.connect(self.event_text_changed)
                self.textEdited.connect(self.event_text_changed)
                self.signals_connected = True

        else:
            self.is_clear_button_enabled = False
            self._update_stylesheet()
            self.main_layout.invalidate()

            if self.signals_connected:
                for signal in (self.textChanged, self.textEdited):
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
        else:
            self.setClearButtonEnabled(False)


    def setEnabled(self, enable: bool) -> None:
        # print(f"{__class__.__name__} set enabled={enable}")
        super().setEnabled(enable)
        self.is_clear_button_enabled = (
            enable if not self.isReadOnly() else False
        )
        self.setClearButtonEnabled(self.is_clear_button_enabled)


    def setDisabled(self, enable: bool) -> None:
        # print(f"{__class__.__name__} set disabled={enable}")
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
