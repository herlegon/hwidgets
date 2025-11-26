import os
from pprint import pprint
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
    QPointF,
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
        # radius: int,
        # bgd_color: str,
        # border_color: str,
        parent: QWidget = None
    ):
        super().__init__(parent)
        default_style = theme.common

        self.radius = float(default_style.radius)
        self.bgd_color = QColor(default_style.bgd)
        self.border_color = QColor(theme.line_edit.selection)
        self.top_border_color = QColor(default_style.border)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet(stylesheet)

        self.setSpacing(0)
        self.setUniformItemSizes(True)
        self.margin_top = (
            theme.common.height + theme.common.radius + 2
        )
        self.margin_bottom = theme.common.radius


    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        r = QRectF(self.rect())
        r.adjust(0.5, 0, -0.5, -0.5)

        left, top, right, bottom = r.left(), r.top(), r.right(), r.bottom()
        radius = self.radius

        path = QPainterPath()
        path.moveTo(left, top)
        path.lineTo(left, bottom - radius)
        path.quadTo(left, bottom, left + radius, bottom)
        path.lineTo(right - radius, bottom)
        path.quadTo(right, bottom, right, bottom - radius)
        path.lineTo(right, top)

        painter.fillPath(path, self.bgd_color)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        pen = QPen(self.top_border_color, 1)
        painter.setPen(pen)
        top_path = QPainterPath()
        top_path.moveTo(left, top+0.5)
        top_path.lineTo(right, top+0.5)
        painter.drawPath(top_path)

        pen.setColor(self.border_color)
        painter.setPen(pen)
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

        self.theme = theme

        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        )
        self.setFixedHeight(theme.common.height)

        self.setInsertPolicy(QComboBox.InsertPolicy.InsertAtCurrent)
        self.setAcceptDrops(True)

        default_pixmap: QPixmap = load_png_icon(
            "keyboard_arrow_down_20dp_000000_FILL0_wght400_GRAD0_opsz20.png",
            theme.combobox.font_color
        )

        self._pixmaps: dict[str, QPixmap] = {
            "normal" : make_tinted_pixmap(default_pixmap, theme.combobox.font_color),
            "disabled" : make_tinted_pixmap(default_pixmap, theme.line_edit.button_disabled),
        }
        self.border_color = QColor(self.theme.common.border)
        self.border_edition = QColor(self.theme.line_edit.selection)
        self.border_disabled = QColor(self.theme.line_edit.font_color_disabled)

        super().setEditable(True)
        self._update_stylesheet()
        line_edit = self.lineEdit()
        line_edit.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        line_edit.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        line_edit.installEventFilter(self)
        line_edit.setReadOnly(True)

        super().setEditable(False)
        self.installEventFilter(self)

        # adjust to the max wifth of items
        #   currently disabled because of the borders that are not cleaned
        self.adjust_popup_width = False

        # when clicking the first time, the combobox is not shown, bug fix:
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


    def _update_stylesheet(self):
        self.variant = ""
        default_style = self.theme.common
        le_style = self.theme.line_edit

        radius = default_style.radius

        template_subst: dict = dict(
            radius=f"{radius}px",
            padding_left=f"{int(1.5 * radius) - 2}px",
            padding_right=f"{int(1.5 * radius)}px",
            margin_top=f"{radius}px",
            popup_width = f"{self.width()}px",

            item_padding_top = f"2px",
            item_padding_bottom = f"2px",

            window_bgd=self.theme.window_bgd,
            widget_bgd=default_style.bgd,
            hover=f"{le_style.hover}",
            border_color=f"{default_style.border}",
            border_edition=f"{le_style.selection}",

            selection=le_style.selection,
            disabled=le_style.disabled,

            font_family=f"\"{le_style.font.family}\"",
            font_size=f"{le_style.font.size}pt",
            font_color=f"{le_style.font_color}",
            font_color_disabled=f"{le_style.font_color_disabled}",
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
                theme=self.theme,
                parent=self
            )
            self.setView(view)
            self.view().setWindowFlags(Qt.WindowType.Widget)
        else:
            self.view().setStyleSheet(self.popup_qss)


    def _pixmap_rect(self) -> QRect:
        pixmap = self._pixmaps.get("normal")
        if not pixmap:
            return QRect()

        x = self.width() - self.height() - self.theme.common.radius
        button_rect = QRect(x, 0, self.width() - x, self.height())
        return button_rect


    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.isEnabled() and not self.lineEdit():
            self.setCursor(Qt.CursorShape.PointingHandCursor)

        super().mouseMoveEvent(event)


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


        radius = self.theme.common.radius
        popup_width = self.width()
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
            # add 4px because of bottom padding: see qss
            # popup.resize(popup_width, popup.height() + 2 * radius + 4)

        popup.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        popup.setStyleSheet("QFrame { background: transparent; border: none; }")
        popup.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.view().viewport().update()

        if sys.platform == 'win32':
            QTimer.singleShot(0, lambda: popup.resize(popup_width, popup.height() +  radius))
            QTimer.singleShot(0.001, lambda: popup.move(self.mapToGlobal(QPoint(0.5, self.height()))))

        else:
            QTimer.singleShot(0, lambda: popup.resize(popup_width, popup.height() +  radius))
            QTimer.singleShot(0.001, lambda: popup.move(self.mapToGlobal(QPoint(0.5, self.height()))))
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

            elif event.type() == QEvent.Type.ContextMenu:
                return False

        if line_edit and event.type() == QEvent.Type.HoverMove:
            if self._pixmap_rect().contains(event.position().toPoint()):
                self.setCursor(Qt.CursorShape.PointingHandCursor)

        return super().eventFilter(watched, event)


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
        painter.setRenderHints(QPainter.RenderHint.Antialiasing, on=True)
        if DEBUG_GEOMETRY:
            draw_widget_rect(self, painter)

        # Draw centered arrow
        x = self.width() - self.height()
        y = (self.height() - pixmap.height()) // 2
        painter.drawPixmap(x, y, pixmap)


        # Border color
        radius: int = self.theme.common.radius
        border_width = 1.0
        pen = QPen(self.border_color, border_width)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        if self.lineEdit():
            if not self.isEnabled():
                pen.setColor(self.border_disabled)

            elif self.lineEdit().hasFocus():
                pen.setColor(self.border_edition)
        painter.drawRoundedRect(self.rect(), radius, radius)


        # Only draw custom border for non-editable combobox
        if self.view().isVisible():
            pen = QPen(self.border_edition)
            # ensures 1px on any device scaling
            pen.setCosmetic(True)

            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            path = QPainterPath()
            r = QRectF(self.rect())
            r.adjust(0.5, +0.5, -0.5, -0.5)

            left, top, right, bottom = r.left(), r.top(), r.right(), r.bottom()
            path.moveTo(left, bottom)
            path.lineTo(left, top + radius)
            path.quadTo(left, top, left + radius, top)
            path.lineTo(right - radius , top)
            path.quadTo(right, top, right, top + radius)
            path.lineTo(right, bottom)

            # bottom side: no line
            painter.drawPath(path)

        painter.end()

