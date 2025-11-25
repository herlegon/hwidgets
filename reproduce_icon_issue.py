import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from hwidgets.line_edit import HLineEdit
from hwidgets.style_manager import StyleManager

def main():
    app = QApplication(sys.argv)

    theme = StyleManager.get_theme("default")

    window = QWidget()
    window.setWindowTitle("HLineEdit Icon Issue")
    window.resize(400, 200)
    window.setStyleSheet(f"background-color: {theme.window_bgd};")

    layout = QVBoxLayout(window)

    # HLineEdit with text and clear button enabled
    line_edit = HLineEdit(theme=theme, clearButtonEnabled=True)
    line_edit.setText("Some text here...")

    layout.addWidget(line_edit)

    window.show()

    # Close after a short delay for automated testing purposes
    # QTimer.singleShot(1000, app.quit)
    # For now, just exit immediately if running in agent mode to verify no crash
    print("Successfully created HLineEdit with icon")

    # sys.exit(app.exec())
    # Just return to avoid blocking if we want to just check init
    return

if __name__ == "__main__":
    main()
