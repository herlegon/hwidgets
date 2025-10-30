from string import Template
from .hstyle import (
    COMBOBOX_RADIUS,
    COMBOBOX_HEIGHT,
    HStyle,
    DEBUG_GEOMETRY,
    draw_widget_rect,
)
from .utils import (
    load_qss,
    make_tinted_pixmap,
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

        qss_template = Template(load_qss("button.qss"))
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


    def sizeHint(self) -> QSize:
        hint = super().sizeHint()
        if not self.text() and self._pixmaps:
            hint.setWidth(COMBOBOX_HEIGHT)
        hint.setHeight(COMBOBOX_HEIGHT)
        return hint


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

        qss_template = Template(load_qss("button.qss"))
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
            "normal" : make_tinted_pixmap(pixmap, hstyle.widget_bgd),
            "hover" : make_tinted_pixmap(pixmap, hstyle.hover_bgd),
            "pressed" : make_tinted_pixmap(pixmap, hstyle.checked),
            "checked" : make_tinted_pixmap(pixmap, hstyle.checked),
            "disabled" : make_tinted_pixmap(pixmap, hstyle.disabled_bgd),
            # Disabled + check should never occurs. bad UI
            "disabled_checked": make_tinted_pixmap(pixmap, hstyle.disabled_text),
        }


    def paintEvent(self, event):
        opt = QStyleOptionButton()
        self.initStyleOption(opt)

        painter = QPainter(self)
        if DEBUG_GEOMETRY:
            draw_widget_rect(self, painter)

        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

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

