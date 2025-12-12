from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                               QWidget, QGraphicsDropShadowEffect, QSizePolicy, QPushButton)
from PySide6.QtCore import Qt, QPoint, Signal, QSize
from PySide6.QtGui import QFont, QIcon, QPixmap, QPainter, QColor, QMouseEvent
from typing import Type, Literal
from enum import IntEnum

from .divider import HHorizontalDivider
from .outlined_button import HOutlinedButton
from .label import HLabel
from .label import HSubtitle
from .styles import Theme
from .debug import (
    DEBUG_GEOMETRY,
    draw_widget_rect,
)

class TitleBar(QWidget):
    """Custom title bar that supports dragging"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self._dragging = False
        self._drag_start_offset = QPoint()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            window = self.window()
            if window:
                self._dragging = True
                # Calculate offset from window top-left to mouse position
                self._drag_start_offset = event.globalPosition().toPoint() - window.pos()
                event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._dragging and event.buttons() == Qt.MouseButton.LeftButton:
            window = self.window()
            if window:
                # Move window to current mouse position minus the initial offset
                window.move(event.globalPosition().toPoint() - self._drag_start_offset)
                event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._dragging = False
        super().mouseReleaseEvent(event)


class HMessageBox(QDialog):
    """Custom frameless message box with modern styling"""

    class StandardButton(IntEnum):
        NoButton = 0
        Ok = 1
        Cancel = 2
        Yes = 4
        No = 8
        Close = 16

    class Icon(IntEnum):
        NoIcon = 0
        Information = 1
        Warning = 2
        Critical = 3
        Question = 4

    buttonClicked = Signal(int)

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        theme: Type[Theme],
        title: str = "Message",
        message: str = "",
        icon: Icon = Icon.NoIcon,
        buttons: StandardButton = StandardButton.Ok,
    ):
        super().__init__(parent)
        self.theme = theme
        self._drag_pos = QPoint()
        self._buttons = {}
        self._result = 0
        self._title_text = title
        self._message_text = message
        self._icon_type = icon
        self._standard_buttons = buttons
        self._dragging = False
        self.f_style = theme.card

        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setModal(True)

        self._init_ui()
        self._update_stylesheet()

        # Initialize drag support after UI is created
        # self._init_drag_support()

        if message:
            self.setText(message)

        if icon != self.Icon.NoIcon:
            self.setIcon(icon)

        if buttons != self.StandardButton.NoButton:
            self.setStandardButtons(buttons)


    def _update_stylesheet(self) -> None:
        thickness: int = 1
        border_color: str = self.theme.default.selection
        stylesheet = """
            QWidget#container {{
                background-color: {bgd};
                border-radius: {radius}px;
                border: {thickness}px solid {border_color};
            }}
        """.format(
            bgd=self.theme.default.bgd,
            radius=int(self.f_style.radius * 1.5),
            thickness=thickness,
            border_color=border_color,
        )
        self.container.setStyleSheet(stylesheet)


    def _init_ui(self):
        """Initialize the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Container widget for styling
        self.container = QWidget()
        self.container.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.container.setObjectName("container")


        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(1, 0, 1, 0)
        container_layout.setSpacing(0)

        # Title bar
        self.title_bar = self._create_title_bar()
        container_layout.addWidget(self.title_bar)

        # Divider
        self.divider = HHorizontalDivider(self.container, theme=self.theme)
        container_layout.addWidget(self.divider)

        # Content area
        content_widget = QWidget()
        content_widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(16)

        # Icon and message layout
        message_layout = QHBoxLayout()
        message_layout.setSpacing(16)

        # Icon label
        self.icon_label = HLabel(theme=self.theme)
        self.icon_label.setFixedSize(48, 48)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.icon_label.setScaledContents(True)
        self.icon_label.hide()
        message_layout.addWidget(self.icon_label, 0, Qt.AlignmentFlag.AlignTop)

        # Message label
        self.message_label = HLabel(theme=self.theme)
        self.message_label.setWordWrap(True)
        self.message_label.setTextFormat(Qt.TextFormat.RichText)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.message_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        message_layout.addWidget(self.message_label, 1)
        content_layout.addLayout(message_layout)

        # Button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(12)
        self.button_layout.addStretch()
        content_layout.addLayout(self.button_layout)

        container_layout.addWidget(content_widget)
        main_layout.addWidget(self.container)

        # Set minimum size
        self.setMinimumWidth(400)


    def _create_title_bar(self) -> QWidget:
        """Create custom title bar"""
        title_bar = TitleBar(self)
        title_bar.setObjectName("titleBar")
        title_bar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        title_bar.setFixedHeight(32)

        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(16, 1, 16, 1)

        # Title label
        self.title_label = HSubtitle(theme=self.theme, text=self._title_text)
        self.title_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        layout.addWidget(self.title_label)

        layout.addStretch()

        # Close button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: {self.theme.default.radius}px;
                color: {self.theme.default.font_color};
                font-size: 24px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.theme.outlined_button.pressed};
            }}
            QPushButton:pressed {{
                background-color: {self.theme.outlined_button.pressed};
            }}
        """)
        self.close_btn.clicked.connect(self.reject)
        layout.addWidget(self.close_btn)

        return title_bar

    def setWindowTitle(self, title: str) -> None:
        """Set the window title"""
        super().setWindowTitle(title)
        self._title_text = title
        if hasattr(self, 'title_label'):
            self.title_label.setText(title)

    def setText(self, text: str) -> None:
        """Set the message text"""
        self._message_text = text
        self.message_label.setText(text)
        self.adjustSize()

    def text(self) -> str:
        """Get the message text"""
        return self._message_text

    def setIcon(self, icon: Icon | QIcon | QPixmap) -> None:
        """Set the message icon"""
        if isinstance(icon, self.Icon):
            self._icon_type = icon
            pixmap = self._get_standard_icon(icon)
            if pixmap:
                self.icon_label.setPixmap(pixmap)
                self.icon_label.show()
            else:
                self.icon_label.hide()
        elif isinstance(icon, (QIcon, QPixmap)):
            if isinstance(icon, QIcon):
                pixmap = icon.pixmap(48, 48)
            else:
                pixmap = icon
            self.icon_label.setPixmap(pixmap)
            self.icon_label.show()

    def _get_standard_icon(self, icon_type: Icon) -> QPixmap | None:
        """Get standard icon pixmap based on type"""
        if icon_type == self.Icon.NoIcon:
            return None

        # Create colored circle icons with symbols
        pixmap = QPixmap(48, 48)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Icon colors
        color_map = {
            self.Icon.Information: QColor("#2196F3"),  # Blue
            self.Icon.Warning: QColor("#FF9800"),       # Orange
            self.Icon.Critical: QColor("#F44336"),      # Red
            self.Icon.Question: QColor("#9C27B0"),      # Purple
        }

        color = color_map.get(icon_type, QColor("#2196F3"))

        # Draw circle
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, 48, 48)

        # Draw symbol
        painter.setPen(QColor("white"))
        font = QFont(self.theme.default.font.family, 24, QFont.Weight.Bold)
        painter.setFont(font)

        symbol_map = {
            self.Icon.Information: "i",
            self.Icon.Warning: "!",
            self.Icon.Critical: "×",
            self.Icon.Question: "?",
        }

        symbol = symbol_map.get(icon_type, "")
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, symbol)
        painter.end()

        return pixmap

    def setStandardButtons(self, buttons: StandardButton) -> None:
        """Set standard buttons"""
        self._standard_buttons = buttons

        # Clear existing buttons
        for button in self._buttons.values():
            button.deleteLater()
        self._buttons.clear()

        # Button configuration
        button_config = [
            (self.StandardButton.Ok, "OK"),
            (self.StandardButton.Cancel, "Cancel"),
            (self.StandardButton.Yes, "Yes"),
            (self.StandardButton.No, "No"),
            (self.StandardButton.Close, "Close"),
        ]

        # Add buttons in order
        for btn_type, text in button_config:
            if buttons & btn_type:
                self.addButton(text, btn_type)

    def addButton(self, text: str, role: StandardButton) -> HOutlinedButton:
        """Add a custom button"""
        button = HOutlinedButton(self, theme=self.theme, text=text)
        button.clicked.connect(lambda checked=False, r=role: self._on_button_clicked(r))
        self._buttons[role] = button
        self.button_layout.addWidget(button)
        return button

    def _on_button_clicked(self, role: StandardButton) -> None:
        """Handle button click"""
        self._result = role
        self.buttonClicked.emit(role)

        # Auto-close behavior
        if role in (self.StandardButton.Ok, self.StandardButton.Yes, self.StandardButton.Close):
            self.accept()
        elif role in (self.StandardButton.Cancel, self.StandardButton.No):
            self.reject()

    def clickedButton(self) -> StandardButton:
        """Get the clicked button"""
        return self._result







    # Static convenience methods
    @staticmethod
    def information(
        parent: QWidget | None,
        title: str,
        message: str,
        theme: Type[Theme],
        buttons: StandardButton = StandardButton.Ok,
    ) -> StandardButton:
        """Show information message box"""
        msgbox = HMessageBox(
            parent=parent,
            theme=theme,
            title=title,
            message=message,
            icon=HMessageBox.Icon.Information,
            buttons=buttons,
        )
        msgbox.exec()
        return msgbox.clickedButton()

    @staticmethod
    def warning(
        parent: QWidget | None,
        title: str,
        message: str,
        theme: Type[Theme],
        buttons: StandardButton = StandardButton.Ok,
    ) -> StandardButton:
        """Show warning message box"""
        msgbox = HMessageBox(
            parent=parent,
            theme=theme,
            title=title,
            message=message,
            icon=HMessageBox.Icon.Warning,
            buttons=buttons,
        )
        msgbox.exec()
        return msgbox.clickedButton()

    @staticmethod
    def critical(
        parent: QWidget | None,
        title: str,
        message: str,
        theme: Type[Theme],
        buttons: StandardButton = StandardButton.Ok,
    ) -> StandardButton:
        """Show critical message box"""
        msgbox = HMessageBox(
            parent=parent,
            theme=theme,
            title=title,
            message=message,
            icon=HMessageBox.Icon.Critical,
            buttons=buttons,
        )
        msgbox.exec()
        return msgbox.clickedButton()

    @staticmethod
    def question(
        parent: QWidget | None,
        title: str,
        message: str,
        theme: Type[Theme],
        buttons: StandardButton = StandardButton.Yes | StandardButton.No,
    ) -> StandardButton:
        """Show question message box"""
        msgbox = HMessageBox(
            parent=parent,
            theme=theme,
            title=title,
            message=message,
            icon=HMessageBox.Icon.Question,
            buttons=buttons,
        )
        msgbox.exec()
        return msgbox.clickedButton()


