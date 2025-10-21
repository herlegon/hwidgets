from enum import IntEnum

import ctypes
from ctypes import (
    byref,
    sizeof,
    windll,
    c_int,
    POINTER,
    HRESULT,
    pointer,
)
from ctypes.wintypes import (
    DWORD,
    HWND,
    POINT,
    RECT,
    UINT,
    ULONG,
    LPARAM,
    LPRECT,
    HBRUSH,
    COLORREF,
)
from enum import Enum
from PySide6.QtCore import (
    QRect,
    QMargins,
)

# Use the DPI-aware version of the API
user32 = ctypes.windll.user32
# user32.SetProcessDPIAware()
gdi32 = ctypes.windll.gdi32
dwmapi = ctypes.windll.dwmapi

class AccentPolicy(ctypes.Structure):
    _fields_ = [
        ("AccentState", DWORD),
        ("AccentFlags", DWORD),
        ("GradientColor", DWORD),
        ("AnimationId", DWORD),
    ]


class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [
        ("Attribute", DWORD),
        ("Data", POINTER(AccentPolicy)),
        ("SizeOfData", ULONG),
    ]


class MARGINS(ctypes.Structure):
    _fields_ = [
        ("cxLeftWidth", c_int),
        ("cxRightWidth", c_int),
        ("cyTopHeight", c_int),
        ("cyBottomHeight", c_int),
    ]
tagMARGINS = MARGINS
LPMARGINS = PMARGINS = POINTER(MARGINS)


class MINMAXINFO(ctypes.Structure):
    _fields_ = [
        ("ptReserved", POINT),
        ("ptMaxSize", POINT),
        ("ptMaxPosition", POINT),
        ("ptMinTrackSize", POINT),
        ("ptMaxTrackSize", POINT),
    ]


class PWINDOWSPOS(ctypes.Structure):
    _fields_ = [
        ('hWnd', HWND),
        ('hwndInsertAfter', HWND),
        ('x', c_int),
        ('y', c_int),
        ('cx', c_int),
        ('cy', c_int),
        ('flags', UINT)
    ]


class NCCALCSIZE_PARAMS(ctypes.Structure):
    _fields_ = [
        ('rgrc', RECT * 3),
        ('lppos', POINTER(PWINDOWSPOS))
    ]
LPNCCALCSIZE_PARAMS = POINTER(NCCALCSIZE_PARAMS)


class APPBARDATA(ctypes.Structure):
    _fields_ = [
        ('cbSize', DWORD),
        ('hWnd', HWND),
        ('uCallbackMessage', UINT),
        ('uEdge', UINT),
        ('rc', RECT),
        ('lParam', LPARAM),
    ]
tagMINMAXINFO = APPBARDATA
LPAPPBARDATA = PAPPBARDATA = POINTER(APPBARDATA)



class MINMAXINFO(ctypes.Structure):
    _fields_ = [
        ("ptReserved", POINT),
        ("ptMaxSize", POINT),
        ("ptMaxPosition", POINT),
        ("ptMinTrackSize", POINT),
        ("ptMaxTrackSize", POINT)
    ]
tagMINMAXINFO = MINMAXINFO
LPMINMAXINFO = PMINMAXINFO = POINTER(MINMAXINFO)


class WINDOWPLACEMENT(ctypes.Structure):
    _fields_ = [
        ('length', UINT),
        ('flags', UINT),
        ('showCmd', UINT),
        ('ptMinPosition', POINT),
        ('ptMaxPosition', POINT),
        ('rcNormalPosition', RECT),
    ]
tagMINMAXINFO = WINDOWPLACEMENT
LPWINDOWPLACEMENT = PWINDOWPLACEMENT = POINTER(WINDOWPLACEMENT)


class MONITORINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("rcMonitor", RECT),
        ("rcWork", RECT),
        ("dwFlags", DWORD),
    ]
tagMONITORINFO = MONITORINFO
LPMONITORINFO = PMONITORINFO = POINTER(MONITORINFO)


class CursorHotSpot(Enum):
    HtClient = 1
    HtMaxButton = 9
    HtLeft = 10
    HtRight = 11
    HtTop = 12
    HtTopLeft = 13
    HtTopRight = 14
    HtBottom = 15
    HtBottomLeft = 16
    HtBottomRight = 17

