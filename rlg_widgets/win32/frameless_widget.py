from __future__ import annotations

from ctypes import (
    cast, WinDLL
)
from ctypes.wintypes import (
    LPRECT,
    MSG,
)
import time

from ..window.rlg_window_base import RlgWindowBase
from ..utils import GRIP_BORDER_SIZE
from ..title_bar.close_button import CONTROL_BUTTON_WIDTH

from .utils import (
    HTCAPTION,
    LPNCCALCSIZE_PARAMS,
    TASKBAR_THICKNESS,
    WM_NCCALCSIZE,
    WM_NCHITTEST,
    WM_NCLBUTTONDBLCLK,
    WM_NCLBUTTONDOWN,
    WM_NCLBUTTONUP,
    WM_NCMOUSELEAVE,
    WVR_REDRAW,
    CursorHotSpot,
    TaskbarPosition,
    WmToName,
    get_border_size,
    get_dpi_for_window,
    get_taskbar_position,
    is_window_maximized,
    is_taskbar_autohide,
    is_window_normal,
    set_window_style,
    set_window_to_move_state,
)

from PySide6.QtCore import (
    QEvent,
    QPoint,
    Qt,
    QRect,
    QMargins,
    QByteArray,
    QObject,
)
from PySide6.QtGui import (
    QMouseEvent,
    QCursor,
)
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
)

user32 = WinDLL('user32')


EDGE_TO_CURSOR_HOTSPOT = {
    Qt.Edge.TopEdge | Qt.Edge.LeftEdge: CursorHotSpot.HtTopLeft,
    Qt.Edge.TopEdge: CursorHotSpot.HtTop,
    Qt.Edge.TopEdge | Qt.Edge.RightEdge: CursorHotSpot.HtTopRight,
    Qt.Edge.RightEdge: CursorHotSpot.HtRight,
    Qt.Edge.BottomEdge | Qt.Edge.RightEdge: CursorHotSpot.HtBottomRight,
    Qt.Edge.BottomEdge: CursorHotSpot.HtBottom,
    Qt.Edge.BottomEdge | Qt.Edge.LeftEdge: CursorHotSpot.HtBottomLeft,
    Qt.Edge.LeftEdge: CursorHotSpot.HtLeft,
}


