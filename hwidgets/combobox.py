import os
import sys
from typing import Any
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

from .hstyle import (
    COMBOBOX_HEIGHT,
    COMBOBOX_RADIUS,
    DEBUG_GEOMETRY,
    HStyle,
    draw_widget_rect,

)
from .utils import (
    TITLE_BAR_ICON_PATH,
    load_png_icon,
    load_qss,
    make_tinted_pixmap,
)


class RoundedListView(QListView):
    def __init__(self, stylesheet: str, radius: int, bgd_color: str, parent=None):
        super().__init__(parent)
        self.radius = radius + 1
        self.bgd_color = QColor(bgd_color)
        self.setStyleSheet(stylesheet)
        self.setSpacing(0)
        self.setUniformItemSizes(True)
        self.margin_top = COMBOBOX_HEIGHT + COMBOBOX_RADIUS + 2
        self.margin_bottom = COMBOBOX_RADIUS

    def paintEvent(self, event):
        """Paint rounded background with bottom corners rounded only."""
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.viewport().rect() # .adjusted(0, self.margin_top, 1, -self.margin_bottom)

        if sys.platform == 'win32':
            rect = rect.adjusted(0,0,1,0)
        path = QPainterPath()

        # Only bottom corners rounded
        path.moveTo(rect.topLeft())
        path.lineTo(rect.bottomLeft().x(), rect.bottomLeft().y() - self.radius)
        path.quadTo(rect.bottomLeft(), rect.bottomLeft() + QPoint(self.radius, 0))
        path.lineTo(rect.bottomRight().x() - self.radius, rect.bottomRight().y())
        path.quadTo(rect.bottomRight(), rect.bottomRight() + QPoint(0, -self.radius))
        path.lineTo(rect.topRight())

        painter.fillPath(path, self.bgd_color)
        super().paintEvent(event)



class HComboBox(QComboBox):
    signal_f_selected = Signal(str)


    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        hstyle: HStyle,
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
        self.setFixedHeight(COMBOBOX_HEIGHT)

        self.setInsertPolicy(QComboBox.InsertPolicy.InsertAtCurrent)
        self.setAcceptDrops(True)

        self.hstyle = hstyle
        default_pixmap: QPixmap = load_png_icon(
            os.path.join(
                TITLE_BAR_ICON_PATH,
                "keyboard_arrow_down_20dp_000000_FILL0_wght400_GRAD0_opsz20.png"
            ),
            hstyle.text_color
        )

        self._pixmaps: dict[str, QPixmap] = {
            "normal" : default_pixmap,
            "disabled" : make_tinted_pixmap(default_pixmap, hstyle.disabled_text),
        }

        super().setEditable(True)
        self.set_stylesheet(hstyle=hstyle)
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
        super().setMinimumSize(QSize(size.width(), COMBOBOX_HEIGHT))
        super().setFixedHeight(COMBOBOX_HEIGHT)


    def setMaximumSize(self, size: QSize) -> None:
        super().setMaximumSize(QSize(size.width(), COMBOBOX_HEIGHT))
        super().setFixedHeight(COMBOBOX_HEIGHT)


    def _pixmap_rect(self) -> QRect:
        pixmap = self._pixmaps.get("normal")
        if not pixmap:
            return QRect()

        x = self.width() - self.height() - COMBOBOX_RADIUS
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
            popup_width = max(self.width(), max_text_width + scrollbar_width + padding)

            popup.resize(popup_width, popup.height() + 2 * COMBOBOX_RADIUS)

        else:
            popup.resize(self.width(), popup.height() + 2 * COMBOBOX_RADIUS)

        self.view().viewport().update()

        if sys.platform == 'win32':
            QTimer.singleShot(0, lambda: popup.move(self.mapToGlobal(QPoint(0, self.height()))))

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
                    mouse_event.button() == Qt.MouseButton.LeftButto
                    and line_edit.isReadOnly()
                ):
                    QTimer.singleShot(0, self.showPopup)
                    return True

            if event.type() == QEvent.Type.ContextMenu:
                return False

        return super().eventFilter(watched, event)


    def set_stylesheet(self, hstyle: HStyle):
        self.variant = ""

        template_subst: dict = dict(
            window_bgd=hstyle.window_bgd,
            widget_bgd=hstyle.widget_bgd,
            hover_bgd=hstyle.hover_bgd,
            selection_bgd=hstyle.selection_bgd,
            disabled_bgd=hstyle.disabled_bgd,
            disabled_text=hstyle.disabled_text,
            text_color=hstyle.text_color,
            selected_text=f"{hstyle.selected_text}",
            radius=f"{COMBOBOX_RADIUS}px",
            margin_top=f"{COMBOBOX_RADIUS}px",
            popup_width = f"{self.width()}px",
            padding_left=f"{int(1.5 * COMBOBOX_RADIUS) - 2}px",
            padding_right=f"{int(1.5 * COMBOBOX_RADIUS)}px",
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
                radius=COMBOBOX_RADIUS,
                bgd_color=hstyle.widget_bgd,
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

        if self.lineEdit() and self.lineEdit().hasFocus():
            # Draw rounded rectangle border
            border_color = QColor(self.hstyle.selected)
            border_width = 1
            pen = QPen(border_color, border_width)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(
                self.rect(),
                COMBOBOX_RADIUS,
                COMBOBOX_RADIUS
            )

        painter.end()