HTCAPTION = 2

WVR_REDRAW = 0x0300


WM_GETMINMAXINFO = 36
WM_WINDOWPOSCHANGING = 70
WM_WINDOWPOSCHANGED = 71
WM_MOVE = 0x0003
WM_NCHITTEST = 132
WM_CAPTURECHANGED = 533
WM_MOVING = 534
WM_NCCALCSIZE = 131
WM_NCLBUTTONDOWN = 0x00A1
WM_NCLBUTTONUP = 0x00A2
WM_NCLBUTTONDBLCLK = 0x00A3
WM_LBUTTONDBLCLK = 0x0203
WM_WINDOWPOSCHANGING = 70
WM_GETMINMAXINFO = 36
WM_NCPAINT = 133
WM_ERASEBKGND = 20
WM_WINDOWPOSCHANGED = 71
WM_SIZE = 0x0005
WM_SETCURSOR = 0x0020
WM_GETOBJECT = 0x003d
WM_SYSKEYDOWN = 0x0104
WM_NCMOUSEMOVE = 0x00a0
WM_NCMOUSELEAVE = 0x02a2


# For Debug:
WmToName = {
    20: "WM_ERASEBKGND",
    36: "WM_GETMINMAXINFO",
    70: "WM_WINDOWPOSCHANGING",
    71: "WM_WINDOWPOSCHANGED",
    0x0003: "WM_MOVE",
    0x0005: "WM_SIZE",
    132: "WM_NCHITTEST",
    533: "WM_CAPTURECHANGED",
    534: "WM_MOVING",
    131: "WM_NCCALCSIZE",
    515: "WM_LBUTTONDBLCLK",
    0x0104: "WM_SYSKEYDOWN",
    0x003d: "WM_GETOBJECT",
    0x0020: "WM_SETCURSOR",
    0x00a0: "WM_NCMOUSEMOVE",
    0x02a2: "WM_NCMOUSELEAVE",

}


ABS_AUTOHIDE = 1
ABM_GETSTATE = 4
ABM_GETTASKBARPOS = 5 # Fixed on Window 11
def is_taskbar_autohide() -> bool:
    app_bar_data = APPBARDATA()
    app_bar_data.lParam = 1
    app_bar_data.length = sizeof(app_bar_data)
    taskbarState = windll.shell32.SHAppBarMessage(ABM_GETSTATE, byref(app_bar_data))
    return bool(taskbarState == ABS_AUTOHIDE)



ABM_GETAUTOHIDEBAREX  = 0x0000000B
TASKBAR_THICKNESS: int = 2
class TaskbarPosition(IntEnum):
    ABM_LEFT = 0
    ABM_TOP = 1
    ABM_RIGHT = 2
    ABE_BOTTOM = 3
    UNKNOWN = -1


def get_taskbar_position(window_handle: int) -> TaskbarPosition | None:
    MONITOR_DEFAULTTONEAREST = 2
    monitor_handle = user32.MonitorFromWindow(window_handle, MONITOR_DEFAULTTONEAREST)
    if monitor_handle == 0:
        return TaskbarPosition.UNKNOWN

    get_monitor_info = user32.GetMonitorInfoA
    get_monitor_info.argtypes = [HWND, LPMONITORINFO]
    monitor_info = MONITORINFO()
    monitor_info.cbSize = sizeof(MONITORINFO)
    if not get_monitor_info(monitor_handle, byref(monitor_info)):
        return TaskbarPosition.UNKNOWN

    appbarData = APPBARDATA(sizeof(APPBARDATA), 0, 0, 0, monitor_info.rcMonitor, 0)
    for position in (TaskbarPosition.ABM_LEFT,
                        TaskbarPosition.ABM_TOP,
                        TaskbarPosition.ABM_RIGHT,
                        TaskbarPosition.ABE_BOTTOM):
        appbarData.uEdge = position
        if windll.shell32.SHAppBarMessage(ABM_GETAUTOHIDEBAREX , byref(appbarData)):
            print(f"is {position}")
            return position
    TaskbarPosition.UNKNOWN



