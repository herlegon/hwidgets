from string import Template

from PySide6.QtCore import (
    QSize,
    Qt,
    QSize,
)
from PySide6.QtGui import (
    QIcon,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
    QLineEdit,
)

from .hstyle import (
    COMBOBOX_RADIUS,
    COMBOBOX_HEIGHT,
    COMBOBOX_RADIUS,
    HStyle,
    load_png_icon,
    load_qss,
)


class _ClearButton(QPushButton):
    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        hstyle: HStyle
    ):
        super().__init__(parent)

        self.setFixedSize(QSize(COMBOBOX_HEIGHT, COMBOBOX_HEIGHT))
        self.setFlat(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.normal_icon = QIcon(load_png_icon(
            "cancel_22dp_000000_FILL0_wght400_GRAD0_opsz24.png", hstyle.text_color
        ))
        self.hover_icon = QIcon(load_png_icon(
            "cancel_22dp_000000_FILL0_wght400_GRAD0_opsz24.png", hstyle.selected
        ))
        self.setIcon(self.normal_icon)

        qss_template = Template(load_qss("lineedit_button.qss"))
        qss = qss_template.substitute(
            radius=f"{COMBOBOX_RADIUS}px",
            hover_bgd=f"{hstyle.hover_bgd}",
            selection_bgd=f"{hstyle.selection_bgd}",
            selected=f"{hstyle.selected}",
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
        hstyle: HStyle,
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

        self.setCursor(Qt.CursorShape.ArrowCursor)

        self.setFixedHeight(COMBOBOX_HEIGHT)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # Replace the clear button
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.addStretch(1)
        self.clear_button = _ClearButton(self, hstyle=hstyle)
        self.main_layout.addWidget(
            self.clear_button, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.setLayout(self.main_layout)

        qss_template = Template(load_qss("lineedit.qss"))
        qss = qss_template.substitute(
            widget_bgd=f"{hstyle.widget_bgd}",
            text_color=f"{hstyle.text_color}",
            radius=f"{COMBOBOX_RADIUS}px",
            hover_bgd=f"{hstyle.hover_bgd}",
            border_color=f"{hstyle.border}",
            disabled_bgd=f"{hstyle.disabled_bgd}",
            disabled_text=f"{hstyle.disabled_text}",
            padding_right=f"{self.clear_button.width()}px",
            editing_border=f"{hstyle.selected}",
            selected_text=f"{hstyle.selected_text}",
            selected=f"{hstyle.selected}",
        )
        self.setStyleSheet(qss)

        # print(f"{__class__.__name__} Instanciate: ro={readOnly}, button={clearButtonEnabled}")
        self.signals_connected = False
        if readOnly is not None and readOnly:
            self.setReadOnly(True)

        elif clearButtonEnabled is not None and clearButtonEnabled:
            self.setClearButtonEnabled(True)

        else:
            self.setClearButtonEnabled(False)

        self.clear_button.released.connect(self.clear_button_released)
        # print(f"{__class__.__name__} Instanciated")


    def clear_button_released(self):
        self.clear()
        self.clear_button.hide()


    def event_text_changed(self, text: str) -> None:
        if len(text) > 0:
            self.clear_button.show()
        else:
            self.clear_button.hide()


    def setClearButtonEnabled(self, enable: bool) -> None:
        # print(f"{__class__.__name__} set clear button={enable} (ro: {self.isReadOnly()}, enabled: {self.isVisible()})")
        self.blockSignals(True)
        super().setClearButtonEnabled(False)
        if enable and not self.isReadOnly() and self.isEnabled():
            self.clear_button.show()
            if not self.signals_connected:
                # print(f"{__class__.__name__}   connect signals")
                self.textChanged.connect(self.event_text_changed)
                self.textEdited.connect(self.event_text_changed)
                self.signals_connected = True
        else:
            self.clear_button.hide()
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
