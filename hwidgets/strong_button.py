from string import Template
from typing import Type

from .button_deprecated import HButton

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
    QFontMetrics,
    QFont,
    QPaintEvent,
)
from PySide6.QtWidgets import (
    QPushButton,
    QSizePolicy,
    QWidget,
    QStyleOptionButton,
    QStyle,
)



class HStrongButton(QPushButton):

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
        self.default_style = theme.default

        self._icon = None
        self.text_width = 0
        # space between icon and text
        self.space: int = 12

        self._cached_size: QSize = None

        if text is not None:
            self.setText(text)
        if icon is not None:
            self.setIcon(icon)
        self._pixmaps = {}

        self.populate_pixmaps()
        self._update_stylesheet()


    def _recalculate_size(self) -> None:
        """Recalculate the width and height of the button and store it in cache."""
        radius: int = self.theme.default.radius
        height: int = self.theme.strong_button.height

        if self.text():
            text_width = self.fontMetrics().horizontalAdvance(self.text())

            if self._icon:
                icon_width = height
                total_width = radius + icon_width + self.space + text_width + radius
            else:
                total_width = 2 * radius + text_width + self.space

            width = max(total_width, height)
        else:
            width = height

        self._cached_size = QSize(width, height)


    def sizeHint(self) -> QSize:
        if self._cached_size is None:
            self._recalculate_size()
        return self._cached_size


    def minimumSizeHint(self) -> QSize:
        """Return the same as sizeHint to prevent shrinking below desired size."""
        return self.sizeHint()


    def setText(self, text: str) -> None:
        super().setText(text)
        self._recalculate_size()
        self._update_stylesheet()


    def setIcon(self, icon: QIcon | QPixmap) -> None:
        self._icon = icon
        self.populate_pixmaps()
        self._recalculate_size()
        self._update_stylesheet()


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
        normal = QColor(btn_style.font_color)
        pressed = QColor(btn_style.font_color)
        disabled = QColor(btn_style.font_color_disabled)
        hover = QColor(btn_style.font_color)

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


    def _update_stylesheet(self):
        if self.text():
            self.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
            )
        else:
            self.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            )
        self.setMinimumWidth(self.sizeHint().width())

        radius: int = self.theme.default.radius
        strong_btn_style = self.theme.strong_button
        default_style = self.theme.default
        self.setFixedHeight(strong_btn_style.height)

        qss_template = Template(load_qss("button.qss"))
        qss = qss_template.substitute(
            radius=f"{radius}px",
            margin_left=f"{radius + default_style.height + 6}px",

            window_bgd=f"{self.theme.window_bgd}",
            widget_bgd=f"{strong_btn_style.bgd}",

            hover=f"{strong_btn_style.hover}",
            pressed=f"{strong_btn_style.pressed}",
            checked=f"{strong_btn_style.checked}",
            disabled=f"{strong_btn_style.disabled}",

            font_family=f"\"{strong_btn_style.font.family}\"",
            font_size=f"{strong_btn_style.font.size}pt",
            font_weight=f"{strong_btn_style.font.weight}",

            font_color=f"{strong_btn_style.font_color}",
            font_color_checked=f"{strong_btn_style.font_color_checked}",
            font_color_disabled=f"{strong_btn_style.font_color_disabled}",
        )
        self.setStyleSheet(qss)

        # Create the font based on FontConfig
        # Calculate text width using QFontMetrics
        font = QFont(
            strong_btn_style.font.family,
            strong_btn_style.font.size,
            strong_btn_style.font.weight
        )
        font_metrics = QFontMetrics(font)
        self.text_width = font_metrics.horizontalAdvance(self.text())


    def paintEvent(self, event: QPaintEvent) -> None:
        option = QStyleOptionButton()
        self.initStyleOption(option)

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        if DEBUG_GEOMETRY:
            draw_widget_rect(self, painter)

        self.style().drawControl(QStyle.ControlElement.CE_PushButtonBevel, option, painter, self)
        radius = self.theme.default.radius
        state = option.state

        if self._icon is not None:
            # This button has an icon
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

            if not self.text():
                x = (self.width() - self.pixmap_size.width()) // 2

            elif self.layoutDirection() == Qt.LayoutDirection.RightToLeft:
                x = (self.width() + (self.text_width + self.space) - pixmap.width() ) // 2

            else:
                x = (self.width() - self.text_width - self.space - pixmap.width()) // 2

            # Draw centered pixmap if no text
            y = (self.height() - self.pixmap_size.height()) // 2
            painter.drawPixmap(x, y, pixmap)

        # Draw text, better
        if self.text():
            if self._icon:
                if self.layoutDirection() == Qt.LayoutDirection.RightToLeft:
                    alignment = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
                    left = radius + (self.width() - self.text_width - self.space - pixmap.width()) // 2
                    right = left + self.text_width

                else:
                    left = radius + pixmap.width() + self.space
                    right = self.width() - radius
                    alignment = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft

            else:
                left = 0
                right = self.width()
                alignment = Qt.AlignmentFlag.AlignCenter

            text_rect = QRect(left, 0, right - left, self.height() - 4)
            painter.setPen(QColor(
                self.theme.button.font_color
                if state & QStyle.StateFlag.State_Enabled
                else self.theme.button.font_color_disabled
            ))
            painter.drawText(text_rect, alignment, self.text())

        painter.end()


