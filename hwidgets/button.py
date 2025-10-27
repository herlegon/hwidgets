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
    QEvent,
)
from PySide6.QtGui import (
    QIcon,
    QPixmap,
    QPainter,
    QColor,
    QMouseEvent,
)
from PySide6.QtWidgets import (
    QPushButton,
    QSizePolicy,
    QWidget,
    QStyleOptionButton,
    QStyle,
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
        self.hstyle = hstyle

        self.setFlat(True)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        )
        self.setMinimumWidth(COMBOBOX_HEIGHT)
        self.setFixedHeight(COMBOBOX_HEIGHT)

        self._pixmaps = {}

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

        if text is not None:
            self.setText(text)

        if icon is not None:
            self.setIcon(icon)


    def _make_tinted_pixmap(
        self,
        pixmap: QPixmap,
        color: QColor | str
    ) -> QPixmap:
        """Return a QIcon tinted to the given color."""
        tinted_pixmap = QPixmap(pixmap.size())
        tinted_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(tinted_pixmap)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()

        return tinted_pixmap


    def setIconSize(self, size):
        # return super().setIconSize(size)
        return


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

        # Create tinted icons for each state
        self.pixmap_size = icon.availableSizes()[0]
        pixmap = icon.pixmap(self.pixmap_size, QIcon.Mode.Normal, QIcon.State.Off)
        self._pixmaps: dict[str, QPixmap] = {
            "normal" : self._make_tinted_pixmap(pixmap, hstyle.widget_bgd),
            "hover" : self._make_tinted_pixmap(pixmap, hstyle.hover_bgd),
            "pressed" : self._make_tinted_pixmap(pixmap, hstyle.checked),
            "checked" : self._make_tinted_pixmap(pixmap, hstyle.checked),
            "disabled" : self._make_tinted_pixmap(pixmap, hstyle.disabled_bgd),
            # Disabled + check should never occurs. bad UI
            "disabled_checked": self._make_tinted_pixmap(pixmap, hstyle.disabled_text),
        }


    def paintEvent(self, event):
        opt = QStyleOptionButton()
        self.initStyleOption(opt)

        painter = QPainter(self)

        # This button is a text button
        self.style().drawControl(QStyle.ControlElement.CE_PushButtonBevel, opt, painter, self)
        self.style().drawControl(QStyle.ControlElement.CE_PushButtonLabel, opt, painter, self)

        if not self._pixmaps:
            painter.end()
            return

        # This button is an icon
        state = opt.state
        if not (state & QStyle.StateFlag.State_Enabled):
            if state & QStyle.StateFlag.State_On:
                pixmap = self._pixmaps["disabled_checked"]
            else:
                pixmap = self._pixmaps["disabled"]

        elif state & QStyle.StateFlag.State_Sunken:
            pixmap = self._pixmaps["pressed"]

        elif state & QStyle.StateFlag.State_On:
            pixmap = self._pixmaps["checked"]

        elif state & QStyle.StateFlag.State_MouseOver:
            pixmap = self._pixmaps["hover"]

        else:
            pixmap = self._pixmaps["normal"]

        # Draw centered pixmap
        x = (self.width() - self.pixmap_size.width()) // 2
        y = (self.height() - self.pixmap_size.height()) // 2
        painter.drawPixmap(x, y, pixmap)
        painter.end()




    # def _update_icon_state(self) -> None:
    #     """Sets the icon based on the button's current state."""
    #     # Don't do anything if icons haven't been generated yet
    #     if not self._icons:
    #         return

    #     if not self.isEnabled():
    #         super().setIcon(self._icons["disabled"])

    #     elif self.isDown(): # and not self.isChecked():
    #         super().setIcon(self._icons["checked"])

    #     elif self.isChecked():
    #         super().setIcon(self._icons["checked"])

    #     elif self.underMouse():
    #         super().setIcon(self._icons["hover"])

    #     else:
    #         super().setIcon(self._icons["normal"])


    # def enterEvent(self, event):
    #     if not self.isEnabled():
    #         return
    #     if not self.isDown() and not self.isChecked():
    #         self._update_icon_state("hover")
    #     super().enterEvent(event)


    # def leaveEvent(self, event):
    #     if not self.isEnabled():
    #         return
    #     if not self.isDown() and not self.isChecked():
    #         self._update_icon_state("normal")
    #     super().leaveEvent(event)


    # def mousePressEvent(self, event):
    #     if event.button() == Qt.MouseButton.LeftButton and self.isEnabled():
    #         self._update_icon_state("pressed")
    #     super().mousePressEvent(event)


    # def mouseReleaseEvent(self, event):
    #     if self.isEnabled():
    #         if self.isChecked():
    #             self._update_icon_state("checked")
    #         else:
    #             self._update_icon_state("hover" if self.rect().contains(event.pos()) else "normal")
    #     super().mouseReleaseEvent(event)


    # def changeEvent(self, event: QEvent) -> None:
    #     """Handle state changes like enabled/disabled."""
    #     super().changeEvent(event)
    #     if event.type() == QEvent.Type.EnabledChange:
    #         self._update_icon_state()


    # def changeEvent(self, event):
    #     """Handle enable/disable and checked state changes."""
    #     if event.type() == QEvent.Type.EnabledChange:
    #         self._update_icon_state("normal" if self.isEnabled() else "disabled")
    #     elif event.type() == QEvent.Type.StyleChange:
    #         self._update_icon_state("checked" if self.isChecked() else "normal")
    #     super().changeEvent(event)


    # def _update_icon_state(self, state: str):
    #     """Switch the displayed icon according to the state."""
    #     if self._icons and state not in self._icons:
    #         state = "normal"
    #         self._current_state = state
    #         super().setIcon(self._icons[state])


    # def _set_state(self, state):
    #     """Switch icon based on interaction state."""
    #     if state not in self._icons:
    #         return
    #     self._current_state = state
    #     super().setIcon(self._icons[state])



    # def enterEvent(self, event):
    #     if self.isEnabled():
    #         if self._current_state == "checked":
    #             self._set_state("checked")
    #         else:
    #             self._set_state("hover")
    #     super().enterEvent(event)


    # def leaveEvent(self, event):
    #     print(f"{__class__.__name__} leaveEvent: checked:{self.isChecked()}")
    #     if self._current_state == "checked":
    #         self._set_state("checked")
    #     else:
    #         self._set_state("normal")
    #     super().leaveEvent(event)


    # def mousePressEvent(self, event):
    #     print(f"{__class__.__name__} press: current checked:{self.isChecked()}")
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         self._set_state("pressed")
    #     super().mousePressEvent(event)


    # def mouseReleaseEvent(self, event):
    #     print(f"{__class__.__name__} release: checked:{self.isChecked()}")
    #     if self.isCheckable():
    #         self._set_state("checked")

    #     elif self.rect().contains(event.pos()):
    #         self._set_state("hover")
    #     else:
    #         if self.isChecked():
    #             self._set_state("checked")
    #         else:
    #             self._set_state("normal")
    #     super().mouseReleaseEvent(event)


    # def setChecked(self, b: bool) -> None:
    #     print(f"{__class__.__name__} setChecked: checked:{self.isChecked()}, b={b}")
    #     if b or self._current_state == "checked":
    #         self._set_state("checked")
    #     else:
    #         self._set_state("normal")
    #     return super().setChecked(b)