class FramelessWidget(QMainWindow, RlgWindowBase):

    def __init__(self,
        parent: QWidget
    ) -> None:
        super().__init__()
        self.__is_initialized: bool = False
        self.snap_started: bool = False

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        # self.setAttribute(Qt.WidgetAttribute.WA_NativeWindow)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        if isinstance(self, QMainWindow):
            # Translucent background=true + no shadow: no white border, no flickering
            # Translucent background=false + shadow = true: white border when resizing + low qual radius
            # Translucent background + shadow not possible
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
            set_window_style(self.winId(), shadow=False)
            self._central_widget: QWidget = QWidget(self)
        else:
            # Shadow cannot be used
            # Flickering when resizing
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
            set_window_style(self.winId(), shadow=False)

        # window_handle = self.winId()
        # self.setAttribute(Qt.WidgetAttribute.WA_PaintOnScreen)
        # print(f"window handle: {window_handle}")


    def initialize(self) -> None:
        if self.titlebar is None:
            raise ValueError("Titlebar must be defined before calling this method")
        # self.setWindowModality(Qt.WindowModality.NonModal)
        # self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(Qt.WidgetAttribute.WA_NativeWindow)
        # self.setAttribute(Qt.WidgetAttribute.WA_PaintOnScreen)
        # paint_background(self.winId())
        self.__is_initialized = True


    def moving_event(self, enabled: bool) -> None:
        if enabled:
            set_window_to_move_state(self.winId())
        else:
            self.activateWindow()
        self.moving = enabled


    def update_style(self, window_state: Qt.WindowState | None = None) -> None:
        raise NotImplementedError("This method shall be defined in child")


    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        event_type = event.type()

        if not self.moving and watched in (self, self.titlebar):
            if event_type == QEvent.Type.WindowActivate:
                self.moving = False
                self.titlebar.set_active(True)
                return True
            elif event_type == QEvent.Type.WindowDeactivate:
                self.moving = False
                self.titlebar.set_active(False)
                return True



        # print(f"{watched}, {event}")


        return super().eventFilter(watched, event)


    def nativeEvent(self, eventType: QByteArray | bytes, message: int) -> object:
        # Native events only get sent to widgets with a native window handle
        # Native events don't propagate.

        # In your reimplementation of this function, if you want to stop the event
        # being handled by Qt, return true and set result. The result parameter has
        # meaning only on Windows. If you return false, this native event is passed
        # back to Qt, which translates the event into a Qt event and sends it to
        # the widget.
        msg = MSG.from_address(message.__int__())
        if not msg.hWnd:
            return False, 0

        # print(f"{time.time()}: {WmToName.get(msg.message, hex(msg.message))}")


        # is_fullscreen = (
        #     is_window_fullscreen(msg.hWnd, self.higher_layout.contentsMargins())
        #     if self.__is_created
        #     else False
        # )
        # is_maximized = is_window_maximized(msg.hWnd)
        # is_maximized = is_maximized and not is_fullscreen

        # if msg.message == WM_GETMINMAXINFO:
        #     min_max_info = cast(msg.lParam, LPMINMAXINFO).contents
        #     # print("\nmin_max_info:")
        #     print("")
        #     # print(f"mintracksize: ({min_max_info.ptMinTrackSize.x},{min_max_info.ptMinTrackSize.y})")
        #     # print(f"maxtracksize: ({min_max_info.ptMaxTrackSize.x},{min_max_info.ptMaxTrackSize.y})")
        #     (dx, dy) = win_utils.get_border_thickness(msg.hWnd)

        #     # min_max_info.ptMaxPosition.x += 8
        #     # min_max_info.ptMaxPosition.y -= dy
        #     # min_max_info.ptMaxSize.x += dy
        #     min_max_info.ptMaxTrackSize.y -= abs(dy)
        #     print(f"max_size: ({min_max_info.ptMaxSize.x},{min_max_info.ptMaxSize.y})")
        #     print(f"max_pos: ({min_max_info.ptMaxPosition.x},{min_max_info.ptMaxPosition.y})")
        #     # print(f"maxtracksize: ({min_max_info.ptMaxTrackSize.x},{min_max_info.ptMaxTrackSize.y})")

        #     result = 0 if not msg.wParam else WVR_REDRAW
        #     return False, 0
        if msg.message == WM_NCCALCSIZE:
            if not self.__is_initialized:
                return True, 0

            if msg.wParam:
                rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
            else:
                rect = cast(msg.lParam, LPRECT).contents

            # # adjust the size of client rect
            # if self.windowState() == Qt.WindowState.WindowMaximized:
            if is_window_maximized(msg.hWnd):
                self.update_style(Qt.WindowState.WindowMaximized)
                # This is not exact but it works good enough for scale < 175%
                # This is a workaround for the bug in PySide: QTBUG-120196
                (dx, dy) = get_border_size(msg.hWnd)
                _, _, x_factor, y_factor = get_dpi_for_window(msg.hWnd)
                dx = round(dx / x_factor)
                dy = round(dy / y_factor)
                self.higher_layout.setContentsMargins(abs(dx), abs(dy), abs(dx), abs(dy))
                dx -= 1
                dy -= 1

                # Auto-hide taskbar
                if is_taskbar_autohide():
                    taskbar_position: TaskbarPosition = get_taskbar_position(msg.hWnd)
                    if taskbar_position == TaskbarPosition.ABM_LEFT:
                        rect.left += TASKBAR_THICKNESS + dx
                    elif taskbar_position == TaskbarPosition.ABM_TOP:
                        rect.top += TASKBAR_THICKNESS + dy
                    elif taskbar_position == TaskbarPosition.ABM_RIGHT:
                        rect.right -= TASKBAR_THICKNESS + dx
                    elif taskbar_position == TaskbarPosition.ABE_BOTTOM:
                        rect.bottom -= TASKBAR_THICKNESS + dy

                if self.moving:
                    self.moving = False

            elif is_window_normal(msg.hWnd) and self.windowState() != Qt.WindowState.WindowNoState:
                # Change into normal
                self.higher_layout.setContentsMargins(0,0,0,0)
                self.update_style(Qt.WindowState.WindowNoState)


            # self.titlebar.maximize_button.force_over_state(False, True)

            # https://github.com/MicrosoftDocs/win32/blob/docs/desktop-src/winmsg/wm-nccalcsize.md
            # If the wParam parameter is FALSE, the application should return zero.
            # If wParam is TRUE, the application should return zero or a combination of the following values.

            # paint_background(msg.hWnd, rect)
            return True, 0 if msg.wParam == 0 else WVR_REDRAW

        if msg.message == WM_NCMOUSELEAVE and self.snap_started:
            self.titlebar.maximize_button.force_over_state(False)
            self.snap_started = False

        cursor_position: QPoint = QCursor.pos() - self.geometry().topLeft()
        if msg.message == WM_NCHITTEST and self.resizable:
            # Sent to a window in order to determine what part of the window corresponds
            # to a particular screen coordinate. This can happen, for example, when the
            # cursor moves, when a mouse button is pressed or released, or in response to
            # a call to a function such as WindowFromPoint

            if is_window_normal(msg.hWnd):
                ngrip_area: QRect
                ngrip_area = (
                    self.rect()
                    - QMargins(GRIP_BORDER_SIZE, GRIP_BORDER_SIZE, GRIP_BORDER_SIZE, GRIP_BORDER_SIZE)
                )

                # if self.titlebar.buttons_hover():
                #     print(f"{time.time()}: WM_NCHITTEST: in area")
                # print(ngrip_area)
                # print(cursor_position)
                # print()
                if not ngrip_area.contains(cursor_position) and not self.titlebar.is_cursor_over_buttons():
                    x, y = cursor_position.toTuple()
                    near_edges = Qt.Edge(0)
                    if x < ngrip_area.left():
                        near_edges |= Qt.Edge.LeftEdge
                    elif x > ngrip_area.right():
                        near_edges |= Qt.Edge.RightEdge
                    if y < ngrip_area.top():
                        near_edges |= Qt.Edge.TopEdge
                    elif y > ngrip_area.bottom():
                        near_edges |= Qt.Edge.BottomEdge

                    self.resizing = True
                    cursor_hotspot = EDGE_TO_CURSOR_HOTSPOT.get(near_edges, None)
                    if cursor_hotspot is not None:
                        return True, cursor_hotspot.value

            if self.titlebar.is_over_maximize_button(cursor_position):
                self.titlebar.maximize_button.force_over_state(True)
                self.snap_started = True
                return True, CursorHotSpot.HtMaxButton.value
            elif self.snap_started:
                self.titlebar.maximize_button.force_over_state(False)
                self.snap_started = False

            if self.titlebar.is_over(cursor_position):
                return False, HTCAPTION


        elif self.__is_initialized and self.titlebar.is_over_maximize_button(cursor_position):

            if msg.message in [WM_NCLBUTTONDOWN, WM_NCLBUTTONDBLCLK]:
                return True, 0

            if msg.message == WM_NCLBUTTONUP:
                self.titlebar.maximize_button.force_over_state(False)
                if self.windowState() == Qt.WindowState.WindowMaximized:
                    event_push = QMouseEvent(
                        QEvent.Type.MouseButtonPress,
                        QPoint(),
                        Qt.MouseButton.LeftButton,
                        Qt.MouseButton.NoButton,
                        Qt.KeyboardModifier.NoModifier,
                    )
                    event_release = QMouseEvent(
                        QEvent.Type.MouseButtonRelease,
                        QPoint(),
                        Qt.MouseButton.LeftButton,
                        Qt.MouseButton.NoButton,
                        Qt.KeyboardModifier.NoModifier,
                    )
                    QApplication.sendEvent(self.titlebar.maximize_button, event_push)
                    QApplication.sendEvent(self.titlebar.maximize_button, event_release)

                else:
                    new_point = QCursor.pos() + QPoint(-2 * CONTROL_BUTTON_WIDTH, 0)
                    event = QMouseEvent(
                        QEvent.Type.MouseButtonDblClick,
                        new_point,
                        Qt.MouseButton.LeftButton,
                        Qt.MouseButton.NoButton,
                        Qt.KeyboardModifier.NoModifier,
                    )
                    QApplication.sendEvent(self.titlebar, event)
                return True, 0

        # print(f"{time()} {msg.message}")

        # Resizing
        # 1706650290.7352471 15
        # 1706650290.7372496 532    WM_CAPTURE...
        # 1706650290.7372496 70     WM_WINDOWPOSCHANGING
        # 1706650290.7372496 36     WM_GETMINMAXINFO
        # 1706650290.7392552 133    WM_NCPAINT
        # 1706650290.7392552 20     WM_ERASEBKGND
        # 1706650290.7392552 71     WM_WINDOWPOSCHANGED
        # 1706650290.7392552 5      WM_SIZE



        # return super().nativeEvent(eventType, message)
        return False, 0

