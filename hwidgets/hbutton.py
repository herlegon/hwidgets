from string import Template
from .hstyle import (
    COMBOBOX_RADIUS,
    COMBOBOX_HEIGHT,
    HStyle,
    load_qss,
)

from PySide6.QtCore import (
    Qt,
    QSize,
)
from PySide6.QtGui import (
    QIcon,
    QPixmap,
    QPainter,
    QColor,
)
from PySide6.QtWidgets import (
    QPushButton,
    QSizePolicy,
    QWidget,
)


class HButton(QPushButton):

    def __init__(
        self,
        /,
        parent: QWidget | None = ...,
        *,
        icon: QIcon | QPixmap | None = None,
        text: str | None = None,
        hstyle: HStyle,
        autoDefault: bool | None = None,
        default: bool | None = None,
        flat: bool | None = True,
    ) -> None:

        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        if text is not None:
            self.setText(text)
        if icon is not None:
            self.setIcon(icon)

        self.setFlat(True)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        )
        self.setMinimumWidth(COMBOBOX_HEIGHT)
        self.setFixedHeight(COMBOBOX_HEIGHT)


        qss_template = Template(load_qss(f"hbutton.qss"))
        qss = qss_template.substitute(
            window_bgd=f"{hstyle.window_bgd}",
            widget_bgd=f"{hstyle.widget_bgd}",
            widget_hover=f"{hstyle.hover_bgd}",
            disabled_bgd=f"{hstyle.disabled_bgd}",
            text_color=f"{hstyle.text_color}",
            selection_bgd=f"{hstyle.selection_bgd}",
            checked_color=f"{hstyle.enabled}",
            radius=f"{COMBOBOX_RADIUS}px",
            text_disabled=f"{hstyle.disabled_text}",
            checked_text=f"{hstyle.checked_text}",
        )
        self.setStyleSheet(qss)

        self.hstyle = hstyle
        self._base_icon = None
        self._icons = {}  # {"normal": QIcon, "hover": QIcon, "pressed": QIcon}
        self._current_state = "normal"


    def _make_tinted_icon(self, base_icon, pixmap, color):
        """Return a QIcon tinted to the given color."""
        tinted_pixmap = QPixmap(pixmap.size())
        tinted_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(tinted_pixmap)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()

        new_icon = QIcon(base_icon)
        new_icon.addPixmap(tinted_pixmap, QIcon.Mode.Normal, QIcon.State.Off)
        return new_icon


    def setIcon(self, icon: QIcon | QPixmap) -> None:
        hstyle = self.hstyle

        qss_template = Template(load_qss(f"hbutton.qss"))
        qss = qss_template.substitute(
            window_bgd=f"{hstyle.window_bgd}",
            widget_bgd=f"{hstyle.window_bgd}",
            widget_hover=f"{hstyle.window_bgd}",
            disabled_bgd=f"{hstyle.window_bgd}",
            text_color=f"{hstyle.selection_bgd}",
            selection_bgd=f"{hstyle.window_bgd}",
            checked_color=f"{hstyle.enabled}",
            radius=f"{COMBOBOX_RADIUS}px",
            text_disabled=f"{hstyle.disabled_text}",
            checked_text=f"{hstyle.checked_text}",
        )
        self.setStyleSheet(qss)

        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        )
        self.setFixedWidth(COMBOBOX_HEIGHT)


        self._base_icon = icon
        size = icon.availableSizes()[0]

        pixmap = icon.pixmap(size, QIcon.Mode.Normal, QIcon.State.Off)
        if pixmap.isNull():
            pixmap = icon.pixmap(size)

        if pixmap.isNull():
            return super().setIcon(icon)

        # Create tinted icons for each state
        self._icons["normal"] = self._make_tinted_icon(icon, pixmap, self.hstyle.widget_bgd)
        self._icons["hover"] = self._make_tinted_icon(icon, pixmap, self.hstyle.hover_bgd)
        self._icons["pressed"] = self._make_tinted_icon(icon, pixmap, self.hstyle.checked)
        self._icons["checked"] = self._make_tinted_icon(icon, pixmap, self.hstyle.checked)

        super().setIcon(self._icons["normal"])


    def enterEvent(self, event):
        if self.isEnabled():
            if self._current_state == "checked":
                self._set_state("checked")
            else:
                self._set_state("hover")
        super().enterEvent(event)


    def leaveEvent(self, event):
        # print(f"{__class__.__name__} leaveEvent: checked:{self.isChecked()}")
        if self._current_state == "checked":
            self._set_state("checked")
        else:
            self._set_state("normal")
        super().leaveEvent(event)


    def mousePressEvent(self, event):
        print(f"{__class__.__name__} release: checked:{self.isChecked()}")
        if event.button() == Qt.MouseButton.LeftButton:
            self._set_state("pressed")
        super().mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        print(f"{__class__.__name__} release: checked:{self.isChecked()}")
        if self.isCheckable():
            self._set_state("checked")

        elif self.rect().contains(event.pos()):
            self._set_state("hover")
        else:
            if self.isChecked():
                self._set_state("checked")
            else:
                self._set_state("normal")
        super().mouseReleaseEvent(event)


    def setChecked(self, b: bool) -> None:
        print(f"{__class__.__name__} release: checked:{self.isChecked()}, b={b}")
        if b or self._current_state == "checked":
            self._set_state("checked")
        else:
            self._set_state("normal")
        return super().setChecked(b)


    def _set_state(self, state):
        """Switch icon based on interaction state."""
        if state not in self._icons:
            return
        self._current_state = state
        super().setIcon(self._icons[state])

