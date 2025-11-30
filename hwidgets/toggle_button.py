from pprint import pprint
from string import Template
from typing import Type

from .styles import Theme
from .debug import (
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
    QRect,
)
from PySide6.QtGui import (
    QIcon,
    QPixmap,
    QPainter,
    QColor,
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



class HToggleButton(QPushButton):

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
        self._is_grayscale: bool = False
        self.useGreyscale(False)

        self.setCheckable(True)

        self._icon = None
        self.text_width = 0
        # space between icon and text
        self._spacing: int = 12
        self._cached_size: QSize = None

        if text is not None:
            self.setText(text)
        if icon is not None:
            self.setIcon(icon)
        self._pixmaps = {}

        self.populate_pixmaps()
        self._update_stylesheet()


    def spacing(self) -> None:
        return self._spacing


    def setSpacing(self, spacing: int) -> None:
        self._spacing = spacing


    def isGrayscale(self) -> bool:
        return self._is_grayscale


    def setCheckable(self, b: bool):
        super().setCheckable(b)
        if b:
            self.btn_style = (
                self.theme.toggle_grey_button
                if self.isGrayscale()
                else self.theme.toggle_button
            )

        else:
            self.btn_style = (
                self.theme.strong_grey_button
                if self.isGrayscale()
                else self.theme.strong_button
            )


    def useGreyscale(self, b: bool) -> None:
        self._is_grayscale = b
        if self.isCheckable():
            self.btn_style = (
                self.theme.toggle_grey_button if b else self.theme.toggle_button
            )

        else:
            self.btn_style = (
                self.theme.strong_grey_button if b else self.theme.strong_button
            )


    def _recalculate_size(self) -> None:
        """Recalculate the width and height of the button and store it in cache."""
        radius: int = self.theme.default.radius
        height: int = self.btn_style.height

        if self.text():
            text_width = self.fontMetrics().horizontalAdvance(self.text())
            if self._icon:
                icon_width = height
                total_width = radius + icon_width + self._spacing + text_width + radius
            else:
                total_width = 2 * radius + text_width + self._spacing

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

        normal = QColor(self.btn_style.font_color)
        pressed = QColor(self.btn_style.font_color)
        disabled = QColor(self.btn_style.font_color_disabled)
        hover = QColor(self.btn_style.font_color)

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
        btn_style = self.btn_style
        default_style = self.theme.default
        self.setFixedHeight(btn_style.height)

        qss_template = Template(load_qss("button.qss"))
        qss = qss_template.substitute(
            radius=f"{radius}px",
            margin_left=f"{radius + default_style.height + 6}px",
            padding=f"{btn_style.padding}px",

            widget_bgd=f"{btn_style.bgd}",

            hover=f"{btn_style.hover}",
            pressed=f"{btn_style.pressed}",
            checked=f"{btn_style.checked}",
            disabled=f"{btn_style.disabled}",

            font_color=f"{btn_style.font_color}",
            font_color_disabled=f"{btn_style.font_color_disabled}",
        )
        self.setStyleSheet(qss)
        self.setFont(btn_style.font.make_font())
        self.text_width = self.fontMetrics().horizontalAdvance(self.text())

        self.font_color = btn_style.font_color
        self.font_color_disabled = btn_style.font_color_disabled


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
                x = (self.width() + (self.text_width + self._spacing) - pixmap.width() ) // 2

            else:
                x = (self.width() - self.text_width - self._spacing - pixmap.width()) // 2

            # Draw centered pixmap if no text
            y = (self.height() - self.pixmap_size.height()) // 2
            painter.drawPixmap(x, y, pixmap)

        # Draw text, better
        if self.text():
            if self._icon:
                if self.layoutDirection() == Qt.LayoutDirection.RightToLeft:
                    alignment = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
                    left = radius + (self.width() - self.text_width - self._spacing - pixmap.width()) // 2
                    right = left + self.text_width

                else:
                    left = radius + pixmap.width() + self._spacing
                    right = self.width() - radius
                    alignment = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft

            else:
                left = 0
                right = self.width()
                alignment = Qt.AlignmentFlag.AlignCenter

            height = (
                self.height() - 2
                if isinstance(self, HToggleButton | HToggleGreyButton)
                else self.height()
            )
            text_rect = QRect(left, 0, right - left, height)
            painter.setPen(QColor(
                self.font_color
                if state & QStyle.StateFlag.State_Enabled
                else self.font_color_disabled
            ))
            painter.drawText(text_rect, alignment, self.text())

        painter.end()




class HToggleGreyButton(HToggleButton):

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
        super().__init__(
            parent,
            icon=icon,
            text=text,
            theme=theme,
            autoDefault=autoDefault,
            default=default,
            flat=flat
        )

        self.useGreyscale(True)
