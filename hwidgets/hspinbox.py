from string import Template
from PySide6.QtCore import (
    QSize,
    Qt,
    QEvent,
    QTimer,
)
from PySide6.QtGui import (
    QIcon,
)
from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QSizePolicy,
    QAbstractSpinBox,
)

from .hstyle import (
    COMBOBOX_RADIUS,
    COMBOBOX_HEIGHT,
    HStyle,
    load_png_icon,
    load_qss,
)



class HDoubleSpinBox(QDoubleSpinBox):

    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        hstyle: HStyle,
        prefix: str | None = None,
        suffix: str | None = None,
        cleanText: str | None = None,
        decimals: int | None = None,
        minimum: float | None = None,
        maximum: float | None = None,
        singleStep: float | None = None,
        stepType: QAbstractSpinBox.StepType | None = None,
        value: float | None = ...
    ) -> None:
        super().__init__(parent)

        # self.lineEdit().setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEdit().setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)


        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(COMBOBOX_HEIGHT)


        self.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, COMBOBOX_RADIUS, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.addStretch(1)
        icon_size = QSize(COMBOBOX_HEIGHT//2-1, COMBOBOX_HEIGHT//2-1)
        self.plus_button = QPushButton(self)
        self.plus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.plus_button.setFlat(True)
        self.plus_button.setFixedSize(icon_size)
        icon_plus = QIcon()
        icon_plus.addPixmap(
            load_png_icon("add_FILL0_wght500_GRAD0_opsz20.png", "#F0F0F0"),
            QIcon.Mode.Normal, QIcon.State.Off
        )
        self.plus_button.setIconSize(icon_size)
        self.plus_button.setIcon(icon_plus)
        self.plus_button.setAutoRepeat(True)

        self.minus_button = QPushButton(self)
        self.minus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.minus_button.setFlat(True)
        self.minus_button.setFixedSize(icon_size)
        icon_minus = QIcon()
        icon_minus.addPixmap(
            load_png_icon("remove_FILL0_wght500_GRAD0_opsz20.png", "#F0F0F0"),
            QIcon.Mode.Normal, QIcon.State.Off
        )
        self.minus_button.setIconSize(icon_size)
        self.minus_button.setIcon(icon_minus)
        self.minus_button.setAutoRepeat(True)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(0)
        # button_layout.setContentsMargins(0,2,0,2)
        button_layout.setContentsMargins(0,0,0,0)
        button_layout.addWidget(
            self.plus_button, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
        button_layout.addWidget(
            self.minus_button, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )

        self.main_layout.addLayout(button_layout)
        self.plus_button.clicked.connect(self.stepUp)
        self.minus_button.clicked.connect(self.stepDown)

        # self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.customContextMenuRequested.connect(self._showContextMenu)

        self.setLayout(self.main_layout)
        # self.installEventFilter(self.lineEdit())

        qss_template = Template(load_qss("hdoublespinbox.qss"))
        qss = qss_template.substitute(
            widget_bgd=f"{hstyle.widget_bgd}",
            text_color=f"{hstyle.text_color}",
            radius=f"{COMBOBOX_RADIUS}px",
            hover_bgd=f"{hstyle.hover_bgd}",
            border_color=f"{hstyle.border}",
            disabled_bgd=f"{hstyle.disabled_bgd}",
            disabled_text=f"{hstyle.disabled_text}",
            padding_right=f"{COMBOBOX_RADIUS + COMBOBOX_HEIGHT//2}px",
            editing_border=f"{hstyle.checked}",
            selected_text=f"{hstyle.selected_text}",
            padding=f"{COMBOBOX_RADIUS}px",
            selection_bgd=f"{hstyle.selection_bgd}"
        )
        self.setStyleSheet(qss)


        self._last_valid_value = self.value()
        self.lineEdit().deselect()


    # def setReadOnly(self, state: bool):
    #     super().setReadOnly(state)
    #     self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, state)


    def _validate_value(self):
        """Called when the user presses Enter — confirm the new value."""
        try:
            self.interpretText()  # Ensures text → value conversion
        except ValueError:
            self.lineEdit().setText(str(self._last_valid_value))
        else:
            self._last_valid_value = self.value()

        self.clearFocus()  # optional: lose focus on confirm


    def _cancel_edit(self):
        """Called when Escape is pressed — revert to previous value."""
        self.blockSignals(True)
        self.setValue(self._last_valid_value)
        self.blockSignals(False)
        self.lineEdit().deselect()
        self.clearFocus()


    def keyPressEvent(self, event: QEvent):
        key = event.key()

        # Validate value on Enter or Return
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._validate_value()
            event.accept()
            return

        # Revert to last valid value on Escape
        elif key == Qt.Key.Key_Escape:
            self._cancel_edit()
            event.accept()
            return

        # Otherwise, normal behavior
        super().keyPressEvent(event)


        # def __init__(...)
        # ...
        # Prevent valueChanged from selecting text
        # self.valueChanged.connect(self.event_value_modified)

    # def event_value_modified(self, value: float | int) -> None:
    #     print(f"modified")
    #     self.blockSignals(True)
    #     self.lineEdit().deselect()
    #     self.lineEdit().clearFocus()
    #     self.clearFocus()
    #     self.blockSignals(False)

    # def _prevent_auto_selection(self):
    #     QTimer.singleShot(0, self._clear_selection)
    #     QTimer.singleShot(10, self._clear_selection)

    # def _clear_selection(self):
    #     lineedit = self.lineEdit()
    #     if lineedit and (lineedit.hasSelectedText() or lineedit.hasFocus()):
    #         lineedit.deselect()
    #         lineedit.clearFocus()
    #         self.clearFocus()



class HSpinBox(HDoubleSpinBox):
    ...
