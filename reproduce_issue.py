
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import QTimer
from hwidgets.plain_text_edit import HPlainTextEdit
from hwidgets.style_manager import StyleManager

def test_issue():
    app = QApplication(sys.argv)
    theme = StyleManager.get_theme()

    widget = QWidget()
    layout = QVBoxLayout(widget)

    # Case 1: Initialization with long text
    long_text = "line\n" * 100
    pte = HPlainTextEdit(long_text, theme=theme)
    layout.addWidget(pte)

    widget.resize(400, 300)
    widget.show()

    def check_initialization():
        scrollbar_visible = pte.overlay_vbar.isVisible()
        button_pos = pte.clear_button.pos()
        print(f"Init - Scrollbar visible: {scrollbar_visible}")
        print(f"Init - Button pos: {button_pos}")

        scrollbar_width = pte.overlay_vbar.width() + 4 if scrollbar_visible else 4
        expected_x = pte.width() - pte.clear_button.width() - scrollbar_width

        print(f"Init - Expected x: {expected_x}, Actual x: {button_pos.x()}")

        if abs(expected_x - button_pos.x()) > 2:
            print("FAIL: Button position incorrect after initialization")
        else:
            print("PASS: Button position correct after initialization")

        # Case 2: Paste long text into empty
        pte.clear()
        QTimer.singleShot(100, check_paste)

    def check_paste():
        print("\nClearing text and simulating paste...")
        pte.setPlainText(long_text)

        # Give time for timer to fire
        QTimer.singleShot(100, verify_paste)

    def verify_paste():
        scrollbar_visible = pte.overlay_vbar.isVisible()
        button_pos = pte.clear_button.pos()
        print(f"Paste - Scrollbar visible: {scrollbar_visible}")
        print(f"Paste - Button pos: {button_pos}")

        scrollbar_width = pte.overlay_vbar.width() + 4 if scrollbar_visible else 4
        expected_x = pte.width() - pte.clear_button.width() - scrollbar_width

        print(f"Paste - Expected x: {expected_x}, Actual x: {button_pos.x()}")

        if abs(expected_x - button_pos.x()) > 2:
            print("FAIL: Button position incorrect after paste")
        else:
            print("PASS: Button position correct after paste")

        app.quit()

    QTimer.singleShot(500, check_initialization)
    app.exec()

if __name__ == "__main__":
    test_issue()
