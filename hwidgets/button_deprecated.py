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
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme = theme
        self.default_style = theme.common

        # self.setFlat(True)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        )
        self.setMinimumWidth(theme.button.height)
        self.setFixedHeight(theme.button.height)

        self._icon = None
        self._pixmaps = {}

        qss_template = Template(load_qss("button.qss"))
        btn_style = theme.button
        default_style = theme.common
        radius: int = theme.common.radius
        qss = qss_template.substitute(
            radius=f"{radius}px",
            margin_left=f"{radius + default_style.height + 6}px",

            window_bgd=f"{theme.window_bgd}",
            widget_bgd=f"{default_style.bgd}",

            hover=f"{btn_style.hover}",
            pressed=f"{btn_style.pressed}",
            checked=f"{btn_style.checked}",
            disabled=f"{btn_style.disabled}",

            font_family=f"\"{btn_style.font.family}\"",
            font_size=f"{btn_style.font.size}pt",
            font_weight=f"{btn_style.font.weight}",

            font_color=f"{btn_style.font_color}",
            font_color_checked=f"{btn_style.font_color_checked}",
            font_color_disabled=f"{btn_style.font_color_disabled}",
        )
        self.setStyleSheet(qss)

        if text is not None:
            self.setText(text)

        if icon is not None:
            self.setIcon(icon)


    def sizeHint(self) -> QSize:
        hint = super().sizeHint()
        if not self.text() and self._pixmaps:
            hint.setWidth(self.default_style.height)
        hint.setHeight(self.default_style.height)
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
            normal = QColor(btn_style.font_color)
            pressed = QColor(btn_style.font_color)
            disabled = QColor(btn_style.font_color_disabled)
            hover = QColor(btn_style.font_color)
        else:
            normal = QColor(btn_style.normal)
            pressed = QColor(btn_style.pressed)
            disabled = QColor(btn_style.font_color_disabled)
            hover = QColor(btn_style.hover)

        self._pixmaps: dict[str, QPixmap] = {
            "normal" : make_tinted_pixmap(pixmap, normal),
            "hover" : make_tinted_pixmap(pixmap, hover),
            # "normal" : make_tinted_pixmap(pixmap, hstyle.widget_bgd),
            # "hover" : make_tinted_pixmap(pixmap, hstyle.hover_bgd),
            "pressed" : make_tinted_pixmap(pixmap, pressed),
            "checked" : make_tinted_pixmap(pixmap, pressed),
            "disabled" : make_tinted_pixmap(pixmap, disabled),
            # Disabled + check should never occurs. bad UI
            "disabled_checked": make_tinted_pixmap(pixmap, disabled),
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
        default_style = self.theme.common

        qss_template = Template(load_qss("button.qss"))
        qss = qss_template.substitute(
            radius=f"{radius}px",
            margin_left=f"{radius + default_style.height + 6}px",

            window_bgd=f"{self.theme.window_bgd}",
            widget_bgd=f"{default_style.bgd}",

            hover=f"{btn_style.hover}",
            pressed=f"{btn_style.pressed}",
            checked=f"{btn_style.checked}",
            disabled=f"{btn_style.disabled}",

            font_family=f"\"{btn_style.font.family}\"",
            font_size=f"{btn_style.font.size}pt",
            font_weight=f"{btn_style.font.weight}",

            font_color=f"{btn_style.font_color}",
            font_color_checked=f"{btn_style.font_color_checked}",
            font_color_disabled=f"{btn_style.font_color_disabled}",
        )
        self.setStyleSheet(qss)

        super().setText(text)
        self.populate_pixmaps()


    def setIcon(self, icon: QIcon | QPixmap) -> None:
        btn_style = self.theme.button
        self._icon = icon

        if icon is not None:
            radius: int = self.theme.common.radius
            btn_style = self.theme.button
            default_style = self.theme.common

            qss_template = Template(load_qss("button.qss"))
            qss = qss_template.substitute(
                radius=f"{radius}px",
                margin_left=f"{radius + default_style.height + 6}px",

                window_bgd=f"{self.theme.window_bgd}",
                widget_bgd=f"transparent",

                hover="transparent",
                pressed="transparent",
                checked=f"transparent",
                disabled=f"transparent",

                font_family=f"\"{btn_style.font.family}\"",
                font_size=f"{btn_style.font.size}pt",
                font_weight=f"{btn_style.font.weight}",

                font_color=f"{btn_style.font_color}",
                font_color_checked=f"{btn_style.font_color_checked}",
                font_color_disabled=f"{btn_style.font_color_disabled}",
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

