from string import Template
from typing import Type

from .styles import Theme
from .hstyle import (
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
    QRect,
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
        theme: Type[Theme],
        autoDefault: bool | None = None,
        default: bool | None = None,
        flat: bool | None = True,
    ) -> None:
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.hstyle = theme

        # self.setFlat(True)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        )
        self.setMinimumWidth(theme.button.height)
        self.setFixedHeight(theme.button.height)

        self._icon = None
        self._pixmaps = {}

        qss_template = Template(load_qss("button.qss"))
        qss = qss_template.substitute(
            window_bgd=f"{theme.window_bgd}",
            widget_bgd=f"{theme.widget_bgd}",
            widget_hover=f"{theme.hover_bgd}",
            disabled_bgd=f"{theme.disabled_bgd}",
            font_color=f"{theme.font_color}",
            selection_bgd=f"{theme.selection_bgd}",
            checked_color=f"{theme.enabled}",
            radius=f"{COMBOBOX_RADIUS}px",
            margin_left=f"{COMBOBOX_RADIUS + COMBOBOX_HEIGHT + 6}px",
            text_disabled=f"{theme.disabled_text}",
            checked_text=f"{theme.checked_text}",
            font_family=f"\"{theme.font_family}\"",
            font_size=f"{theme.font_size}pt",
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


    def setIconSize(self, size):
        # return super().setIconSize(size)
        return


    def populate_pixmaps(self) -> None:
        # Create tinted icons for each state
        icon = self._icon
        if not icon:
            return

        try:
            self.pixmap_size = icon.availableSizes()[0]
        except:
            raise FileNotFoundError(f"Empty icon for button: {self.objectName()}")
            self.pixmap_size = QSize(COMBOBOX_HEIGHT, COMBOBOX_HEIGHT)
        pixmap = icon.pixmap(self.pixmap_size, QIcon.Mode.Normal, QIcon.State.Off)

        hstyle = self.hstyle
        if self.text():
            normal = hstyle.font_color
            pressed = hstyle.font_color
            disabled = hstyle.disabled_text
            hover = hstyle.font_color
        else:
            normal = hstyle.normal_button
            pressed = hstyle.pressed_button
            disabled = hstyle.disabled_bgd
            hover = hstyle.hover_button

        self._pixmaps: dict[str, QPixmap] = {
            "normal" : make_tinted_pixmap(pixmap, normal),
            "hover" : make_tinted_pixmap(pixmap, hover),
            # "normal" : make_tinted_pixmap(pixmap, hstyle.widget_bgd),
            # "hover" : make_tinted_pixmap(pixmap, hstyle.hover_bgd),
            "pressed" : make_tinted_pixmap(pixmap, pressed),
            "checked" : make_tinted_pixmap(pixmap, pressed),
            "disabled" : make_tinted_pixmap(pixmap, disabled),
            # Disabled + check should never occurs. bad UI
            "disabled_checked": make_tinted_pixmap(pixmap, hstyle.disabled_text),
        }


    def setText(self, text: str) -> None:
        if not text:
            self.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            )
            return
        else:
            self.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            )

        hstyle = self.hstyle

        qss_template = Template(load_qss("button.qss"))
        qss = qss_template.substitute(
            window_bgd=f"{hstyle.window_bgd}",
            widget_bgd=f"{hstyle.widget_bgd}",
            widget_hover=f"{hstyle.hover_bgd}",
            disabled_bgd=f"{hstyle.disabled_bgd}",
            font_color=f"{hstyle.font_color}",
            selection_bgd=f"{hstyle.window_bgd}",
            checked_color=f"{hstyle.enabled}",
            radius=f"{COMBOBOX_RADIUS}px",
            margin_left=f"{COMBOBOX_RADIUS + COMBOBOX_HEIGHT + 6}px",
            text_disabled=f"{hstyle.disabled_text}",
            checked_text=f"{hstyle.checked_text}",
            font_family=f"\"{hstyle.font_family}\"",
            font_size=f"{hstyle.font_size}pt",
        )
        self.setStyleSheet(qss)

        super().setText(text)
        self.populate_pixmaps()


    def setIcon(self, icon: QIcon | QPixmap) -> None:
        hstyle = self.hstyle
        self._icon = icon

        if icon is not None:

            qss_template = Template(load_qss("button.qss"))
            qss = qss_template.substitute(
                window_bgd=f"{hstyle.window_bgd}",
                widget_bgd=f"{hstyle.window_bgd}",
                widget_hover=f"{hstyle.window_bgd}",
                disabled_bgd=f"{hstyle.window_bgd}",
                font_color=f"{hstyle.selection_bgd}",
                selection_bgd=f"{hstyle.window_bgd}",
                checked_color=f"{hstyle.enabled}",
                radius=f"{COMBOBOX_RADIUS}px",
                margin_left=f"{COMBOBOX_RADIUS + COMBOBOX_HEIGHT + 6}px",
                text_disabled=f"{hstyle.disabled_text}",
                checked_text=f"{hstyle.checked_text}",
            )
            self.setStyleSheet(qss)
            self.populate_pixmaps()



    def paintEvent(self, event):
        opt = QStyleOptionButton()
        self.initStyleOption(opt)

        painter = QPainter(self)
        if DEBUG_GEOMETRY:
            draw_widget_rect(self, painter)

        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        self.style().drawControl(QStyle.ControlElement.CE_PushButtonBevel, opt, painter, self)
        if not self._pixmaps:
            # This button is a text button
            self.style().drawControl(QStyle.ControlElement.CE_PushButtonLabel, opt, painter, self)
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


        # Draw centered pixmap if no text
        x = (
            COMBOBOX_RADIUS
            if self.text()
            else (self.width() - self.pixmap_size.width()) // 2
        )
        y = (self.height() - self.pixmap_size.height()) // 2
        painter.drawPixmap(x, y, pixmap)

        # Draw text, better
        if self.text():
            text_rect = QRect(
                COMBOBOX_RADIUS + COMBOBOX_HEIGHT + 6, 0,
                self.width() - COMBOBOX_RADIUS,
                self.height()
            )
            painter.setPen(QColor(
                self.hstyle.font_color
                if state & QStyle.StateFlag.State_Enabled
                else self.hstyle.disabled_text
            ))
            painter.drawText(
                text_rect,
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                self.text()
            )

        painter.end()

