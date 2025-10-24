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
    QPlainTextEdit,
)

from hwidgets.hscrollbar import HScrollBar

from .hstyle import (
    COMBOBOX_RADIUS,
    COMBOBOX_HEIGHT,
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
        self.setCursor(Qt.CursorShape.ArrowCursor)

        self.setFixedSize(QSize(COMBOBOX_HEIGHT, COMBOBOX_HEIGHT))
        self.setFlat(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.normal_icon = QIcon(load_png_icon(
            "cancel_22dp_000000_FILL0_wght400_GRAD0_opsz24.png",
            hstyle.text_color
        ))
        self.hover_icon = QIcon(load_png_icon(
            "cancel_22dp_000000_FILL0_wght400_GRAD0_opsz24.png",
            hstyle.enabled
        ))
        self.setIcon(self.normal_icon)

        qss_template = Template(load_qss("hplaintextedit_button.qss"))
        qss = qss_template.substitute(
            radius=f"{COMBOBOX_RADIUS}px",
            hover_bgd=f"{hstyle.hover_bgd}",
            selection_bgd=f"{hstyle.selection_bgd}",
        )
        self.setStyleSheet(qss)


    def enterEvent(self, event):
        self.setIcon(self.hover_icon)
        super().enterEvent(event)


    def leaveEvent(self, event):
        self.setIcon(self.normal_icon)
        super().leaveEvent(event)



class HPlainTextEdit(QPlainTextEdit):

    def __init__(
        self,
        text: str,
        /,
        parent: QWidget | None = None,
        *,
        hstyle: HStyle,
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

        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)


        # Replace the default scrollbars
        self.vbar = HScrollBar(self, hstyle=hstyle)
        self.vbar.setOrientation(Qt.Orientation.Vertical)
        self.setVerticalScrollBar(self.vbar)

        # hbar = HScrollBar(self)
        # self.setHorizontalScrollBar(hbar)



        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.main_layout.addStretch(1)
        self.clear_button = _ClearButton(self, hstyle=hstyle)
        self.main_layout.addWidget(
            self.clear_button, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.setLayout(self.main_layout)

        qss_template = Template(load_qss("hplaintextedit.qss"))
        qss = qss_template.substitute(
            widget_bgd=f"{hstyle.widget_bgd}",
            text_color=f"{hstyle.text_color}",
            radius=f"{COMBOBOX_RADIUS}px",
            hover_bgd=f"{hstyle.hover_bgd}",
            border_color=f"{hstyle.border}",
            disabled_bgd=f"{hstyle.disabled_bgd}",
            disabled_text=f"{hstyle.disabled_text}",
            padding_right=f"{COMBOBOX_RADIUS}px",
            editing_border=f"{hstyle.checked}",
            selected_text=f"{hstyle.selected_text}",
        )
        self.setStyleSheet(qss)
        # for HLineEdit, it's set in the qss file. here because the button has
        #   to be moved, it can't be done in the stylesheet
        self.margin = 2


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
        vertical_scrollbar = self.verticalScrollBar()
        vertical_scrollbar.rangeChanged.connect(self.on_scrollbar_changed)
        vertical_scrollbar.valueChanged.connect(self.on_scrollbar_changed)

        horitical_scrollbar = self.horizontalScrollBar()
        horitical_scrollbar.rangeChanged.connect(self.on_scrollbar_changed)
        horitical_scrollbar.valueChanged.connect(self.on_scrollbar_changed)

        self.update_clear_button_position()

        # print(f"{__class__.__name__} Instanciated")


    def resizeEvent(self, event):
        super().resizeEvent(event)
        # self.vbar.updateGeometryRelativeToParent()
        self.update_clear_button_position()


    def on_scrollbar_changed(self, *args):
        self.update_clear_button_position()


    def clear_button_released(self):
        self.clear()
        self.clear_button.hide()


    def update_clear_button_position(self):
        v_scrollbar = self.verticalScrollBar()
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
