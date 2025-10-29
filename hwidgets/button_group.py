from string import Template
from .hstyle import (
    COMBOBOX_RADIUS,
    COMBOBOX_HEIGHT,
    DEBUG_GEOMETRY,
    HStyle,
    draw_widget_rect,
    load_qss,
)
from PySide6.QtCore import (
    Qt,
    QSize,
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
    def __init__(
        self,
        /,
        parent: QWidget | None = ...,
        *,
        buttons: list[str] | tuple[str] | None = None,
        hstyle: HStyle,
    ) -> None:
        super().__init__(parent)

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
        self._buttons = []
        if buttons is not None and buttons:
            self.set_buttons(buttons)

        self.group.buttonClicked.connect(self.on_button_clicked)

    def sizeHint(self) -> QSize:
        # width = self._buttons[0].width() * len(self._buttons)
        return QSize(self.width(), COMBOBOX_HEIGHT)


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


    def _normalize_button_widths(self) -> None:
        max_width = max(b.sizeHint().width() for b in self._buttons)
        for b in self._buttons:
            b.setFixedWidth(max_width)
        return max_width * len(self._buttons)

    def set_buttons(
        self,
        buttons: list[str] | tuple[str],
        normalize_widths: bool = False
    ) -> None:

        for i, text in enumerate(buttons):
            button = QToolButton()
            button.setText(text)
            button.setCheckable(True)
            button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
            button.setFixedHeight(COMBOBOX_HEIGHT)

            if i == 0:
                button.setObjectName("segment-left")

            elif i == len(buttons) - 1:
                button.setObjectName("segment-right")

            else:
                button.setObjectName("segment-center")

            self.group.addButton(button, i)
            self._layout.addWidget(button)
            self._buttons.append(button)

        if self.group.buttons():
            self.group.buttons()[0].setChecked(True)

        self._update_stylesheet()
        # self.adjustSize()
        width = self._normalize_button_widths()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setFixedWidth(width)
        self.adjustSize()


    def on_button_clicked(self, button):
        print(f"Button clicked: {button.text()}")


    def paintEvent(self, event):
        if DEBUG_GEOMETRY:
            painter = QPainter(self)
            draw_widget_rect(self, painter)
            painter.end()

        return super().paintEvent(event)
