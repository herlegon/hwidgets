import os
import signal
import sys
from hytils import parent_directory
sys.path.append(os.path.join(parent_directory(__file__), "hwidgets"))
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from hwidgets import (
    StyleManager,
    HDescription,
    HMessageBox,
    HLabel,
    HOutlinedButton,
)
from hwidgets.label import HAppTitle


class HMessageBoxTestWindow(QMainWindow):
    """Test window to display all HMessageBox variants"""

    def __init__(self):
        super().__init__()
        self.theme = StyleManager().get_theme()
        self.setWindowTitle("HMessageBox Style Validation Test")
        self.setMinimumSize(600, 700)

        # Setup UI
        self._setup_ui()

        # Apply theme to main window
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.theme.window_bgd};
            }}
        """)

    def _setup_ui(self):
        """Setup the test UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Title
        title = HAppTitle(theme=self.theme, text="HMessageBox Style Validation")
        layout.addWidget(title)

        # Description
        desc = HDescription(
            theme=self.theme,
            text="Click each button to test different message box variants and styles."
        )
        layout.addWidget(desc)

        layout.addSpacing(20)

        # Test buttons for each variant
        test_cases = [
            ("Information - Simple", self.test_information_simple),
            ("Information - Long Text", self.test_information_long),
            ("Warning - Simple", self.test_warning_simple),
            ("Warning - With Details", self.test_warning_details),
            ("Critical - Error", self.test_critical_error),
            ("Critical - Multiple Lines", self.test_critical_multiline),
            ("Question - Yes/No", self.test_question_yesno),
            ("Question - Yes/No/Cancel", self.test_question_yesnocancel),
            ("Custom - Ok/Cancel", self.test_custom_okcancel),
            ("Custom - Multiple Buttons", self.test_custom_multiple),
            ("Custom Icon - Pixmap", self.test_custom_icon),
            ("No Icon - Text Only", self.test_no_icon),
            ("Rich Text - HTML", self.test_rich_text),
            ("All Button Types", self.test_all_buttons),
        ]

        for label, callback in test_cases:
            btn = HOutlinedButton(self, theme=self.theme, text=label)
            btn.clicked.connect(callback)
            layout.addWidget(btn)

        layout.addStretch()

        # Result label
        self.result_label = HLabel(theme=self.theme, text="Click a button to start testing")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

    def show_result(self, result: HMessageBox.StandardButton, test_name: str):
        """Display the result of the last test"""
        button_names = {
            HMessageBox.StandardButton.Ok: "OK",
            HMessageBox.StandardButton.Cancel: "Cancel",
            HMessageBox.StandardButton.Yes: "Yes",
            HMessageBox.StandardButton.No: "No",
            HMessageBox.StandardButton.Close: "Close",
        }
        button_text = button_names.get(result, f"Unknown ({result})")
        self.result_label.setText(f"Test: {test_name} | Clicked: {button_text}")

    # Test cases
    def test_information_simple(self):
        """Test simple information dialog"""
        result = HMessageBox.information(
            parent=self,
            title="Information",
            message="This is a simple information message.",
            theme=self.theme,
        )
        self.show_result(result, "Information - Simple")

    def test_information_long(self):
        """Test information dialog with long text"""
        result = HMessageBox.information(
            parent=self,
            title="Detailed Information",
            message="This is a longer information message that contains more details. "
                    "It demonstrates how the message box handles text wrapping and "
                    "maintains readability with multiple lines of content. "
                    "The dialog should automatically adjust its size to accommodate "
                    "the text while remaining visually appealing.",
            theme=self.theme,
        )
        self.show_result(result, "Information - Long Text")

    def test_warning_simple(self):
        """Test simple warning dialog"""
        result = HMessageBox.warning(
            parent=self,
            title="Warning",
            message="This operation may have unintended consequences.",
            theme=self.theme,
        )
        self.show_result(result, "Warning - Simple")

    def test_warning_details(self):
        """Test warning dialog with details"""
        result = HMessageBox.warning(
            parent=self,
            title="Unsaved Changes",
            message="You have unsaved changes in your document. "
                    "These changes will be lost if you continue without saving.",
            theme=self.theme,
            buttons=HMessageBox.StandardButton.Ok,
        )
        self.show_result(result, "Warning - With Details")

    def test_critical_error(self):
        """Test critical error dialog"""
        result = HMessageBox.critical(
            parent=self,
            title="Critical Error",
            message="An unexpected error has occurred. The application may need to restart.",
            theme=self.theme,
        )
        self.show_result(result, "Critical - Error")

    def test_critical_multiline(self):
        """Test critical dialog with multiple lines"""
        result = HMessageBox.critical(
            parent=self,
            title="Operation Failed",
            message="Failed to save the file.\n\nError details:\n"
                    "- Permission denied\n"
                    "- Path: /protected/folder/file.txt\n"
                    "- Error code: 403",
            theme=self.theme,
        )
        self.show_result(result, "Critical - Multiple Lines")

    def test_question_yesno(self):
        """Test question dialog with Yes/No"""
        result = HMessageBox.question(
            parent=self,
            title="Confirm Action",
            message="Are you sure you want to delete this item? This action cannot be undone.",
            theme=self.theme,
            buttons=HMessageBox.StandardButton.Yes | HMessageBox.StandardButton.No,
        )
        self.show_result(result, "Question - Yes/No")

    def test_question_yesnocancel(self):
        """Test question dialog with Yes/No/Cancel"""
        result = HMessageBox.question(
            parent=self,
            title="Save Changes?",
            message="Do you want to save changes before closing?",
            theme=self.theme,
            buttons=HMessageBox.StandardButton.Yes |
                    HMessageBox.StandardButton.No |
                    HMessageBox.StandardButton.Cancel,
        )
        self.show_result(result, "Question - Yes/No/Cancel")

    def test_custom_okcancel(self):
        """Test custom dialog with Ok/Cancel"""
        msgbox = HMessageBox(
            parent=self,
            theme=self.theme,
            title="Confirm Operation",
            message="This will perform a custom operation. Do you want to continue?",
            icon=HMessageBox.Icon.Question,
            buttons=HMessageBox.StandardButton.Ok | HMessageBox.StandardButton.Cancel,
        )
        msgbox.exec()
        self.show_result(msgbox.clickedButton(), "Custom - Ok/Cancel")

    def test_custom_multiple(self):
        """Test custom dialog with multiple button types"""
        msgbox = HMessageBox(
            parent=self,
            theme=self.theme,
            title="Multiple Options",
            message="Choose an action to proceed:",
            icon=HMessageBox.Icon.Information,
            buttons=HMessageBox.StandardButton.Yes |
                    HMessageBox.StandardButton.No |
                    HMessageBox.StandardButton.Cancel |
                    HMessageBox.StandardButton.Close,
        )
        msgbox.exec()
        self.show_result(msgbox.clickedButton(), "Custom - Multiple Buttons")

    def test_custom_icon(self):
        """Test dialog with custom icon (if available)"""
        msgbox = HMessageBox(
            parent=self,
            theme=self.theme,
            title="Custom Icon Test",
            message="This message box tests custom icon functionality.",
            icon=HMessageBox.Icon.Information,
            buttons=HMessageBox.StandardButton.Ok,
        )

        # You can set a custom icon here if you have one
        # from PySide6.QtGui import QIcon
        # custom_icon = QIcon("path/to/icon.png")
        # msgbox.setIcon(custom_icon)

        msgbox.exec()
        self.show_result(msgbox.clickedButton(), "Custom Icon")

    def test_no_icon(self):
        """Test dialog without icon"""
        msgbox = HMessageBox(
            parent=self,
            theme=self.theme,
            title="No Icon",
            message="This message box has no icon, just text content.",
            icon=HMessageBox.Icon.NoIcon,
            buttons=HMessageBox.StandardButton.Ok,
        )
        msgbox.exec()
        self.show_result(msgbox.clickedButton(), "No Icon - Text Only")

    def test_rich_text(self):
        """Test dialog with rich text (HTML)"""
        msgbox = HMessageBox(
            parent=self,
            theme=self.theme,
            title="Rich Text Support",
            message="<b>Bold text</b>, <i>italic text</i>, and <u>underlined text</u>.<br><br>"
                    "You can also use:<br>"
                    "• <span style='color: #2196F3;'>Colored text</span><br>"
                    "• Different <span style='font-size: 16px;'>font sizes</span><br>"
                    "• <a href='https://example.com'>Links</a> (if enabled)",
            icon=HMessageBox.Icon.Information,
            buttons=HMessageBox.StandardButton.Ok,
        )
        msgbox.exec()
        self.show_result(msgbox.clickedButton(), "Rich Text - HTML")

    def test_all_buttons(self):
        """Test dialog with all button types"""
        msgbox = HMessageBox(
            parent=self,
            theme=self.theme,
            title="All Button Types",
            message="This dialog shows all available standard buttons.",
            icon=HMessageBox.Icon.Question,
            buttons=HMessageBox.StandardButton.Ok |
                    HMessageBox.StandardButton.Cancel |
                    HMessageBox.StandardButton.Yes |
                    HMessageBox.StandardButton.No |
                    HMessageBox.StandardButton.Close,
        )
        msgbox.exec()
        self.show_result(msgbox.clickedButton(), "All Button Types")


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    """Main entry point"""
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    # Create and show test window
    window = HMessageBoxTestWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
