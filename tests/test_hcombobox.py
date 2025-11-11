import os
import sys
from hytils import parent_directory
sys.path.append(os.path.join(parent_directory(__file__), "hwidgets"))


from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QWidget,
    QGridLayout,
)
from hytils import (
    blue, lightcyan, lightgreen, lightgrey, orange,
    purple, yellow,
)

from hwidgets.combobox import HComboBox
from hwidgets.hstyle import *
from hwidgets.logger import hlogger


if __name__ == "__main__":
    import signal
    from argparse import ArgumentParser

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    parser = ArgumentParser()
    parser.add_argument("--debug", "-debug", action="store_true", required=False)
    arguments = parser.parse_args()
    if arguments.debug:
        import logging
        logger: logging.Logger = logging.getLogger("hwidgets")
        hlogger.addHandler(logging.StreamHandler(sys.stdout))
        logging.disable(logging.NOTSET)
        hlogger.setLevel("DEBUG")


    app = QApplication(sys.argv)

    items = [
        "This is a long text you can select if you want",
        "Another item to test a very very very long text to display",
        "Copy me with Ctrl+C you should see some dots in the line",
        "Right-click won't work"
    ]

    hrl_style = HStyle()

    window = QWidget()
    window.setStyleSheet(f"""
        background-color: {hrl_style.window_bgd};
        color: {hrl_style.text_color};
    """)
    p = window.palette()
    p.setColor(window.backgroundRole(), hrl_style.window_bgd)
    window.setPalette(p)

    main_layout = QGridLayout(window)
    main_layout.setContentsMargins(50,50,50,300)
    main_layout.setSpacing(64)

    qcombobox = QComboBox(window)
    qcombobox.addItems(items)

    hcombobox = HComboBox(window, hstyle=hrl_style)
    hcombobox.addItems(items)

    main_layout.addWidget(qcombobox, 0, 0, 1, 1)
    main_layout.addWidget(hcombobox, 0, 1, 1, 1)

    window.show()
    sys.exit(app.exec())
