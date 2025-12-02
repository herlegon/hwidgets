from argparse import ArgumentParser
from pathlib import Path
from hytils import parent_directory
import os
import signal
import sys
sys.path.append(os.path.join(parent_directory(__file__), "hwidgets"))

from PySide6.QtGui import (
    QFontDatabase,
    QFont,
)
from PySide6.QtWidgets import (
    QApplication,
)
from main_window import MainWindow

if sys.platform == "win32":
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "pynnlib.gui"
    )


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    parser = ArgumentParser()
    parser.add_argument("--debug", "-debug", action="store_true", required=False)
    arguments = parser.parse_args()
    if arguments.debug:
        import logging
        hlogger: logging.Logger = logging.getLogger("hwidgets")
        hlogger.addHandler(logging.StreamHandler(sys.stdout))
        logging.disable(logging.NOTSET)
        hlogger.setLevel("DEBUG")

    # Environment fixes
    if sys.platform == 'linux':
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
        os.environ["QT_FONT_DPI"] = "96"
        os.environ["QT_QPA_PLATFORM"] = "xcb"
        os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "RoundPreferFloor"

    QApplication.setStyle("Fusion")
    application = QApplication(sys.argv)

    default_font = application.font()
    default_font.setStyleStrategy(QFont.PreferAntialias)
    default_font.setHintingPreference(QFont.PreferNoHinting)
    application.setFont(default_font)

    main_window = MainWindow()
    main_window.show()
    sys.exit(application.exec())


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()

























from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
import time
from typing import Any, Literal, Optional, Sequence
from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QRectF,
    Signal,
    QSize,
    QTime,
    QUrl,
    QObject,
    Qt,
    QAbstractItemModel,
    QPersistentModelIndex,
    QSize,
    QEvent,
    QTimer,

)
from PySide6.QtGui import (
    QPen,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QDragEnterEvent,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPalette,
    QPixmap,
    QRadialGradient,
    QRegion,
    QTransform,
    QWheelEvent,
    QFocusEvent,
    QPaintEvent,
    QContextMenuEvent,
    QKeyEvent,
    QResizeEvent,
    QInputMethodEvent,
    QValidator,
    QShowEvent,
    QHideEvent,
    QBitmap,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QStyle,
    QStyledItemDelegate,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QLabel,
    QCompleter,
    QAbstractItemDelegate,
    QStyleOptionComboBox,
    QAbstractItemView,
    QLineEdit,
    QGridLayout,
    QFrame,
    QListView,
)
from string import Template


from hytils import blue, lightcyan, lightgreen, lightgrey, orange, parent_directory, purple, yellow

from hwidgets.combobox import HComboBox
from hwidgets.debug import *
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

    hrl_style = Theme()

    window = QWidget()
    window.setStyleSheet(f"""
        background-color: {hrl_style.window_bgd};
        color: {hrl_style.font_color};
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
