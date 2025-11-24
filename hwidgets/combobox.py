import os
import sys
from typing import Any, Type
from PySide6.QtCore import (
    QObject,
    QPoint,
    Signal,
    QSize,
    QObject,
    Qt,
    QSize,
    QEvent,
    QRect,
    QSize,
    QTimer,
    QRectF,
)
from PySide6.QtGui import (
    QPen,
    QColor,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QMouseEvent,
    QPixmap,
    QFontMetrics,
    QCursor,
)
from PySide6.QtWidgets import (
    QMenu,
    QApplication,
    QComboBox,
    QSizePolicy,
    QStyle,
    QWidget,
    QListView,
    QStyleOptionComboBox,
    QStyle,
)
from string import Template

from .style_manager import Theme

from .hstyle import (
    DEBUG_GEOMETRY,
    draw_widget_rect,
)
from .utils import (
    TITLE_BAR_ICON_PATH,
    load_png_icon,
    load_qss,
    make_tinted_pixmap,
)


class RoundedListView(QListView):
    def __init__(
        self,
        stylesheet: str,
        theme: Theme,
        radius: int,
        bgd_color: str,
        border_color: str,
        parent: QWidget = None
    ):
        super().__init__(parent)
        self.radius = float(radius)
        self.bgd_color = QColor(bgd_color)
        self.border_color  = QColor(border_color)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet(stylesheet)

        self.setSpacing(0)
        self.setUniformItemSizes(True)
        self.margin_top = (
            theme.common.height + theme.common.radius + 2
        )
        self.margin_bottom = theme.common.radius


    def paintEvent(self, event):
        """Paint rounded background with bottom corners rounded only."""
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.viewport().rect())
        if sys.platform == 'win32':
            rect.adjust(0, 0, -0.5, -0.5)
        path = QPainterPath()

        # Only bottom corners rounded
        path.moveTo(rect.topLeft())
        path.lineTo(rect.bottomLeft().x(), rect.bottomLeft().y() - self.radius)
        path.quadTo(rect.bottomLeft(), rect.bottomLeft() + QPoint(self.radius, 0))
        path.lineTo(rect.bottomRight().x() - self.radius, rect.bottomRight().y())
        path.quadTo(rect.bottomRight(), rect.bottomRight() + QPoint(0, -self.radius))
        path.lineTo(rect.topRight())

        painter.fillPath(path, self.bgd_color)

        pen = QPen(self.border_color, 2.0)
        pen.setCosmetic(True)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        painter.drawPath(path)

        super().paintEvent(event)



