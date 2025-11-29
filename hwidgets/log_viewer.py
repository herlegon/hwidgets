import logging
from pprint import pprint
import re
from string import Template
from typing import Type

from PySide6.QtCore import (
    Qt,
    Signal,
    QObject,
)
from PySide6.QtGui import (
    QColor,
    QTextCursor,
    QTextCharFormat,
    QFont,
)
from PySide6.QtWidgets import (
    QWidget,
    QPlainTextEdit,
)

from .plain_text_edit import (
    HPlainTextEdit,
    OverlayVScrollBar,
)
from .style_manager import Theme
from .utils import (
    load_png_icon,
    load_qss,
)


class QtLogHandler(QObject, logging.Handler):
    # Emit both message and log level name
    new_log = Signal(str, int)

    def __init__(self):
        QObject.__init__(self)
        logging.Handler.__init__(self)


    def emit(self, record: logging.LogRecord):
        msg = self.format(record)
        self.new_log.emit(msg, record.levelno)


class HLogViewer(HPlainTextEdit):

    _COLOR_MAP = {
        logging.DEBUG: QColor("#efefef"),   # gray
        logging.INFO: QColor("#55aa55"),    # green
        logging.WARNING: QColor("#ffaa00"), # orange
        logging.ERROR: QColor("#ff5555"),   # red
        logging.CRITICAL: QColor("#ff0000") # bright red
    }

    _ANSI_COLOR_MAP = {
        "30": QColor("#000000"),  # Black
        "31": QColor("#ff5555"),  # Red
        "32": QColor("#55ff55"),  # Green
        "33": QColor("#ffff55"),  # Yellow
        "34": QColor("#5555ff"),  # Blue
        "35": QColor("#ff55ff"),  # Magenta
        "36": QColor("#55ffff"),  # Cyan
        "37": QColor("#ffffff"),  # White
        "90": QColor("#888888"),  # Bright black (gray)
        "91": QColor("#ff7777"),
        "92": QColor("#77ff77"),
        "93": QColor("#ffff77"),
        "94": QColor("#7777ff"),
        "95": QColor("#ff77ff"),
        "96": QColor("#77ffff"),
        "97": QColor("#ffffff"),
    }

    _ansi_pattern = re.compile(r"\x1B\[(\d+)(;\d+)*m")

    _LEVEL_SYMBOLS = {
        logging.DEBUG: "•",
        logging.INFO: "→",
        logging.WARNING: "⚠",
        logging.ERROR: "✖",
        logging.CRITICAL: "‼",
    }

    _LEVEL_PREFIX = {
        logging.DEBUG: "[D]",
        5: "[V]",               # example VERBOSE custom level if used
        logging.INFO: "[I]",
        logging.WARNING: "[W]",
        logging.ERROR: "[E]",
        logging.CRITICAL: "[C]",
    }

    def __init__(
        self,
        text: str | QWidget | None = None,
        /,
        parent: QWidget | None = None,
        *,
        theme: Type[Theme],
        tabChangesFocus: bool | None = None,
        documentTitle: str | None = None,
        undoRedoEnabled: bool | None = None,
        lineWrapMode: QPlainTextEdit.LineWrapMode | None = None,
        readOnly: bool | None = None,
        plainText: str | None = None,
        overwriteMode: bool | None = None,
        tabStopDistance: float | None = None,
        cursorWidth: int | None = None,
        textInteractionFlags: Qt.TextInteractionFlag | None = None,
        blockCount: int | None = None,
        maximumBlockCount: int | None = None,
        backgroundVisible: bool | None = None,
        centerOnScroll: bool | None = None,
        placeholderText: str | None = None,
        clearButtonEnabled: bool = True,
    ) -> None:
        self.theme = theme
        self.log_style = theme.log_viewer

        super().__init__(
            parent=parent,
            theme=theme,
            tabChangesFocus=True,
            documentTitle=documentTitle,
            undoRedoEnabled=False,
            lineWrapMode=True,
            readOnly=True,
            plainText=plainText,
            clearButtonEnabled=False,
        )
        self.setContentsMargins(20, 0, 20, 10)
        self._update_stylesheet()

        # --- GUI Log Handler ---
        self.gui_handler = QtLogHandler()
        self.gui_handler.new_log.connect(self.append_colored_log)


    def _update_stylesheet(self) -> None:
        log_style = self.log_style
        radius = self.theme.default.radius

        padding_left, padding_right = radius, radius

        # Same style sheet as line edit
        qss_template = Template(load_qss("plain_text_edit.qss"))
        qss = qss_template.substitute(
            radius=f"{radius}px",
            padding_right=f"{padding_right}px",
            padding_left=f"{padding_left}px",

            widget_bgd=f"{log_style.bgd}",
            hover=f"{log_style.hover}",
            disabled=f"{log_style.disabled}",

            border_color=f"{log_style.border}",
            border_read_only_color=f"{log_style.border_read_only}",
            border_edition=f"{log_style.selection}",

            selection=f"{log_style.selection}",

            font_color=f"{log_style.font_color}",
            font_color_disabled=f"{log_style.font_color_disabled}",
        )
        self.setStyleSheet(qss)
        self.viewer_font = self.log_style.font.make_font()
        self.document().setDefaultFont(self.viewer_font)
        self.setFont(self.viewer_font)


    def setPlainText(self, text: str) -> None:
        super().setPlainText("")
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        fmt = QTextCharFormat()
        fmt.setFont(self.viewer_font)
        cursor.insertText(text, fmt)


    def appendPlainText(self, message: str = ""):
        self._append_log(message)


    def _append_log(self, message):
        # Fallback for plain text append without level
        self.append_colored_log(message, logging.INFO)


    def append_colored_log(self, msg: str, levelno: int):
        """Append a log message with ANSI and log-level colors."""

        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)

        default_color = self._COLOR_MAP.get(levelno, QColor(self.log_style.font_color))

        fmt = QTextCharFormat()
        fmt.setFont(self.viewer_font)
        fmt.setForeground(default_color)

        prefix = self._LEVEL_PREFIX.get(levelno, "[?]") + " "

        # Insert the prefix
        prefix_fmt = QTextCharFormat()
        prefix_fmt.setFont(self.viewer_font)
        prefix_fmt.setForeground(default_color)
        cursor.insertText(prefix, prefix_fmt)

        # Split text by ANSI color codes
        parts = self._ansi_pattern.split(msg)

        current_color = default_color
        for part in parts:
            if part is None:
                continue
            if part.isdigit() and part in self._ANSI_COLOR_MAP:
                current_color = self._ANSI_COLOR_MAP[part]
                fmt.setForeground(current_color)
            elif part == "00":
                # reset code
                fmt.setForeground(default_color)
                current_color = default_color
            else:
                cursor.insertText(part, fmt)

        cursor.insertText("\n", fmt)

        # Scroll to bottom
        self.moveCursor(QTextCursor.End)
