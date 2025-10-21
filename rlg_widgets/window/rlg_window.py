import os
from pathlib import Path
from pprint import pprint
import sys
from typing import Optional
from PySide6.QtCore import (
    Qt,
    QSize,
)
from PySide6.QtGui import (
    QPixmap,
    QMouseEvent,
    QFont,
    QColor,
)
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QFrame,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)
from ..title_bar.title_bar import (
    OsStyle,
    TitleBar,
)
from ..title_bar.style import (
    TitleBarColors,
    TOOLBAR_HEIGHT,
)
from ..utils import (
    GRIP_BORDER_SIZE,
)
if sys.platform == "win32":
    from ..win32.frameless_widget import FramelessWidget
elif sys.platform == "linux":
    from ..linux.frameless_widget import FramelessWidget
elif sys.platform == "darwin":
    from ..darwin.frameless_widget import FramelessWidget
else:
    raise NotImplementedError(f"{sys.platform} is not supported")


_MAIN_FRAME_STYLESHEET = """
    #{name} {{
        background-color: {bgd};
        border-bottom-left-radius: {radius}px;
        border-bottom-right-radius: {radius}px;
        border-left: {border}px solid;
        border-right: {border}px solid;
        border-bottom: {border}px solid;
        border-color: {border_color};
    }}
"""

