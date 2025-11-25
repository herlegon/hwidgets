# simple_round_plaintextedit.py
from PySide6.QtWidgets import QApplication, QPlainTextEdit, QWidget, QVBoxLayout
import sys

QApplication.setStyle("Fusion")
app = QApplication(sys.argv)

w = QWidget()
w.setWindowTitle("Rounded QPlainTextEdit - Simple")
layout = QVBoxLayout(w)

editor = QPlainTextEdit(w)
editor.setPlainText("This is a QPlainTextEdit with rounded corners.\nTry focusing it.")
editor.setMinimumSize(360, 180)

# Style both the widget and its viewport so background and border are rounded
# editor.setStyleSheet("""
# QPlainTextEdit {
#     border: 2px solid #c0c0c0;
#     border-radius: 12px;
#     padding: 8px;                /* space between border and text */
#     background: rgb(158, 255, 197);
#     selection-background-color: #cce4ff;
# }

# /* The viewport is the internal scrolling area that actually holds the text */
# QPlainTextEdit::viewport {
#     border-radius: 12px;
#     background: transparent;     /* use widget background for consistent rounding */
# }

# /* focus state */
# QPlainTextEdit:focus {
#                      border-radius: 12px;
#     border: 2px solid #5b9bd5;
# }
# """)
editor.setStyleSheet("border-radius: 48px; background-color: rgb(158, 255, 197);")
editor.viewport().setAutoFillBackground(False)

layout.addWidget(editor)
w.setLayout(layout)
w.resize(400, 240)
w.show()
sys.exit(app.exec())
