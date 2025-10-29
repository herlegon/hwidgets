from string import Template
from typing import overload
from .hstyle import (
    COMBOBOX_RADIUS,
    COMBOBOX_HEIGHT,
    DEBUG_GEOMETRY,
    HStyle,
    draw_widget_rect,
    load_qss,
)
from PySide6.QtCore import (
    Property,
    Qt,
    QSize,
    Signal,
)
from PySide6.QtGui import (
    QPainter,
)
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QButtonGroup,
    QToolButton,
    QSizePolicy,
)


class HButtonGroup(QWidget):
    buttons_changed = Signal(list)
    signal_selection_changed = Signal(int)

    def __init__(
        self,
        /,
        parent: QWidget | None = ...,
        *,
        buttons: list[str] | tuple[str] | None = None,
        hstyle: HStyle = None,
    ) -> None:
        super().__init__(parent)
        if hstyle is None:
            hstyle = HStyle()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        # Visual Layout
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(1)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(COMBOBOX_HEIGHT)

        # Logical Group
        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        self.hstyle = hstyle
        self._buttons: list[QToolButton] = []
        self._button_keys: list[str] = []
        if buttons is not None and buttons:
            self.set_buttons(buttons)

        self._current_index = -1
        self.set_current_button(0)
        self.group.buttonClicked.connect(self.on_button_clicked)


    def sizeHint(self) -> QSize:
        # width = self._buttons[0].width() * len(self._buttons)
        return QSize(self.width(), COMBOBOX_HEIGHT)


    def minimumSizeHint(self):
        if self._buttons:
            return QSize(self._normalize_button_widths(), COMBOBOX_HEIGHT)
        return super().minimumSizeHint()


    def _update_stylesheet(self) -> None:
        hstyle = self.hstyle
        qss_template = Template(load_qss(f"button_group.qss"))
        qss = qss_template.substitute(
            window_bgd=f"{hstyle.window_bgd}",
            widget_bgd=f"{hstyle.widget_bgd}",
            widget_hover=f"{hstyle.hover_bgd}",
            disabled_bgd=f"{hstyle.disabled_bgd}",
            text_color=f"{hstyle.text_color}",
            selected_bgd=f"{hstyle.selected}",
            checked_color=f"{hstyle.hover_bgd}",
            pressed_color=f"{hstyle.selection_bgd}",
            radius=f"{COMBOBOX_RADIUS}px",
            text_disabled=f"{hstyle.disabled_text}",
            checked_text=f"{hstyle.checked_text}",
        )
        self.setStyleSheet(qss)


    def _normalize_button_widths(self) -> int:
        max_width = max(b.sizeHint().width() for b in self._buttons)
        for b in self._buttons:
            b.setFixedWidth(max_width)
        count = len(self._buttons)
        return max_width * count + (count - 1) * self._layout.spacing()


    def buttons(self) -> list[QToolButton]:
        return self._buttons


    def set_buttons(
        self,
        buttons: list[str] | tuple[str] | dict[str, tuple[str, str]],
    ) -> None:
        """when buttons is dict[str, tuple[str, str]],
                key: (text, tooltip)
        """

        # Get current selected
        for i, b in enumerate(self._buttons):
            if b.isChecked():
                break

        # Remove old buttons from layout and button group
        for b in self._buttons:
            self.group.removeButton(b)
            self._layout.removeWidget(b)
            b.deleteLater()

        self._buttons.clear()

        is_dict: bool = bool(isinstance(buttons, dict))
        if is_dict:
            self._button_keys = list(buttons.keys())
        else:
            self._button_keys = buttons.copy()

        for i, k in enumerate(self._button_keys):
            button = QToolButton()
            if is_dict:
                text, tooltip = buttons[k]
                button.setText(text)
                button.setToolTip(tooltip)
            else:
                button.setText(k)
            button.key = k
            button.setCheckable(True)
            # button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
            button.setFixedHeight(self.height())

            if i == 0:
                button.setObjectName("segment-left")
            elif i == len(buttons) - 1:
                button.setObjectName("segment-right")
            else:
                button.setObjectName("segment-center")

            self.group.addButton(button, i)
            self._layout.addWidget(button)
            self._buttons.append(button)

            # signal to get the real current checked button
            button.clicked.connect(lambda checked, idx=i: self._on_button_checked(idx))

        if self.group.buttons():
            try:
                self.group.buttons()[i].setChecked(True)
                self.set_current_button(i)
            except:
                self.group.buttons()[0].setChecked(True)
                self.set_current_button(0)
        else:
            self.set_current_button(-1)

        self._update_stylesheet()

        width = self._normalize_button_widths()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setFixedWidth(width)
        self.adjustSize()


    @overload
    def get_button(self, index: int) -> QToolButton: ...
    @overload
    def get_button(self, key: str) -> QToolButton: ...
    def get_button(self, value: int | str) -> QToolButton:
        if isinstance(value, int):
            return self._buttons[value]
        elif isinstance(value, str):
            try:
                return self._buttons[self._button_keys.index(value)]
            except:
                print("failed")
                print(self._button_keys)

        #     for btn in self._buttons:
        #         if getattr(btn, "key", None) == value:
        #             return btn
        #     raise KeyError(f"No button with key {value!r}")
        # else:
        #     raise TypeError(f"Expected int or str, got {type(value).__name__}")


    def _update_button_states(self):
        if not self._buttons:
            return
        if self._current_index != -1:
            try:
                self._buttons[self._current_index].setChecked(True)
                return
            except:
                pass
        self._buttons[0].setChecked(True)


    def current_button_index(self) -> int:
        return self._current_index


    def current_button(self) -> QToolButton:
        return self._buttons[self._current_index]


    def _on_button_checked(self, index: int):
        # Make sure only this one is checked
        for i, btn in enumerate(self._buttons):
            btn.setChecked(i == index)
        self._current_index = index
        self.signal_selection_changed.emit(index)


    def set_current_button(self, index: int):
        """Set the currently selected button by index."""
        if index < -1:
            index = -1

        # Validate index range
        button_count = len(self.buttons())
        if index >= button_count:
            index = button_count - 1 if button_count > 0 else -1

        if self._current_index != index and index >= 0:
            self._current_index = index
            self.signal_selection_changed.emit(index)
        elif index >= 0:
            self.signal_selection_changed.emit(index)


    def on_button_clicked(self, b: QToolButton) -> None:
        try:
            index = self._buttons.index(b)
        except ValueError:
            index = -1
        print(f"{self._current_index} -> {index}")
        self.set_current_button(index)


    def paintEvent(self, event):
        if DEBUG_GEOMETRY:
            painter = QPainter(self)
            draw_widget_rect(self, painter)
            painter.end()

        return super().paintEvent(event)


    # For qt designer
    def getButtons(self) -> str:
        return ";".join([b.text() for b in self._buttons])


    def setButtons(self, value: str) -> None:
        buttons = [s.strip() for s in value.split(";") if s.strip()]
        self.set_buttons(buttons)
        self.buttons_changed.emit(value)