class RlgWindow(FramelessWidget):
    def __init__(self,
        parent: Optional[QWidget],
        resizable: bool = True,
        border_radius: int = 8,
        os_style: OsStyle = 'windows'
    ) -> None:
        super().__init__(parent)
        self.__is_initialized: bool = False

        self.resizable = resizable
        self.bgd_color = "#606060"
        self.border_color = self.bgd_color
        self.border_width = 0
        self.border_radius = border_radius
        self.main_frame_style: dict[str, str] = {
            'windowed': "",
            'maximized': "",
        }

        self._central_widget = self
        if FramelessWidget.__base__ == QMainWindow:
            self._central_widget: QWidget = QWidget(self)
        self._central_widget.setObjectName("central_widget")

        self.higher_layout = QVBoxLayout(self._central_widget)
        self.higher_layout.setObjectName("higher_layout")
        self.higher_layout.setSpacing(0)
        self.higher_layout.setContentsMargins(0, 0, 0, 0)

        # Title bar
        self.titlebar_frame = QFrame(self._central_widget)
        self.titlebar_frame.setFixedHeight(TOOLBAR_HEIGHT)
        self.titlebar_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.titlebar_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.titlebar_frame.setLineWidth(0)
        self.titlebar_layout = QVBoxLayout(self.titlebar_frame)
        self.titlebar_layout.setObjectName("titlebar_layout")
        self.titlebar_layout.setSpacing(0)
        self.titlebar_layout.setContentsMargins(0, 0, 0, 0)

        # Main frame
        self._main_frame = QFrame(self._central_widget)
        self._main_frame.setFrameShape(QFrame.Shape.NoFrame)
        self._main_frame.setFrameShadow(QFrame.Shadow.Plain)
        self._main_frame.setLineWidth(0)
        self._main_frame.setObjectName("main_frame")

        # Append frames to the higher layout
        self.higher_layout.addWidget(self.titlebar_frame)
        self.higher_layout.addWidget(self._main_frame)
        self.higher_layout.setObjectName("higher_layout")

        self.titlebar = TitleBar(
            self.titlebar_frame,
            resizable=resizable,
            border_radius=border_radius,
            close_border_size=GRIP_BORDER_SIZE,
            os_style=os_style
        )
        self.titlebar_layout.insertWidget(0, self.titlebar, 0, Qt.AlignmentFlag.AlignTop)
        self.titlebar.signal_minimize.connect(self.minimize_event)
        self.titlebar.signal_maximize_clicked.connect(self.maximize_event)
        # self.titlebar.signal_moving_started.connect(self.update_style)
        self.titlebar.signal_double_clicked.connect(self.double_clicked_event)
        self.titlebar.signal_close.connect(self.close_event)
        self.titlebar.signal_is_moving[bool].connect(self.moving_event)
        self.titlebar.raise_()
        self.titlebar.installEventFilter(self)

        self.titlebar_frame_style: dict[str, str] = {
            'windowed': """
                .QFrame {{
                    border-top-left-radius: {radius}px;
                    border-top-right-radius: {radius}px;
                }}
            """.format(radius=self.border_radius),
            'maximized': """
                .QFrame {{
                    border: 0px;
                }}
            """
        }
        self.main_frame_style: dict[str, str] = {}
        self.setBackgroundColor(self.bgd_color)

        self.titlebar_frame.setStyleSheet(self.titlebar_frame_style['windowed'])
        self._main_frame.setStyleSheet(self.main_frame_style['windowed'])
        self._main_layout = QVBoxLayout(self._main_frame)
        self._main_layout.setContentsMargins(0,0,0,0)
        policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._main_frame.setSizePolicy(policy)
        self._main_frame.setLayout(self._main_layout)


        self._main_widget: QWidget | None = None
        self._main_widget_stylesheet: str | None = None


        # if SHADOW_RADIUS > 0:
        #     self.higher_layout.setContentsMargins(SHADOW_RADIUS, SHADOW_RADIUS, SHADOW_RADIUS, SHADOW_RADIUS)
        #     self.shadow = QGraphicsDropShadowEffect(self)
        #     self.shadow.setColor(QColor(0, 0, 0, SHADOW_ALPHA))
        #     self.shadow.setBlurRadius(SHADOW_RADIUS)
        #     self.shadow.setOffset(2, 2)
        #     self.setGraphicsEffect(self.shadow)

        if FramelessWidget.__base__ == QMainWindow:
            super().setCentralWidget(self._central_widget)

        self.initialize()
        # self.update_style(force=True)
        self._update_stylesheet()
        self.installEventFilter(self)

        # availableGeometry = QApplication.primaryScreen().availableGeometry()
        # print(availableGeometry)
        # screen_resolution = QApplication.primaryScreen().geometry()
        # print(screen_resolution)
        # 100%
        # PySide6.QtCore.QRect(0, 0, 2560, 1392)
        # PySide6.QtCore.QRect(0, 0, 2560, 1440)
        # 125%
        # PySide6.QtCore.QRect(0, 0, 2048, 1104)
        # PySide6.QtCore.QRect(0, 0, 2048, 1152)
        self.__is_initialized = True


    def set_title(self, title: str = '') -> None:
        self.titlebar.set_title(title)


    def set_title_font(
        self,
        font: QFont,
        font_size: int = 11,
        bold: bool = False,
        italic: bool = False
    ) -> None:
        self.titlebar.app_title.set_font_style(font, font_size, bold, italic)


    def set_titlebar_colors(self, colors: TitleBarColors):
        self.titlebar.set_color_style(colors)


    def setWindowTitle(self, title: str = '') -> None:
        return self.set_title(title)


    def set_icon(self, icon: str | Path | QPixmap) -> None:
        self.titlebar.set_icon(icon)


    def setWindowIcon(self, icon: str | Path) -> None:
        TASKBAR_ICON_SIZE = 16
        if isinstance(icon, str | Path):
            if not os.path.exists(icon):
                raise ValueError(f"{icon} not found")
            pixmap = QPixmap(icon)
            icon_size = QSize(TASKBAR_ICON_SIZE, TASKBAR_ICON_SIZE)
            if pixmap.size() != icon_size:
                pixmap = pixmap.scaled(icon_size, aspectMode=Qt.AspectRatioMode.IgnoreAspectRatio)
            super().setWindowIcon(pixmap)
        self.set_icon(icon)


    def setCentralWidget(self, widget: QWidget) -> None:
        self._main_widget = widget
        self._main_layout.addWidget(widget)
        if self._main_widget_stylesheet is not None:
            print("set centralwidget stylesheet")
            self._main_widget.setStyleSheet(self._main_widget_stylesheet)


    def setStyleSheet(self, styleSheet: str) -> None:
        if self._main_widget is None:
            self._main_widget_stylesheet = styleSheet
        else:
            self._main_widget.setStyleSheet(styleSheet)


    def close_event(self):
        for w in QApplication.topLevelWidgets():
            w.close()
        self.close()


    def minimize_event(self):
        self.showMinimized()


    def maximize_event(self):
        if self.windowState() in (Qt.WindowState.WindowMaximized,
                                Qt.WindowState.WindowFullScreen):
            self.showNormal()
        else:
            self.showMaximized()
        self.update_style()
        self.moving = False


    def double_clicked_event(self):
        self.maximize_event()


    # def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    #     print("mouse released")
    #     new_state = self.windowState()
    #     if self.previous_window_state != new_state:
    #         self.update_style(new_state)
    #         self.previous_window_state = new_state

    #     if self.titlebar.is_cursor_over_buttons():
    #         self.titlebar.setCursor(Qt.CursorShape.ArrowCursor)
    #         self.setCursor(Qt.CursorShape.ArrowCursor)

    #     if self.moving or self.resizing:
    #         self.moving = False
    #         self.resizing = False
    #         # return True

    #     return super().mouseReleaseEvent(event)


    def update_style(
        self,
        window_state: Qt.WindowState | None = None,
        force: bool = False
    ) -> None:
        window_state = self.windowState() if window_state is None else window_state
        if self.previous_window_state != window_state or force:
            self.previous_window_state = window_state
            if window_state in (Qt.WindowState.WindowMaximized,
                                Qt.WindowState.WindowFullScreen):
                self.titlebar.set_window_state(window_state)
                self._main_frame.setStyleSheet(self.main_frame_style['maximized'])

            elif window_state == Qt.WindowState.WindowNoState:
                self.higher_layout.setContentsMargins(0, 0, 0, 0)
                self.titlebar.set_window_state(window_state)
                self._main_frame.setStyleSheet(self.main_frame_style['windowed'])


    def _update_stylesheet(self) -> None:
        self.main_frame_style: dict[str, str] = {
            'windowed': _MAIN_FRAME_STYLESHEET.format(
                name=self._main_frame.objectName(),
                bgd=self.bgd_color,
                border=self.border_width,
                border_color=self.border_color,
                radius=self.border_radius
            ),
            'maximized': _MAIN_FRAME_STYLESHEET.format(
                name=self._main_frame.objectName(),
                bgd=self.bgd_color,
                border=0,
                border_color=self.bgd_color,
                radius=0
            ),
        }


    def setBackgroundColor(self, color: str | tuple) -> None:
        if isinstance(color, tuple):
            self.bgd_color = QColor(*color).name()
        else:
            self.bgd_color = color
        self._update_stylesheet()
        if self.__is_initialized:
            self.update_style(force=True)


    def _set_border_style(self, color: str, width: int = 1, radius: int=12) -> None:
        self.border_color = color
        self.border_width = width
        self.border_radius = radius
        self._update_stylesheet()
        if self.__is_initialized:
            self.update_style(force=True)


    def remove_border(self) -> None:
        self.border_color = self.bgd_color
        self.border = 0
        self.titlebar.remove_border()
        self._update_stylesheet()
        if self.__is_initialized:
            self.update_style(force=True)


    def _setTitlebarSeparation(self, color: str) -> None:
        widget: QWidget = self.higher_layout.itemAt(1).widget()
        if widget.objectName() != "main_separation_bar":
            line = QFrame(self._central_widget)
            line.setObjectName("main_separation_bar")
            line.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
            line.setFixedHeight(1)
            line.setFrameShadow(QFrame.Shadow.Plain)
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.higher_layout.insertWidget(1, line)
            widget = line

        widget.setStyleSheet(
            """
                #main_separation_bar {{
                    color:{bgd};
                }}
            """.format(bgd=color)
        )


    def setWindowStyle(self, style: dict) -> None:
        self.titlebar.set_style(style)

        titlebar: TitleBarColors = style['titlebar']
        if titlebar.separation is not None:
            self._setTitlebarSeparation(titlebar.separation)

        self._set_border_style(
            color=style['window']['border_color'],
            width=style['window']['border_width'],
            radius=style['window']['border_radius'],
        )

        self.bgd_color = style['window']['background']
        self._update_stylesheet()
        self.update_style(force=True)
