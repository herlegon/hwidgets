from PySide6.QtGui import QFontDatabase
from pathlib import Path

_fonts_loaded = False

def load_fonts():
    global _fonts_loaded
    if _fonts_loaded:
        return

    fonts_path = (Path(__file__).parent / "fonts").resolve()
    ids: list[str] = []
    for font_file in fonts_path.glob("*.ttf"):
        ids.append(QFontDatabase.addApplicationFont(str(font_file)))

    # for id in ids:
    #     families = QFontDatabase.applicationFontFamilies(id)
    #     print(f"families: {families}")

    _fonts_loaded = True
