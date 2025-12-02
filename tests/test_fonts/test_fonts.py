import os
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtGui import QFontDatabase, QFont
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt

os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_FONT_DPI"] = "96"
if sys.platform == 'linux':
    # Environment fixes
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "RoundPreferFloor"

# os.environ["QT_DEBUG_FONTS"] = "1"

app = QApplication(sys.argv)

default_font = app.font()
default_font.setStyleStrategy(QFont.PreferAntialias)
default_font.setHintingPreference(QFont.PreferNoHinting)   # or PreferFullHinting
app.setFont(default_font)

# default_font = app.font()
# default_font.setStyleStrategy(QFont.PreferAntialias)
# default_font.setHintingPreference(QFont.PreferNoHinting)
# app.setFont(default_font)


# Load Roboto fonts
font_id_roboto = QFontDatabase.addApplicationFont("Roboto-VariableFont_wdth,wght.ttf")
font_id_italic = QFontDatabase.addApplicationFont("Roboto-Italic-VariableFont_wdth,wght.ttf")

# Load Inter fonts
font_id_inter = QFontDatabase.addApplicationFont("Inter-VariableFont_opsz,wght.ttf")
font_id_inter_italic = QFontDatabase.addApplicationFont("Inter-Italic-VariableFont_opsz,wght.ttf")


font_id_open_sans = QFontDatabase.addApplicationFont("OpenSans-VariableFont_wdth,wght.ttf")
font_id_open_sans_italic = QFontDatabase.addApplicationFont("OpenSans-Italic-VariableFont_wdth,wght.ttf")

font_id_noto = QFontDatabase.addApplicationFont("NotoSans-VariableFont_wdth,wght.ttf")
font_id_noto_italic = QFontDatabase.addApplicationFont("NotoSans-Italic-VariableFont_wdth,wght.ttf")

font_id_dejavu = QFontDatabase.addApplicationFont("DejaVuSans.ttf")

font_id_plex_mono_regular = QFontDatabase.addApplicationFont("IBMPlexMono-Regular.ttf")
font_id_plex_mono_semi_bold = QFontDatabase.addApplicationFont("IBMPlexMono-SemiBold.ttf")
font_id_JetBrainsMono = QFontDatabase.addApplicationFont("JetBrainsMono[wght].ttf")
font_id_JetBrainsMono_italic = QFontDatabase.addApplicationFont("JetBrainsMono-Italic[wght].ttf")



# Check if fonts loaded successfully
if font_id_roboto < 0 or font_id_inter < 0:
    print("Error loading fonts!")
else:
    print("Fonts loaded successfully!")
    families_roboto = QFontDatabase.applicationFontFamilies(font_id_roboto)
    families_inter = QFontDatabase.applicationFontFamilies(font_id_inter)
    families_open_sans = QFontDatabase.applicationFontFamilies(font_id_open_sans)
    families_noto = QFontDatabase.applicationFontFamilies(font_id_noto)
    families_dejavu = QFontDatabase.applicationFontFamilies(font_id_dejavu)
    print(f"Roboto families: {families_roboto}")
    print(f"Inter families: {families_inter}")
    print(f"open sans families: {families_open_sans}")
    print(f"Noto families: {families_noto}")
    print(f"DejaVu families: {families_dejavu}")

# Create main window
window = QMainWindow()
window.setWindowTitle("Font Comparison: Roboto vs Inter")
window.resize(800, 400)

# Create central widget and main horizontal layout
central_widget = QWidget()
main_layout = QVBoxLayout(central_widget)


layouts: list[QVBoxLayout] = []
for f_name in (
    "Roboto",
    "Inter",
    "Noto Sans",
    # "DejaVu Sans",
    # "Open Sans",

    "JetBrains Mono",
    "IBM Plex Mono",
):
    layout = QVBoxLayout()
    title = QLabel(f_name)
    title.setFont(QFont(f_name, 16, QFont.Bold))
    layout.addWidget(title)

    regular = QLabel("The quick brown fox jumps over the lazy dog")
    regular.setFont(QFont(f_name, 14))
    layout.addWidget(regular)

    bold = QLabel("The quick brown fox jumps over the lazy dog")
    bold.setFont(QFont(f_name, 14, QFont.Bold))
    layout.addWidget(bold)

    italic = QLabel("The quick brown fox jumps over the lazy dog")
    font_italic = QFont(f_name, 14)
    font_italic.setItalic(True)
    italic.setFont(font_italic)
    layout.addWidget(italic)

    sample = QLabel("[pip] FFmpeg ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    sample.setFont(QFont(f_name, 12))
    layout.addWidget(sample)

    sample = QLabel("[pip] FFmpeg ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    sample.setFont(QFont(f_name, 10))
    layout.addWidget(sample)

    layout.addStretch()
    layouts.append(layout)

central_widget.font().setStyleStrategy(QFont.StyleStrategy.PreferQuality)
central_widget.font().setHintingPreference(QFont.HintingPreference.PreferNoHinting)
for l in layouts:
    main_layout.addLayout(l)

window.setCentralWidget(central_widget)
window.show()

sys.exit(app.exec())