SW_NORMAL = 1
SW_SHOWMINIMIZED = 2
SW_SHOWMAXIMIZED = 3
def _get_window_placement(window_handle: int) -> int:
    get_window_placement = windll.user32.GetWindowPlacement
    get_window_placement.argtypes = [HWND, PWINDOWPLACEMENT]
    get_window_placement.restype = bool
    window_placement = WINDOWPLACEMENT()
    window_placement.length = sizeof(window_placement)
    get_window_placement(window_handle, byref(window_placement))
    return window_placement.showCmd


def is_window_maximized(window_handle: int) -> bool:
    return bool(_get_window_placement(window_handle) == SW_SHOWMAXIMIZED)


def is_window_minimized(window_handle: int) -> bool:
    return bool(_get_window_placement(window_handle) == SW_SHOWMINIMIZED)


def is_window_normal(window_handle: int) -> bool:
    return bool(_get_window_placement(window_handle) == SW_NORMAL)



def is_window_fullscreen(window_handle: int, margins: QMargins) -> bool:
    MONITOR_DEFAULTTOPRIMARY = 1
    MONITOR_DEFAULTTONEAREST = 2
    if not window_handle:
        return False

    get_window_rect_fct = user32.GetWindowRect
    get_window_rect_fct.argtypes = [HWND, LPRECT]
    get_window_rect_fct.restype = bool

    rect = RECT()
    result = get_window_rect_fct(window_handle, byref(rect))
    if not result:
        False
    window_rect: QRect = QRect(rect.left, rect.top, rect.right, rect.bottom)
    window_rect -= QMargins(margins.left(), margins.top(), 0, 0)

    monitor_handle = user32.MonitorFromWindow(window_handle, MONITOR_DEFAULTTONEAREST)
    if monitor_handle == 0:
        return False

    get_monitor_info = user32.GetMonitorInfoA
    get_monitor_info.argtypes = [HWND, LPMONITORINFO]
    monitor_info = MONITORINFO()
    monitor_info.cbSize = sizeof(MONITORINFO)
    if not get_monitor_info(monitor_handle, byref(monitor_info)):
        return False
    rect = monitor_info.rcMonitor
    monitor_rect: QRect = QRect(rect.left, rect.top, rect.right, rect.bottom)

    return bool(window_rect == monitor_rect)



def get_border_size(window_handle: int):
    SM_CXSIZEFRAME = 32
    SM_CYSIZEFRAME = 33
    SM_CXPADDEDBORDER = 92
    x_dpi, y_dpi, _, _ = get_dpi_for_window(window_handle)
    # print(f"x_dpi, y_dpi = ({x_dpi}, {y_dpi})")
    h_border = (
        user32.GetSystemMetricsForDpi(SM_CXSIZEFRAME, x_dpi)
        + user32.GetSystemMetricsForDpi(SM_CXPADDEDBORDER, x_dpi)
    )
    # print(user32.GetSystemMetricsForDpi(SM_CXSIZEFRAME, x_dpi))
    # print(user32.GetSystemMetricsForDpi(SM_CXPADDEDBORDER, x_dpi))
    v_border = (
        user32.GetSystemMetricsForDpi(SM_CYSIZEFRAME, y_dpi)
        + user32.GetSystemMetricsForDpi(SM_CXPADDEDBORDER, y_dpi)
    )
    return h_border, v_border



def get_dpi_for_window(window_handle):
    # https://github.com/github/VisualStudio/blob/master/tools/Debugging%20Tools%20for%20Windows/winext/manifest/gdi32.h
    # https://referencesource.microsoft.com/#System.Windows.Forms/misc/GDI/DeviceCapabilities.cs,956b6ef762bba1c1
    # HORZRES = 8 # Horizontal width in pixels
    # VERTRES = 10 # Vertical height in pixels
    LOGPIXELSX = 88 # Logical pixels/inch in X
    LOGPIXELSY = 90 # Logical pixels/inch in Y
    # PHYSICALOFFSETX = 112 # Physical Printable Area x margin
    # PHYSICALOFFSETY = 113 # Physical Printable Area y margin
    # VREFRESH = 116  # Current vertical refresh rate of the display device (for displays only) in Hz
    x_dpi, y_dpi = 96, 96
    try:
        dc_handle = user32.GetDC(window_handle)
        x_dpi = max(0, gdi32.GetDeviceCaps(dc_handle, LOGPIXELSX))
        y_dpi = max(0, gdi32.GetDeviceCaps(dc_handle, LOGPIXELSY))
        user32.ReleaseDC(dc_handle)
    except Exception as _:
        pass
    return x_dpi, y_dpi, x_dpi/96, y_dpi/96



