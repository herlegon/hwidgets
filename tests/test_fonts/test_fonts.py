from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtGui import QFontDatabase, QFont
import sys

app = QApplication(sys.argv)

# Load Roboto fonts
font_id_roboto = QFontDatabase.addApplicationFont("Roboto-VariableFont_wdth,wght.ttf")
font_id_roboto_italic = QFontDatabase.addApplicationFont("Roboto-Italic-VariableFont_wdth,wght.ttf")

# Load Inter fonts
font_id_inter = QFontDatabase.addApplicationFont("Inter-VariableFont_opsz,wght.ttf")
font_id_inter_italic = QFontDatabase.addApplicationFont("Inter-Italic-VariableFont_opsz,wght.ttf")


font_id_open_sans = QFontDatabase.addApplicationFont("OpenSans-VariableFont_wdth,wght.ttf")
font_id_open_sans_italic = QFontDatabase.addApplicationFont("OpenSans-Italic-VariableFont_wdth,wght.ttf")

font_id_noto = QFontDatabase.addApplicationFont("NotoSans-VariableFont_wdth,wght.ttf")
font_id_noto_italic = QFontDatabase.addApplicationFont("NotoSans-Italic-VariableFont_wdth,wght.ttf")






# Check if fonts loaded successfully
if font_id_roboto < 0 or font_id_inter < 0:
    print("Error loading fonts!")
else:
    print("Fonts loaded successfully!")
    families_roboto = QFontDatabase.applicationFontFamilies(font_id_roboto)
    families_inter = QFontDatabase.applicationFontFamilies(font_id_inter)
    families_open_sans = QFontDatabase.applicationFontFamilies(font_id_open_sans)
    families_noto = QFontDatabase.applicationFontFamilies(font_id_noto)
    print(f"Roboto families: {families_roboto}")
    print(f"Inter families: {families_inter}")
    print(f"open sans families: {families_open_sans}")
    print(f"Noto families: {families_noto}")

# Create main window
window = QMainWindow()
window.setWindowTitle("Font Comparison: Roboto vs Inter")
window.resize(800, 400)

# Create central widget and main horizontal layout
central_widget = QWidget()
main_layout = QHBoxLayout(central_widget)

# Left column - Roboto
roboto_layout = QVBoxLayout()
roboto_title = QLabel("Roboto Font")
roboto_title.setFont(QFont("Roboto", 18, QFont.Bold))
roboto_layout.addWidget(roboto_title)

roboto_regular = QLabel("The quick brown fox jumps over the lazy dog")
roboto_regular.setFont(QFont("Roboto", 14))
roboto_layout.addWidget(roboto_regular)

roboto_bold = QLabel("The quick brown fox jumps over the lazy dog")
roboto_bold.setFont(QFont("Roboto", 14, QFont.Bold))
roboto_layout.addWidget(roboto_bold)

roboto_italic = QLabel("The quick brown fox jumps over the lazy dog")
font_roboto_italic = QFont("Roboto", 14)
font_roboto_italic.setItalic(True)
roboto_italic.setFont(font_roboto_italic)
roboto_layout.addWidget(roboto_italic)

roboto_sample = QLabel("FFmpeg ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
roboto_sample.setFont(QFont("Roboto", 12))
roboto_layout.addWidget(roboto_sample)

roboto_layout.addStretch()

# Right column - Noto Sans
noto_sans_layout = QVBoxLayout()
noto_sans_title = QLabel("Noto Sans")
noto_sans_title.setFont(QFont("NotoSans", 18, QFont.Bold))
noto_sans_layout.addWidget(noto_sans_title)
noto_sans_regular = QLabel("The quick brown fox jumps over the lazy dog")
noto_sans_regular.setFont(QFont("NotoSans", 14))
noto_sans_layout.addWidget(noto_sans_regular)
noto_sans_bold = QLabel("The quick brown fox jumps over the lazy dog")
noto_sans_bold.setFont(QFont("NotoSans", 14, QFont.Bold))
noto_sans_layout.addWidget(noto_sans_bold)
noto_sans_italic = QLabel("The quick brown fox jumps over the lazy dog")
font_noto_sans_italic = QFont("NotoSans", 14)
font_noto_sans_italic.setItalic(True)
noto_sans_italic.setFont(font_noto_sans_italic)
noto_sans_layout.addWidget(noto_sans_italic)
noto_sans_sample = QLabel("FFmpeg ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
noto_sans_sample.setFont(QFont("NotoSans", 12))
noto_sans_layout.addWidget(noto_sans_sample)
noto_sans_layout.addStretch()


# Right column - Inter
open_sans_layout = QVBoxLayout()
open_sans_title = QLabel("Open Sans")
open_sans_title.setFont(QFont("Open Sans", 18, QFont.Bold))
open_sans_layout.addWidget(open_sans_title)
open_sans_regular = QLabel("The quick brown fox jumps over the lazy dog")
open_sans_regular.setFont(QFont("Open Sans", 14))
open_sans_layout.addWidget(open_sans_regular)
open_sans_bold = QLabel("The quick brown fox jumps over the lazy dog")
open_sans_bold.setFont(QFont("Open Sans", 14, QFont.Bold))
open_sans_layout.addWidget(open_sans_bold)
open_sans_italic = QLabel("The quick brown fox jumps over the lazy dog")
font_open_sans_italic = QFont("Open Sans", 14)
font_open_sans_italic.setItalic(True)
open_sans_italic.setFont(font_open_sans_italic)
open_sans_layout.addWidget(open_sans_italic)
open_sans_sample = QLabel("FFmpeg ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
open_sans_sample.setFont(QFont("Open Sans", 12))
open_sans_layout.addWidget(open_sans_sample)
open_sans_layout.addStretch()


# Add both columns to main layout
main_layout.addLayout(roboto_layout)
main_layout.addLayout(noto_sans_layout)
main_layout.addLayout(open_sans_layout)

window.setCentralWidget(central_widget)
window.show()

sys.exit(app.exec())
