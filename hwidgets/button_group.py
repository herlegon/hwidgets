from string import Template
from typing import overload
from warnings import warn
from .hstyle import (
    DEBUG_GEOMETRY,
    draw_widget_rect,
)
from .style_manager import Theme
from .utils import (
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
    signal_selection_changed = Signal(str)

    def __init__(
        self,
        /,
        parent: QWidget | None = ...,
        *,
        buttons: list[str] | tuple[str] | None = None,
        theme: Theme = None,
    ) -> None:
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        if theme is None:
            raise
        self.theme: Theme = theme
        self.useGreyscale(False)

        # Visual Layout
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(theme.button.height)

        # Logical Group
        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        self.hstyle = theme
        self._buttons: list[QToolButton] = []
        self._button_keys: list[str] = []
        if buttons is not None and buttons:
            self.set_buttons(buttons)

        self._current_index = -1
        self.set_current_button(0)
        self.group.buttonClicked.connect(self.on_button_clicked)


    def useGreyscale(self, b: bool) -> None:
        if b:
            self.btn_group_style = self.theme.grey_button_group
        else:
            self.btn_group_style = self.theme.button_group


    def sizeHint(self) -> QSize:
        # width = self._buttons[0].width() * len(self._buttons)
        return QSize(self.width(), self.theme.button.height)


    def minimumSizeHint(self):
        if self._buttons:
            return QSize(self._normalize_button_widths(), self.theme.button.height)
        return super().minimumSizeHint()


    def _update_stylesheet(self) -> None:
        radius: int = self.theme.default.radius
        btn_style = self.btn_group_style

        qss_template = Template(load_qss(f"button_group.qss"))
        qss = qss_template.substitute(
            radius=f"{radius}px",

            widget_bgd=f"{btn_style.bgd}",
            hover=f"{btn_style.hover}",
            pressed=f"{btn_style.pressed}",
            checked=f"{btn_style.checked}",
            disabled=f"{btn_style.disabled}",
            disabled_checked=f"{btn_style.disabled_checked}",

            border_color=f"{btn_style.border}",

            font_family=f"{btn_style.font.family}",
            font_size=f"{btn_style.font.size}pt",
            font_weight=f"{btn_style.font.weight}",
            font_color=f"{btn_style.font_color}",
            font_color_disabled=f"{btn_style.font_color_disabled}",
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
            button.setCursor(Qt.CursorShape.PointingHandCursor)

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
                warn(f"failed {self._button_keys}")


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
        self.signal_selection_changed.emit(self._buttons[index].key)


    @overload
    def set_current_button(self, index: int) -> None: ...
    @overload
    def set_current_button(self, key: str) -> None: ...
    def set_current_button(self, value: int | str) -> None:
        if isinstance(value, int):
            self.set_current_button_index(value)
        elif isinstance(value, str):
            try:
                index = self._button_keys.index(value)
                self.blockSignals(True)
                self.get_button(index).setChecked(True)
                self.blockSignals(False)
                self._current_index = index
            except:
                print(f"failed to set button: key=\'{value}\'")


    def set_current_button_index(self, index: int):
        """Set the currently selected button by index."""
        if index < -1:
            index = -1

        # Validate index range
        button_count = len(self.buttons())
        if index >= button_count:
            index = button_count - 1 if button_count > 0 else -1

        if index < 0:
            return

        self.blockSignals(True)
        self._buttons[index].setChecked(True)
        self.blockSignals(False)

        if self._current_index != index and index >= 0:
            self._current_index = index
            self.signal_selection_changed.emit(self._buttons[index].key)


    def on_button_clicked(self, b: QToolButton) -> None:
        try:
            index = self._buttons.index(b)
        except ValueError:
            index = -1
        if index != self._current_index:
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



class HGreyButtonGroup(HButtonGroup):

    def __init__(
        self,
        /,
        parent: QWidget | None = ...,
        *,
        buttons: list[str] | tuple[str] | None = None,
        theme: Theme = None,
    ) -> None:
        super().__init__(
            parent,
            buttons=buttons,
            theme=theme,
        )

        self.useGreyscale(True)
