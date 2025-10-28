
import os
import sys
import time
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
    QFont,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QMouseEvent,
    QPixmap,
    QFocusEvent,
    QShowEvent,
)
from PySide6.QtWidgets import (
    QComboBox,
    QSizePolicy,
    QStyle,
    QWidget,
    QListView,
    QStyleOptionComboBox,
    QStyle,
    QApplication,
)
from string import Template


from hutils import blue, lightcyan, lightgreen, lightgrey, orange, parent_directory, purple, red, yellow
from .hstyle import (
    COMBOBOX_HEIGHT,
    COMBOBOX_RADIUS,
    DEBUG_GEOMETRY,
    TITLE_BAR_ICON_PATH,
    HStyle,
    draw_widget_rect,
    load_png_icon,
    load_qss,
    make_tinted_pixmap,
)
from .logger import hlogger



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

        self.setEditable(True)
        self.set_stylesheet(hstyle=hstyle)
        self.setEditable(False)
        # if self.lineEdit():
        #     self.lineEdit().setMouseTracking(True)
        #     self.lineEdit().installEventFilter(self)
        # self.installEventFilter(self)


    def setEditable(self, editable: bool) -> None:
        # print(f"{self.objectName()} set editable: {editable}")
        was_editable = self.isEditable()

        super().setEditable(editable)

        # Reinstall event filter if lineEdit changed
        if self.lineEdit() and was_editable != editable:
            line_edit = self.lineEdit()
            line_edit.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            line_edit.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
            line_edit.removeEventFilter(self)
            line_edit.installEventFilter(self)
            line_edit.setReadOnly(not editable)


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
            print(red("edrftvgbhynj,k"))
            return

        # Make the popup a frameless popup and allow transparent background on the window.
        # On Windows this generally works; on some Linux setups true transparency may be
        # limited — but we don't require transparency, because the view draws the background.
        is_editable = self.isEditable()
        self.setEditable(True)
        flags = popup.windowFlags()
        popup.setWindowFlags(flags | Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        popup.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        popup.setStyleSheet("QFrame { background: transparent; border: none; }")

        # Resize
        popup.resize(self.width(), popup.height() + 2 * COMBOBOX_RADIUS)

        self.view().viewport().update()

        if sys.platform == 'linux':
            QTimer.singleShot(0, lambda: popup.move(self.mapToGlobal(QPoint(0, self.height()))))
            super().showPopup()
        else:
            popup.move(self.mapToGlobal(QPoint(0, self.height())))

        self.setEditable(is_editable)


    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        event_type: QEvent.Type = event.type()

        # print(watched, event)
        if watched == self.lineEdit():
            line_edit = self.lineEdit()

            if line_edit.isReadOnly():
                if (
                    event_type == QEvent.Type.Leave
                    and line_edit.isReadOnly()
                ):
                    return True

                if (
                    event_type == QEvent.Type.MouseButtonPress
                    and line_edit.isReadOnly()
                ):
                    print("show popup")
                    # pos_in_combo = line_edit.mapTo(self, event.pos())
                    # new_event = QMouseEvent(
                    #     QEvent.Type.MouseButtonPress,
                    #     pos_in_combo,
                    #     Qt.MouseButton.LeftButton,
                    #     Qt.MouseButton.LeftButton,
                    #     Qt.KeyboardModifier.NoModifier,
                    # )
                    # QApplication.sendEvent(self, new_event)
                    QTimer.singleShot(0, self.showPopup)
                    return True

                if (
                    event_type == QEvent.Type.MouseButtonRelease
                    and line_edit.isReadOnly()
                ):
                    print("released")
                    QTimer.singleShot(0, self.showPopup)
                    return True


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

        # if state & QStyle.StateFlag.State_Sunken:
        #     print(lightcyan(f"CB pressed"))

        # elif state & QStyle.StateFlag.State_On:
        #     print(lightcyan(f"CB checked"))

        # elif state & QStyle.StateFlag.State_MouseOver:
        #     print(lightcyan(f"CB hover"))

        # if state & QStyle.StateFlag.State_Active:
        #     print(lightcyan(f"Active"))


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