class HComboBox(QComboBox):
    signal_f_selected = Signal(str)

    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        theme: Type[Theme],
        editable: bool | None = ...,
        count: int | None = ...,
        currentText: str | None = ...,
        currentIndex: int | None = ...,
        currentData: Any | None = ...,
        maxVisibleItems: int | None = ...,
        maxCount: int | None = ...,
        insertPolicy: QComboBox.InsertPolicy | None = ...,
        sizeAdjustPolicy: QComboBox.SizeAdjustPolicy | None = ...,
        minimumContentsLength: int | None = ...,
        iconSize: QSize | None = ...,
        placeholderText: str | None = ...,
        duplicatesEnabled: bool | None = ...,
        frame: bool | None = ...,
        modelColumn: int | None = ...,
        labelDrawingMode: QComboBox.LabelDrawingMode | None = ...,
    ) -> None:
        super().__init__(parent)

        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        )
        self.setFixedHeight(theme.common.height)

        self.setInsertPolicy(QComboBox.InsertPolicy.InsertAtCurrent)
        self.setAcceptDrops(True)

        self.theme = theme
        default_pixmap: QPixmap = load_png_icon(
            os.path.join(
                TITLE_BAR_ICON_PATH,
                "keyboard_arrow_down_20dp_000000_FILL0_wght400_GRAD0_opsz20.png"
            ),
            theme.combobox.font_color
        )

        self._pixmaps: dict[str, QPixmap] = {
            "normal" : make_tinted_pixmap(default_pixmap, theme.combobox.normal),
            "disabled" : make_tinted_pixmap(default_pixmap, theme.combobox.disabled),
        }

        super().setEditable(True)
        self.set_stylesheet(theme=theme)
        line_edit = self.lineEdit()
        line_edit.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        line_edit.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        line_edit.installEventFilter(self)
        line_edit.setReadOnly(True)

        # fix bug: when clicking the first time on the combobox, the popu is not showed
        self.adjust_popup_width = True
        self.showPopup()
        self.hidePopup()


    def setEditable(self, editable: bool) -> None:
        super().setEditable(editable)
        line_edit = self.lineEdit()
        if line_edit and editable:
            line_edit.setReadOnly(False)


    def setMinimumSize(self, size: QSize) -> None:
        height: int = self.theme.common.height
        super().setMinimumSize(QSize(size.width(), height))
        super().setFixedHeight(height)


    def setMaximumSize(self, size: QSize) -> None:
        height: int = self.theme.common.height
        super().setMaximumSize(QSize(size.width(), height))
        super().setFixedHeight(height)


    def _pixmap_rect(self) -> QRect:
        pixmap = self._pixmaps.get("normal")
        if not pixmap:
            return QRect()

        x = self.width() - self.height() - self.theme.common.radius
        button_rect = QRect(x, 0, self.width() - x, self.height())
        return button_rect


    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.isEnabled() and self.lineEdit() and not self.lineEdit().isReadOnly():
            if self._pixmap_rect().contains(event.position().toPoint()):
                self.setCursor(Qt.CursorShape.ArrowCursor)
            else:
                self.setCursor(Qt.CursorShape.IBeamCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

        super().mouseMoveEvent(event)


    def leaveEvent(self, event: QEvent) -> None:
        """Reset cursor when leaving the widget"""
        # print(f"{self.objectName()}: leaveEvent")
        self.unsetCursor()
        super().leaveEvent(event)


    def showPopup(self):
        if sys.platform != 'linux':
            super().showPopup()
        popup = self.view().window()
        if not popup:
            return

        # Make the popup a frameless popup and allow transparent background on the window.
        # On Windows this generally works; on some Linux setups true transparency may be
        # limited — but we don't require transparency, because the view draws the background.
        is_editable = self.isEditable()
        self.setEditable(True)
        flags = popup.windowFlags()
        popup.setWindowFlags(
            flags
            | Qt.WindowType.Popup
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.NoDropShadowWindowHint
        )
        popup.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        popup.setStyleSheet("QFrame { background: transparent; border: none; }")
        popup.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        if self.adjust_popup_width:
            fm = QFontMetrics(self.font())
            # Measure the longest text width among all items
            max_text_width = max(
                (fm.horizontalAdvance(self.itemText(i)) for i in range(self.count())),
                default=self.width()
            )

            # Add padding for icon + scrollbar + margins
            scrollbar_width = self.style().pixelMetric(QStyle.PixelMetric.PM_ScrollBarExtent)
            padding = 20  # general horizontal padding
            popup_width = max(self.width(), max_text_width + scrollbar_width + padding) + 2
            popup.resize(popup_width, popup.height() + 2 * self.theme.common.radius)

        else:
            popup.resize(self.width(), popup.height() + 2 * self.theme.common.radius)

        self.view().viewport().update()

        if sys.platform == 'win32':
            QTimer.singleShot(0, lambda: popup.move(self.mapToGlobal(QPoint(-1, self.height() - 1))))

        else:
            QTimer.singleShot(0, lambda: popup.move(self.mapToGlobal(QPoint(0, self.height()))))
            super().showPopup()

        self.setEditable(is_editable)


    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.RightButton:
            # Create menu
            menu = QMenu(self)
            menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
            menu.setWindowFlags(menu.windowFlags() | Qt.WindowType.FramelessWindowHint)

            # Add actions
            copy_action = menu.addAction("Copy")
            copy_action.triggered.connect(lambda: QApplication.clipboard().setText(self.currentText()))

            # Style
            if False:
                menu.setStyleSheet("""
                    QMenu {
                        background-color: #2b2b2b;
                        border-radius: 8px;
                        padding: 6px;
                        border: 1px solid #444;
                    }
                    QMenu::item {
                        color: white;
                        padding: 6px 16px;
                        border-radius: 6px;
                    }
                    QMenu::item:selected {
                        background-color: #3c7dd9;
                    }
                """)

                # Optional: custom rounded mask for shadowless transparency
                menu_rect = menu.rect()
                path = QPainterPath()
                path.addRoundedRect(menu_rect, 8, 8)
                region = path.toFillPolygon().toPolygon()
                menu.setMask(region)

                menu.exec(QCursor.pos())
            else:
                menu = QMenu(self)
                copy_action = menu.addAction("Copy")
                copy_action.triggered.connect(
                    lambda: QApplication.clipboard().setText(self.currentText())
                )
                menu.exec(event.globalPos())
            return

        super().mousePressEvent(event)


    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        line_edit = self.lineEdit()
        if watched == line_edit and line_edit:
            if event.type() == QEvent.Type.MouseButtonPress:
                mouse_event: QMouseEvent = event
                if (
                    mouse_event.button() == Qt.MouseButton.LeftButton
                    and line_edit.isReadOnly()
                ):
                    QTimer.singleShot(0, self.showPopup)
                    return True

            if event.type() == QEvent.Type.ContextMenu:
                return False

        return super().eventFilter(watched, event)


    def set_stylesheet(self, theme: Type[Theme]):
        self.variant = ""
        radius = theme.common.radius

        template_subst: dict = dict(
            window_bgd=theme.window_bgd,
            widget_bgd=theme.common.bgd,
            hover_bgd=theme.combobox.hover,
            selection_bgd=theme.combobox.selection,
            disabled_bgd=theme.combobox.disabled,

            font_color_disabled=theme.combobox.font_color_disabled,
            font_color=theme.combobox.font_color,
            selected_text=f"{theme.combobox.font_color_selected}",
            radius=f"{radius}px",
            margin_top=f"{radius}px",
            popup_width = f"{self.width()}px",
            padding_left=f"{int(1.5 * radius) - 2}px",
            padding_right=f"{int(1.5 * radius)}px",
            border_color=f"{theme.border}",
            font_family=f"\"{theme.combobox.font.family}\"",
            font_size=f"{theme.combobox.font.size}pt",
        )

        qss_template = Template(load_qss("combobox.qss", variant=self.variant))
        qss = qss_template.substitute(**template_subst)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(qss)

        qss_template = Template(load_qss("combobox_lineedit.qss", variant=self.variant))
        qss = qss_template.substitute(**template_subst)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.lineEdit().setStyleSheet(qss)

        qss_template = Template(load_qss("combobox_abstractitemview.qss", variant=self.variant))
        self.popup_qss = qss_template.substitute(**template_subst)

        if sys.platform in ('win32', 'linux'):
            view = RoundedListView(
                stylesheet=self.popup_qss,
                radius=theme.common.radius,
                bgd_color=theme.common.bgd,
                border_color=theme.common.border,
                parent=self
            )
            self.setView(view)
            self.view().setWindowFlags(Qt.WindowType.Widget)
        else:
            self.view().setStyleSheet(self.popup_qss)




    def paintEvent(self, e: QPaintEvent) -> None:
        super().paintEvent(e)

        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)

        state = opt.state
        if not (state & QStyle.StateFlag.State_Enabled):
            pixmap = self._pixmaps["disabled"]
        else:
            pixmap = self._pixmaps["normal"]

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        if DEBUG_GEOMETRY:
            draw_widget_rect(self, painter)

        # Draw centered pixmap
        x = self.width() - self.height()
        y = (self.height() - pixmap.height()) // 2
        painter.drawPixmap(x, y, pixmap)

        radius: int = self.theme.common.radius
        if self.lineEdit() and self.lineEdit().hasFocus():
            # Draw rounded rectangle border
            border_color = QColor(self.theme.common.border_selected)
            border_width = 1
            pen = QPen(border_color, border_width)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(self.rect(), radius, radius)

        # Only draw custom border for non-editable combobox
        if not self.isEditable() and self.view().isVisible():
            border_color = QColor(self.theme.border_selected)
            border_width = 2.0

            pen = QPen(border_color, border_width)
            # ensures 1px on any device scaling
            pen.setCosmetic(True)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            r = QRectF(self.rect())
            r.adjust(1, 0, 0, 0)  # align to pixel grid

            path = QPainterPath()
            path.moveTo(r.left(), r.bottom())                   # start bottom-left
            path.lineTo(r.left(), r.top() + radius)             # left side
            path.quadTo(r.left(), r.top(), r.left() + radius, r.top())  # top-left corner
            path.lineTo(r.right() - radius, r.top())            # top side
            path.quadTo(r.right(), r.top(), r.right(), r.top() + radius)  # top-right corner
            path.lineTo(r.right(), r.bottom())                  # right side
            # bottom side left open (no bottom border)

            painter.drawPath(path)

        painter.end()