def set_window_style(window_handle: int, shadow: bool = False) -> None:
    # https://learn.microsoft.com/en-us/windows/win32/winmsg/window-styles
    WS_MINIMIZEBOX = 0x00020000
    WS_MAXIMIZEBOX = 0x00010000
    WS_CAPTION = 0x00C00000
    CS_DBLCLKS = 8
    WS_THICKFRAME = 0x00040000
    GWL_STYLE = -16

    style = user32.GetWindowLongA(window_handle, GWL_STYLE)
    set_window_long_fct = user32.SetWindowLongA
    set_window_long_fct.argtypes = [HWND, ctypes.c_int, DWORD]
    set_window_long_fct.restype = DWORD
    set_window_long_fct (
        window_handle,
        GWL_STYLE,
        style | WS_MINIMIZEBOX | WS_MAXIMIZEBOX | WS_CAPTION | CS_DBLCLKS | WS_THICKFRAME
    )

    if shadow:
        bResult = c_int(0)
        dwmapi.DwmIsCompositionEnabled(byref(bResult))
        if bResult.value != 1:
            return
        dwm_extend_frame_into_client_area_fct = dwmapi.DwmExtendFrameIntoClientArea
        dwm_extend_frame_into_client_area_fct.argtypes = [HWND, LPMARGINS]
        dwm_extend_frame_into_client_area_fct.restype = HRESULT
        margins = MARGINS(-1, -1, -1, -1)
        dwm_extend_frame_into_client_area_fct(window_handle, pointer(margins))



def set_window_to_move_state(window_handle: int):
    WM_SYSCOMMAND = 274
    SC_MOVE = 0xF010
    HTCAPTION = 2
    user32.ReleaseCapture()
    user32.SendMessageA(window_handle, WM_SYSCOMMAND, SC_MOVE | HTCAPTION)



def paint_background(window_handle: int, rect=None) -> None:
    # paint background in Blue
    get_client_rect_fct = user32.GetClientRect
    get_client_rect_fct.argtypes = [HWND, LPRECT]
    get_client_rect_fct.restype  = bool

    if rect is None:
        lp_rect = RECT()
        get_client_rect_fct(window_handle, byref(lp_rect))
        # return Rect(lpRect.left, lpRect.top, lpRect.right, lpRect.bottom)
    else:
        lp_rect = rect
    # print(lp_rect.top, lp_rect.left, lp_rect.bottom, lp_rect.right)
    dc_handle = user32.GetDC(window_handle)
    # Colour backgroundColour = juceWindow->getBackgroundColour();
    # HBRUSH CreateSolidBrush([in] COLORREF color)
    create_solid_brush_fct = gdi32.CreateSolidBrush
    create_solid_brush_fct.argtypes = [COLORREF]
    create_solid_brush_fct.restype = HBRUSH
    bgd_brush = create_solid_brush_fct(0x00FF0000)
    # print(type(bgd_brush))
    # print(bgd_brush)
    BLACK_BRUSH = 4
    hbrush = user32.SetClassLongPtrA(window_handle, -10)
    # int FillRect([in] HDC        hDC, [in] const RECT *lprc, [in] HBRUSH     hbr);
    fill_rect_fct = user32.FillRect
    fill_rect_fct.argtypes = [HWND, LPRECT, HBRUSH]
    fill_rect_fct.restype = UINT
    fill_rect_fct(hbrush, pointer(lp_rect), bgd_brush)


    # FillRect((HDC)hdc, &rect, bgBrush);
    user32.ReleaseDC(dc_handle)

