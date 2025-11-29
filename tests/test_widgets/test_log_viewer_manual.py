
import sys
import logging
import time
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from hwidgets.log_viewer import HLogViewer
from hwidgets.style_manager import Theme

def main():
    app = QApplication(sys.argv)

    # Setup window
    window = QWidget()
    layout = QVBoxLayout(window)

    # Setup theme
    theme = Theme()

    # Setup Log Viewer
    log_viewer = HLogViewer(theme=theme)
    layout.addWidget(log_viewer)

    # Setup Logger
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(log_viewer.gui_handler)

    # Test Buttons
    btn_debug = QPushButton("Log DEBUG")
    btn_debug.clicked.connect(lambda: logger.debug("This is a debug message"))
    layout.addWidget(btn_debug)

    btn_info = QPushButton("Log INFO")
    btn_info.clicked.connect(lambda: logger.info("This is an info message"))
    layout.addWidget(btn_info)

    btn_warning = QPushButton("Log WARNING")
    btn_warning.clicked.connect(lambda: logger.warning("This is a warning message"))
    layout.addWidget(btn_warning)

    btn_error = QPushButton("Log ERROR")
    btn_error.clicked.connect(lambda: logger.error("This is an error message"))
    layout.addWidget(btn_error)

    btn_critical = QPushButton("Log CRITICAL")
    btn_critical.clicked.connect(lambda: logger.critical("This is a critical message"))
    layout.addWidget(btn_critical)

    btn_ansi = QPushButton("Log ANSI Color")
    def log_ansi():
        # ANSI escape codes for colors
        red = "\033[31m"
        green = "\033[32m"
        reset = "\033[00m"
        logger.info(f"This is {red}RED{reset} and this is {green}GREEN{reset} text.")

    btn_ansi.clicked.connect(log_ansi)
    layout.addWidget(btn_ansi)

    window.resize(600, 400)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
