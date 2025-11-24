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
        self.theme = theme

        # self.setFlat(True)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        )
        self.setMinimumWidth(theme.button.height)
        self.setFixedHeight(theme.button.height)

        self._icon = None
        self._pixmaps = {}

        qss_template = Template(load_qss("button.qss"))
        button_theme = theme.button
        radius: int = theme.common.radius
        qss = qss_template.substitute(
            window_bgd=f"{theme.window_bgd}",
            widget_bgd=f"{theme.common.bgd}",
            hover=f"{button_theme.hover}",
            disabled=f"{button_theme.disabled}",
            font_color=f"{button_theme.font_color}",
            checked_color=f"{button_theme.checked}",
            radius=f"{radius}px",
            margin_left=f"{radius + theme.common.height + 6}px",
            text_disabled=f"{button_theme.font_color_disabled}",
            font_family=f"\"{button_theme.font.family}\"",
            font_size=f"{button_theme.font.size}pt",
        )
        self.setStyleSheet(qss)

        if text is not None:
            self.setText(text)

        if icon is not None:
            self.setIcon(icon)


    def sizeHint(self) -> QSize:
        hint = super().sizeHint()
        if not self.text() and self._pixmaps:
            hint.setWidth(self.theme.common.height)
        hint.setHeight(self.theme.common.height)
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

        btn_style = self.theme.button
        if self.text():
            normal = btn_style.font_color
            pressed = btn_style.font_color
            disabled = btn_style.font
            hover = btn_style.font_color
        else:
            normal = btn_style.normal
            pressed = btn_style.pressed
            disabled = btn_style.disabled
            hover = btn_style.hover

        self._pixmaps: dict[str, QPixmap] = {
            "normal" : make_tinted_pixmap(pixmap, normal),
            "hover" : make_tinted_pixmap(pixmap, hover),
            # "normal" : make_tinted_pixmap(pixmap, hstyle.widget_bgd),
            # "hover" : make_tinted_pixmap(pixmap, hstyle.hover_bgd),
            "pressed" : make_tinted_pixmap(pixmap, pressed),
            "checked" : make_tinted_pixmap(pixmap, pressed),
            "disabled" : make_tinted_pixmap(pixmap, disabled),
            # Disabled + check should never occurs. bad UI
            "disabled_checked": make_tinted_pixmap(pixmap, btn_style.font_color_disabled),
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

        radius: int = self.theme.common.radius
        btn_style = self.theme.button

        qss_template = Template(load_qss("button.qss"))
        qss = qss_template.substitute(
            window_bgd=f"{self.theme.window_bgd}",
            widget_bgd=f"{self.theme.common.bgd}",
            widget_hover=f"{btn_style.hover}",
            disabled_bgd=f"{btn_style.disabled}",
            checked=f"{btn_style.checked}",
            pressed=f"{btn_style.pressed}",
            radius=f"{radius}px",
            margin_left=f"{radius + self.theme.common.height + 6}px",

            font_color=f"{btn_style.font_color}",
            font_color_disabled=f"{btn_style.font_color_disabled}",
            font_family=f"\"{btn_style.font.family}\"",
            font_size=f"{btn_style.font.size}pt",
        )
        self.setStyleSheet(qss)

        super().setText(text)
        self.populate_pixmaps()


    def setIcon(self, icon: QIcon | QPixmap) -> None:
        btn_style = self.theme
        self._icon = icon

        if icon is not None:
            radius: int = self.theme.common.radius
            btn_style = self.theme.button

            qss_template = Template(load_qss("button.qss"))
            qss = qss_template.substitute(
                window_bgd=f"{self.theme.window_bgd}",
                widget_bgd=f"{self.theme.window_bgd}",
                widget_hover=f"{self.theme.window_bgd}",
                disabled_bgd=f"{self.theme.window_bgd}",
                checked_color=f"{btn_style.checked}",
                radius=f"{radius}px",
                margin_left=f"{radius + self.theme.common.height + 6}px",

                font_color=f"{btn_style.font_color}",
                font_color_disabled=f"{btn_style.font_color_disabled}",
                font_family=f"\"{btn_style.font.family}\"",
                font_size=f"{btn_style.font.size}pt",
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
        radius = self.theme.common.radius
        height = self.theme.common.height
        x = (
            radius
            if self.text()
            else (self.width() - self.pixmap_size.width()) // 2
        )
        y = (self.height() - self.pixmap_size.height()) // 2
        painter.drawPixmap(x, y, pixmap)

        # Draw text, better
        if self.text():
            text_rect = QRect(
                radius + height + 6, 0,
                self.width() - radius,
                self.height()
            )
            painter.setPen(QColor(
                self.theme.button.font_color
                if state & QStyle.StateFlag.State_Enabled
                else self.theme.button.font_color_disabled
            ))
            painter.drawText(
                text_rect,
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                self.text()
            )

        painter.end()

