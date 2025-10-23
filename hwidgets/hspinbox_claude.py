from string import Template
from warnings import warn
from PySide6.QtCore import (
    QSize,
    Qt,
    QEvent,
    QTimer,
    QPoint,
    QRect,
)
from PySide6.QtGui import (
    QIcon,
    QColor,
    QFont,
    QPainter,
    QPixmap,
    QPainterPath,
    QPen,
)
from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QSizePolicy,
    QAbstractSpinBox,
    QStyle,
    QStyleOptionSpinBox,
)

from .hstyle import (
    COMBOBOX_RADIUS,
    COMBOBOX_HEIGHT,
    HStyle,
    load_png_icon,
    load_qss,
)



class HDoubleSpinBox(QDoubleSpinBox):

    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        hstyle: HStyle,
        prefix: str | None = None,
        suffix: str | None = None,
        cleanText: str | None = None,
        decimals: int | None = None,
        minimum: float | None = None,
        maximum: float | None = None,
        singleStep: float | None = None,
        stepType: QAbstractSpinBox.StepType | None = None,
        value: float | None = 0,
        custom_buttons: bool | None = True,
    ) -> None:
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(COMBOBOX_HEIGHT)
        self.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        self.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.lineEdit().setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFocusPolicy(Qt.FocusPolicy.WheelFocus)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)


        self.button_width = COMBOBOX_RADIUS + COMBOBOX_HEIGHT // 2

        # State tracking
        self.plus_state = 'normal'  # normal, hover, pressed
        self.minus_state = 'normal'
        self.is_enabled = True



        # Pre-render button pixmaps
        self._button_pixmaps = self._create_button_pixmaps()

        qss_template = Template(load_qss("hdoublespinbox.qss"))
        qss = qss_template.substitute(
            widget_bgd=f"{hstyle.widget_bgd}",
            text_color=f"{hstyle.text_color}",
            radius=f"{COMBOBOX_RADIUS}px",
            hover_bgd=f"{hstyle.hover_bgd}",
            border_color=f"{hstyle.border}",
            disabled_bgd=f"{hstyle.disabled_bgd}",
            disabled_text=f"{hstyle.disabled_text}",
            padding_right=f"{COMBOBOX_RADIUS + COMBOBOX_HEIGHT//2}px",
            editing_border=f"{hstyle.checked}",
            selected_text=f"{hstyle.selected_text}",
            padding=f"{COMBOBOX_RADIUS}px",
            selection_bgd=f"{hstyle.selection_bgd}",
            button_width=f"{20}px",
        )
        self.setStyleSheet(qss)
        self.hstyle = hstyle


    def _create_button_pixmaps(self):
        """Pre-render all button states as pixmaps"""
        pixmaps = {}
        states = {
            'normal': '#e0e0e0',
            'hover': '#d0d0d0',
            'pressed': '#c0c0c0',
            'disabled': '#f0f0f0'
        }

        for state, bg_color in states.items():
            # Create pixmap for plus button
            plus_pixmap = QPixmap(self.button_width, 16)
            plus_pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(plus_pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Draw plus button with top-right corner rounded
            path_plus = QPainterPath()
            rect = QRect(0, 0, self.button_width, 16)
            path_plus.moveTo(rect.left(), rect.top())
            path_plus.lineTo(rect.right() - 6, rect.top())
            path_plus.arcTo(rect.right() - 12, rect.top(), 12, 12, 90, -90)
            path_plus.lineTo(rect.right(), rect.bottom())
            path_plus.lineTo(rect.left(), rect.bottom())
            path_plus.closeSubpath()
            painter.fillPath(path_plus, QColor(bg_color))

            # Draw plus text
            text_color = '#a0a0a0' if state == 'disabled' else '#404040'
            painter.setPen(QPen(QColor(text_color)))
            font = QFont()
            font.setPixelSize(14)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, "+")
            painter.end()

            # Create pixmap for minus button
            minus_pixmap = QPixmap(self.button_width, 16)
            minus_pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(minus_pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Draw minus button with bottom-right corner rounded
            path_minus = QPainterPath()
            rect = QRect(0, 0, self.button_width, 16)
            path_minus.moveTo(rect.left(), rect.top())
            path_minus.lineTo(rect.right(), rect.top())
            path_minus.lineTo(rect.right(), rect.bottom() - 6)
            path_minus.arcTo(rect.right() - 12, rect.bottom() - 12, 12, 12, 0, -90)
            path_minus.lineTo(rect.left(), rect.bottom())
            path_minus.closeSubpath()
            painter.fillPath(path_minus, QColor(bg_color))

            # Draw minus text
            painter.setPen(QPen(QColor(text_color)))
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, "-")
            painter.end()

            pixmaps[f'plus_{state}'] = plus_pixmap
            pixmaps[f'minus_{state}'] = minus_pixmap

        return pixmaps

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        rect = self.rect()
        btn_w = self.button_width
        half_height = rect.height() // 2

        # Determine which pixmaps to use based on enabled state
        plus_key = f'plus_{self.plus_state if self.isEnabled() else "disabled"}'
        minus_key = f'minus_{self.minus_state if self.isEnabled() else "disabled"}'

        # Draw plus button pixmap
        plus_pos = QPoint(rect.width() - btn_w, 0)
        painter.drawPixmap(plus_pos, self._button_pixmaps[plus_key])

        # Draw minus button pixmap
        minus_pos = QPoint(rect.width() - btn_w, half_height)
        painter.drawPixmap(minus_pos, self._button_pixmaps[minus_key])


    def _get_button_at_pos(self, pos):
        """Determine which button (if any) is at the given position"""
        rect = self.rect()
        btn_w = self.button_width

        if pos.x() > rect.width() - btn_w:
            half_height = rect.height() // 2
            if pos.y() < half_height:
                return 'plus'
            else:
                return 'minus'
        return None


    def mousePressEvent(self, event):
        if not self.isEnabled():
            super().mousePressEvent(event)
            return

        pos = event.position().toPoint()
        button = self._get_button_at_pos(pos)

        if button == 'plus':
            self.plus_state = 'pressed'
            self.update()
            self.stepUp()
        elif button == 'minus':
            self.minus_state = 'pressed'
            self.update()
            self.stepDown()
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if not self.isEnabled():
            super().mouseReleaseEvent(event)
            return

        pos = event.position().toPoint()
        button = self._get_button_at_pos(pos)

        # Reset to hover if still over button, otherwise normal
        if button == 'plus':
            self.plus_state = 'hover'
        else:
            self.plus_state = 'normal'

        if button == 'minus':
            self.minus_state = 'hover'
        else:
            self.minus_state = 'normal'

        self.update()
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if not self.isEnabled():
            super().mouseMoveEvent(event)
            return

        pos = event.position().toPoint()
        button = self._get_button_at_pos(pos)

        # Update hover states
        new_plus_state = 'hover' if button == 'plus' else 'normal'
        new_minus_state = 'hover' if button == 'minus' else 'normal'

        # Only update if state changed
        if new_plus_state != self.plus_state or new_minus_state != self.minus_state:
            self.plus_state = new_plus_state
            self.minus_state = new_minus_state
            self.update()

        super().mouseMoveEvent(event)

    def enterEvent(self, event):
        self.setMouseTracking(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Reset to normal when mouse leaves widget
        if self.plus_state != 'normal' or self.minus_state != 'normal':
            self.plus_state = 'normal'
            self.minus_state = 'normal'
            self.update()
        self.setMouseTracking(False)
        super().leaveEvent(event)

    def changeEvent(self, event):
        # Handle enabled/disabled state changes
        if event.type() == event.Type.EnabledChange:
            self.update()
        super().changeEvent(event)


class HSpinBox(HDoubleSpinBox):
    ...










