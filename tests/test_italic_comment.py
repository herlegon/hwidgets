import sys
from PySide6.QtWidgets import QApplication
from hwidgets.label import HComment, HLabel, HSubtitle
from hwidgets.style_manager import StyleManager

def main():
    app = QApplication(sys.argv)
    theme = StyleManager.get_theme()

    print("Testing HComment...")
    # Test init with italic=True
    comment = HComment(theme=theme, text="Italic Comment", italic=True)
    if "font-style: italic;" not in comment.styleSheet():
        print("FAIL: Italic style not found in stylesheet (init)")
        sys.exit(1)

    # Test setItalic(False)
    comment.setItalic(False)
    if "font-style: normal;" not in comment.styleSheet():
        print("FAIL: Normal style not found in stylesheet after setItalic(False)")
        sys.exit(1)

    # Test setItalic(True)
    comment.setItalic(True)
    if "font-style: italic;" not in comment.styleSheet():
        print("FAIL: Italic style not found in stylesheet after setItalic(True)")
        sys.exit(1)

    print("Testing HLabel...")
    label = HLabel(theme=theme, text="Label")

    # Test setWeight
    label.setWeight(700)
    if "font-weight: 700;" not in label.styleSheet():
        print("FAIL: Font weight 700 not found in stylesheet")
        sys.exit(1)

    # Test setFontSize
    label.setFontSize(20)
    if "font-size: 20pt;" not in label.styleSheet():
        print("FAIL: Font size 20pt not found in stylesheet")
        sys.exit(1)

    print("Testing HSubtitle...")
    subtitle = HSubtitle(theme=theme, text="Subtitle")
    # Verify default weight/size from theme are preserved (assuming theme defaults)
    # This is a bit tricky without knowing exact theme values, but we can check if they are present
    if "font-size:" not in subtitle.styleSheet() or "font-weight:" not in subtitle.styleSheet():
         print("FAIL: Font size/weight missing from subtitle stylesheet")
         sys.exit(1)

    print("PASS: HLabel refactor verified")

if __name__ == "__main__":
    main()
