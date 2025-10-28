
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
)
from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QMouseEvent,
    QPixmap,
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
        # self.setMouseTracking(True)
        # self.viewport().setMouseTracking(True)
        self.margin_top = COMBOBOX_RADIUS
        self.margin_bottom = COMBOBOX_RADIUS
        self.installEventFilter(self)

    # def mouseReleaseEvent(self, e):
    #     print("released from RoundedListView")
    #     return super().mouseReleaseEvent(e)


    # def eventFilter(self, watched: QObject, event: QEvent) -> bool:
    #     event_type: QEvent.Type = event.type()
    #     print(red(f"{int(time.time())} RoundedListView:"), event)
    #     return super().eventFilter(watched, event)

    def paintEvent(self, event):
        """Paint rounded background with bottom corners rounded only."""
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.viewport().rect().adjusted(0, self.margin_top, 1, -self.margin_bottom)
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
        if self.lineEdit():
            self.lineEdit().setReadOnly(True)
            # self.lineEdit().setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self.lineEdit().setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self.set_stylesheet(hstyle=hstyle)

        self.can_hide: bool = False
        self.is_popup_visible = False
        self.counter: int = 0

        self.setMouseTracking(True)
        if self.lineEdit():
            self.lineEdit().setMouseTracking(True)
            self.lineEdit().installEventFilter(self)
        self.installEventFilter(self)


    def setEditable(self, editable: bool) -> None:
        print(f"{self.objectName()} set editable: {editable}")
        if self.lineEdit():
            self.lineEdit().setReadOnly(not editable)
            self.lineEdit().setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, not editable)

        return super().setEditable(editable)


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




    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        event_type: QEvent.Type = event.type()

        # if watched == self.lineEdit():
        #     if (
        #         event_type == QEvent.Type.MouseButtonPress
        #         and event.button() == Qt.MouseButton.LeftButton
        #         and self.lineEdit()
        #         and self.lineEdit().isReadOnly()
        #     ):
        #         print(lightgreen(f"{int(time.time())} CB MouseButtonPress"))
        #         self.showPopup()
        #         self.mousePressEvent(event)
        #         return True

        #     elif (
        #         event_type == QEvent.Type.MouseButtonRelease
        #         # and event.button() == Qt.MouseButton.LeftButton
        #         and self.lineEdit()
        #         and self.lineEdit().isReadOnly()
        #     ):
        #         return True

        if (
            watched == self.lineEdit()
            and event.type() == QEvent.Type.MouseButtonPress
            and self.lineEdit().isReadOnly()
        ):
            print("here")
            pos_in_combo = self.lineEdit().mapTo(self, event.pos())
            new_event = QMouseEvent(
                QEvent.Type.MouseButtonPress,
                pos_in_combo,
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.LeftButton,
                Qt.KeyboardModifier.NoModifier,
            )
            QApplication.sendEvent(self, new_event)
            return True


        if False:
            if (
                watched == self
                and event.type() == QEvent.Type.MouseButtonPress
                and self.lineEdit().isReadOnly()
            ):
                # Let QComboBox handle normally — this opens popup and keeps it open
                print("Pressed on combo")
                if not self.view().isVisible():
                    self.showPopup()
                else:
                    self.hidePopup()
                return True
                # return super().eventFilter(watched, event)

            if (
                watched == self
                and event.type() == QEvent.Type.MouseButtonRelease
                and self.lineEdit().isReadOnly()
            ):
                return True


        return super().eventFilter(watched, event)


        if self.lineEdit() and not self.lineEdit().isReadOnly():
            # print(red("discard because rw"))
            return super().eventFilter(watched, event)

        if watched == self.lineEdit():

            if (
                event_type == QEvent.Type.MouseButtonPress
                and event.button() == Qt.MouseButton.LeftButton
                and self.lineEdit()
                and self.lineEdit().isReadOnly()
            ):
                print(lightgreen(f"{int(time.time())} CB MouseButtonPress"))
                if not self.view().isVisible():
                    self.showPopup()
                else:
                    self.hidePopup()
                return True  # Event handled, don't propagate

            elif (
                event_type == QEvent.Type.MouseButtonRelease
                and self.lineEdit()
                and self.lineEdit().isReadOnly()
            ):
                # 🛑 Returning True here (consuming the Release event)
                # is what's making the popup disappear instantly.
                # event.accept()
                return True


        return super().eventFilter(watched, event)



        # if watched == self.lineEdit() and self.lineEdit().isReadOnly():
        #     print(lightgreen(f"{int(time.time())} "), event)
        #     if event_type not in (
        #         QEvent.Type.Paint,
        #         QEvent.Type.UpdateLater,
        #     ):
        #         print(lightgreen(f"{int(time.time())} VIEW:"), event)

        #     else:
        #         print(lightgreen(f"{int(time.time())} VIEW:"), event)
        # if (
        #     event_type == QEvent.Type.MouseButtonRelease
        #     and event.button() == Qt.MouseButton.LeftButton
        #     and self.lineEdit()
        #     and self.lineEdit().isReadOnly()
        # ):
        # print(red(f"{watched}"), event)

        # if watched == self.lineEdit():
        #     if (
        #         event_type == QEvent.Type.MouseButtonPress
        #         and event.button() == Qt.MouseButton.LeftButton
        #         and self.lineEdit()
        #         and self.lineEdit().isReadOnly()
        #     ):
        #         print(lightgreen(f"{int(time.time())} CB MouseButtonPress"))
        #         self.showPopup()
        #         return True

        #     elif (
        #         event_type == QEvent.Type.MouseButtonRelease
        #         and event.button() == Qt.MouseButton.LeftButton
        #         and self.lineEdit()
        #         and self.lineEdit().isReadOnly()
        #     ):
        #         return True

        #     elif event.type() == QEvent.Type.MouseMove and not self.lineEdit().isReadOnly():
        #         # Convert lineEdit position to combobox coordinates
        #         # global_pos = self.lineEdit().mapToGlobal(event.pos())
        #         # local_pos = self.mapFromGlobal(global_pos)
        #         print(self._pixmap_rect())
        #         print(event.position().toPoint())
        #         if self._pixmap_rect().contains(event.position().toPoint()):
        #             self.lineEdit().setCursor(Qt.CursorShape.ArrowCursor)
        #         elif not self.lineEdit().isReadOnly():
        #             self.lineEdit().setCursor(Qt.CursorShape.IBeamCursor)
        #         else:
        #             self.lineEdit().setCursor(Qt.CursorShape.ArrowCursor)

        #     if event_type == QEvent.Type.Leave:
        #         self.lineEdit().unsetCursor()


        # if watched == self:
        #     if (
        #         event_type in (
        #             QEvent.Type.FocusAboutToChange,
        #             QEvent.Type.FocusIn,
        #             QEvent.Type.FocusOut,
        #         )
        #         and self.lineEdit()
        #         and self.lineEdit().isReadOnly()
        #     ):
        #         print(lightgreen(f"{int(time.time())} CB Foucs"))
        #         return True

        #     elif (
        #         event_type == QEvent.Type.MouseButtonPress
        #         and event.button() == Qt.MouseButton.LeftButton
        #         and self.lineEdit()
        #         and self.lineEdit().isReadOnly()
        #     ):
        #         print(lightgreen(f"{int(time.time())} CB MouseButtonPress"))
        #         return True

            # else:
            #     print(lightcyan(f"\n{int(time.time())} CB:"), event)

        # if watched == self.lineEdit():
        #     if (
        #         event_type == QEvent.Type.MouseButtonRelease
        #         and event.button() == Qt.MouseButton.LeftButton
        #     ):
        #         print(lightgreen(f"{int(time.time())} LE MouseButtonRelease"))
        #         print(f"\n    can_hide: {self.can_hide}")
        #         return True


        #     elif (
        #         event_type == QEvent.Type.MouseButtonPress
        #         and event.button() == Qt.MouseButton.LeftButton
        #     ):
        #         print(lightgreen(f"{int(time.time())} LE MouseButtonPress"))
        #         self.lineEdit().deselect()
        #         if self.isEnabled():
        #             if not self.view().isVisible():
        #                 self.can_hide = False
        #                 self.showPopup()
        #                 # print(f" lets open, can't hide now")
        #                 return True
        #             return True

        #     elif event_type == QEvent.Type.HoverLeave:
        #         print(yellow(f"{int(time.time())} lineedit: HoverLeave, can_hide: {self.can_hide}"))
        #         if self.view().isVisible():
        #             print(f"  is visible")
        #             self.can_hide = True

        #     # else:
        #     #     print(yellow(f"{int(time.time())} LE:"), event)

        # elif watched == self:
        # #     if event_type == QEvent.Type.InputMethodQuery:
        # #         print(f"{lightcyan(f"{int(time.time())} CB: InputMethodQuery")}")
        # #         print(f"{event}")
        # #         if self.view().isVisible() and self.is_popup_visible:
        # #             print(" is visible")
        # #             if self.counter > 0:
        # #                 print(" counter > 1, hide popup")
        # #                 self.can_hide = True
        # #                 self.counter = 0
        # #                 self.hidePopup()
        # #             else:
        # #                 self.counter += 1

        #     if (
        #         event_type == QEvent.Type.MouseButtonPress
        #         and event.button() == Qt.MouseButton.LeftButton
        #         and self.lineEdit()
        #         and self.lineEdit().isReadOnly()
        #     ):
        #         print(lightgreen(f"{int(time.time())} CB MouseButtonPress"))
        #         self.showPopup()
        #         return True
                # self.lineEdit().deselect()
                # if self.isEnabled():
                #     if not self.view().isVisible():
                #         self.can_hide = True
                #         self.showPopup()
                #         # print(f" lets open, can't hide now")
                #         return True

            # else:
            #     print(lightcyan(f"{int(time.time())} CB:"), event)


        # else:
        #     print(blue(f"unknown:"), event)


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

        popup = self.view().window()
        flags = popup.windowFlags()
        popup.setWindowFlags(flags | Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        popup.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        popup.setStyleSheet("QFrame { background: transparent; border: none; }")
        popup.resize(self.width(), popup.height() + 2 * COMBOBOX_RADIUS)
        self.view().setGeometry(0, 0, popup.width(), popup.height())
        self.view().viewport().update()




    def paintEvent(self, e: QPaintEvent) -> None:
        super().paintEvent(e)

        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)

        state = opt.state
        if not (state & QStyle.StateFlag.State_Enabled):
            pixmap = self._pixmaps["disabled"]
        else:
            pixmap = self._pixmaps["normal"]

        if state & QStyle.StateFlag.State_Sunken:
            print(lightcyan(f"CB pressed"))

        elif state & QStyle.StateFlag.State_On:
            print(lightcyan(f"CB checked"))

        elif state & QStyle.StateFlag.State_MouseOver:
            print(lightcyan(f"CB hover"))


        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        if DEBUG_GEOMETRY:
            draw_widget_rect(self, painter)

        # Draw centered pixmap
        x = self.width() - self.height()
        y = (self.height() - pixmap.height()) // 2
        painter.drawPixmap(x, y, pixmap)
        # print(f"draw: {QRect(x, y, pixmap.width(), pixmap.height())}")


        painter.end()


    # def showPopup(self):
    #     if self.lineEdit() and not self.lineEdit().isReadOnly():
    #         print(f"{self.objectName()} editable: forward to super")
    #         super().showPopup()
    #         return

    #     self.can_hide = False

    #     if sys.platform == 'win32':
    #         self.is_popup_visible = True
    #         super().showPopup()

    #     print(purple(f"{int(time.time())}  OPEN"))
    #     popup = self.view().window()
    #     if not popup:
    #         return

    #     # Make the popup a frameless popup and allow transparent background on the window.
    #     # On Windows this generally works; on some Linux setups true transparency may be
    #     # limited — but we don't require transparency, because the view draws the background.
    #     flags = popup.windowFlags()
    #     popup.setWindowFlags(flags | Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
    #     popup.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
    #     popup.setStyleSheet("QFrame { background: transparent; border: none; }")
    #     popup.resize(self.width(), popup.height() + 2 * COMBOBOX_RADIUS)
    #     self.view().setGeometry(0, 0, popup.width(), popup.height())
    #     self.view().viewport().update()

    #     if sys.platform == 'linux':
    #         super().showPopup()
    #         self.is_popup_visible = True


    # def hidePopup(self):
    #     if self.lineEdit() and not self.lineEdit().isReadOnly():
    #         print(f"{self.objectName()} editable: forward to super")
    #         super().hidePopup()
    #         return

    #     if not self.can_hide:
    #         print(f"  ignore hide, allow for next time")
    #         self.can_hide = True
    #         return
    #     else:
    #         print(f"  can hide")

    #     print(purple(f"{int(time.time())}  HIDE"))
    #     self.counter = 0
    #     super().hidePopup()
    #     self.is_popup_visible = False

