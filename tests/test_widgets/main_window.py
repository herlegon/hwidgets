from hutils import (
    absolute_path,
    get_extension,
)
from hwidgets.hstyle import HStyle

from designer.ui_main_window import Ui_MainWindow
from PySide6.QtCore import (
    Qt,
    QThread,
    QTimer,
    Signal,
    QPoint,
    QSize,
)
from PySide6.QtGui import (
    QAction,
    QCloseEvent,
    QCursor,
    QDragEnterEvent,
    QDropEvent,
    QKeySequence,
    QShortcut,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QWidget
)


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        hrl_style = HStyle()


        self.setupUi(self, hstyle=hrl_style)

        items = [
            "This is a long text you can select if you want",
            "Another item to test a very very very long text to display",
            "Copy me with Ctrl+C you should see some dots in the line",
            "Right-click won't work"
        ]



        self.h_frame.setStyleSheet(f"""
            background-color: {hrl_style.window_bgd};
            color: {hrl_style.text_color};
        """)
        # p = self.palette()
        # p.setColor(self.backgroundRole(), hrl_style.window_bgd)
        # self.setPalette(p)

        for w in (
            self.q_combobox_rw,
            self.q_combobox_read_only,
            self.q_combobox_disabled,
            self.h_combobox_rw,
            self.h_combobox_read_only,
            self.h_combobox_disabled,
        ):
            w.addItems(items)

        self.setMinimumWidth(800)
        self.move(QPoint(400,200))



