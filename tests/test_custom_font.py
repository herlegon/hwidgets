
import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel
from hwidgets.hstyle import Theme
from hwidgets.button import HButton
from hwidgets.line_edit import HLineEdit
from hwidgets.combobox import HComboBox
from hwidgets.checkbox import HCheckBox
from hwidgets.radio_button import HRadioButton
from hwidgets.titles import HTitle

def main():
    app = QApplication(sys.argv)

    # Custom Theme with a distinct font
    class CustomStyle(Theme):
        font_family = "Courier New"
        font_size = 14

    window = QWidget()
    layout = QVBoxLayout(window)

    layout.addWidget(HTitle(theme=CustomStyle, text="Custom Font Test"))
    layout.addWidget(HButton(theme=CustomStyle, text="Button"))
    layout.addWidget(HLineEdit(theme=CustomStyle, text="LineEdit"))
    layout.addWidget(HComboBox(hstyle=CustomStyle, currentText="ComboBox"))
    layout.addWidget(HCheckBox(theme=CustomStyle)) # Checkbox might not show text but we test instantiation
    layout.addWidget(HRadioButton(theme=CustomStyle))

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
