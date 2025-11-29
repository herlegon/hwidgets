import sys
from hwidgets.style_manager import StyleManager
from hytils import (
    absolute_path,
    get_extension,
)

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
from hwidgets.styles import Theme



class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        theme = StyleManager().get_theme()


        self.setupUi(self, theme=theme)

        items = [
            "This is a long text you can select if you want",
            "Another item to test a very very very long text to display",
            "Copy me with Ctrl+C you should see some dots in the line",
            "Right-click won't work"
        ]

        self.setStyleSheet(f"""
            background-color: {theme.window_bgd};

            color: {theme.default.font_color};
            font-family: {theme.default.font.family};
            font-size: {theme.default.font.size};
        """)

        self.h_frame.setStyleSheet(f"""
            background-color: {theme.window_bgd};

            color: {theme.default.font_color};
            font-family: {theme.default.font.family};
            font-size: {theme.default.font.size};
        """)
        # p = self.palette()
        # p.setColor(self.backgroundRole(), hrl_style.window_bgd)
        # self.setPalette(p)

        for w in (
            self.h_combobox_rw,
            self.h_combobox_ro,
            self.h_combobox_disabled,
            self.h_combobox_rw_2,
            self.h_combobox_ro_2,
            self.h_combobox_disabled_2,
        ):
            w.addItems(items)

        # self.h_radial_progress_1.set_standard_triggers()
        # self.h_radial_progress_2.set_standard_triggers()
        # self.h_radial_progress_3.set_standard_triggers()
        # self.h_radial_progress_4.set_standard_triggers()

        # self.h_radial_progress_1.set_legend_text("GPU")
        # self.h_radial_progress_1.set_label_text("label")
        # from PySide6.QtCore import QSize
        # self.h_radial_progress_1.setFixedSize(QSize(100,100))
        # self.h_radial_progress_1.set_thickness(8)

        button_list = ["btn1", "btn2", "btn3", "btn4"]
        # self.h_button_group.set_buttons(button_list)
        # self.h_button_group.get_button(2).setEnabled(False)
        # self.h_button_group_disabled.set_buttons(button_list)

        # self.h_grey_button_group.set_buttons(button_list)
        # self.h_grey_button_group.get_button(2).setEnabled(False)
        # self.h_grey_button_group_disabled.set_buttons(button_list)

        self.setMinimumWidth(800)
        if sys.platform == 'linux':
            self.move(QPoint(400,50))
        else:
            self.move(QPoint(400,200))



        # make it italic
        self.h_comment_italic.setItalic(True)
        self.h_comment_bold.setWeight(800)
        self.h_comment_small_italic.setItalic(True)
        self.h_comment_small_italic.setFontSize(8)

        self.h_plaintextedit_editable.setClearButtonEnabled(False)

        self.h_indet_progress_bar.hide()
        self.h_indet_progress_bar_m2.start()
        self.h_indet_progress_bar_r.hide()

        for rp in (
            self.h_radial_progress_1,
            self.h_radial_progress_2,
            self.h_radial_progress_3,
            self.h_radial_progress_4,
        ):
            rp.setThickness(4)


        for rp in (
            self.h_radial_progress_vram,
            self.h_radial_progress_vram_2,
            self.h_radial_progress_vram_3,
            self.h_radial_progress_vram_4,
        ):
            rp.setFixedWidth(64)
            rp.setThickness(6)
            rp.useColoredTriggers()
            rp.setLegendText("RTX 4080\nVRAM")
            rp.setLabelText("label")
            rp.displayValue(True)

        self.h_radial_progress_ram.setFixedWidth(rp.bar_width)
        self.h_radial_progress_ram.setThickness(6)
        self.h_radial_progress_ram.useColoredTriggers()
        self.h_radial_progress_ram.setLegendText("RAM")
        self.h_radial_progress_ram.displayValue(True)

        self.h_divider_2.setMinimumHeight(rp.height())

        self.h_log_viewer.setPlainText("Description: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
        self.h_log_viewer.appendPlainText("[WebSocket] Connecting to ws://localhost:8765...")
        self.h_log_viewer.appendPlainText("[WebSocket] Connection established")
        self.h_log_viewer.appendPlainText("[System] Starting package installation...")
        self.h_log_viewer.appendPlainText("")
        self.h_log_viewer.appendPlainText("[pip] Installing torch...")
        self.h_log_viewer.appendPlainText("[pip] ✓ Successfully installed torch")
        self.h_log_viewer.appendPlainText("[pip] Installing transformers...")
        self.h_log_viewer.appendPlainText("[pip] ✓ Successfully installed transformers")
        self.h_log_viewer.appendPlainText("[pip] Installing scipy...")
        self.h_log_viewer.appendPlainText("[pip] ✓ Successfully installed scipy")
        self.h_log_viewer.appendPlainText("[pip] Installing matplotlib...")
        self.h_log_viewer.appendPlainText("[pip] ✓ Successfully installed matplotlib")
        self.h_log_viewer.appendPlainText("[pip] Installing scikit-learn...")
        self.h_log_viewer.appendPlainText("[pip] ✓ Successfully installed scikit-learn")

        # Timer to append text
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._append_timer_log)
        self.timer.start(1000)

    def _append_timer_log(self):
        import random
        messages = [
            "[System] Checking for updates...",
            "[Network] Ping 24ms",
            "[App] Memory usage: 45MB",
            "[User] Activity detected",
            "[Log] Background process running"
        ]
        self.h_log_viewer.appendPlainText(random.choice(messages))
