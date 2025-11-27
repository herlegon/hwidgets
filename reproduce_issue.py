from hwidgets.style_manager import StyleManager
from pprint import pprint

def test_line_edit_style():
    theme = StyleManager.get_theme("default")
    line_edit_style = theme.line_edit

    print("LineEditStyle:")
    pprint(line_edit_style)

    print("\nCommon:")
    pprint(theme.default)

    # Check if empty members in LineEditStyle are overridden by common members
    # expected: hover, selection, disabled should be taken from common if they are "" in default LineEditStyle
    # and not present in toml.

    # In default.toml:
    # [line_edit]
    # disabled = "#232223"
    # # selection = "#7777FF"

    # So 'disabled' is set in toml, it should be "#232223".
    # 'selection' is commented out, so it is NOT in toml. Default LineEditStyle.selection is "".
    # Common.selection is "#7777FF".
    # So we expect line_edit_style.selection to be "#7777FF".

    # 'hover' is not in toml. Default LineEditStyle.hover is "".
    # Common.hover is "#66636D".
    # So we expect line_edit_style.hover to be "#66636D".

    # 'font_color' is not in toml. Default LineEditStyle.font_color is "".
    # Common.font_color is "#d4d4d8".
    # So we expect line_edit_style.font_color to be "#d4d4d8".

    failures = []

    if line_edit_style.disabled != "#232223":
        failures.append(f"disabled: expected '#232223', got '{line_edit_style.disabled}'")

    if line_edit_style.selection != theme.default.selection:
         failures.append(f"selection: expected '{theme.default.selection}', got '{line_edit_style.selection}'")

    # 'hover' IS in toml as "". So we expect line_edit_style.hover to be "".
    if line_edit_style.hover != "":
         failures.append(f"hover: expected '', got '{line_edit_style.hover}'")

    if line_edit_style.font_color != theme.default.font_color:
         failures.append(f"font_color: expected '{theme.default.font_color}', got '{line_edit_style.font_color}'")

    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(f)
    else:
        print("\nSUCCESS: All checks passed.")

if __name__ == "__main__":
    test_line_edit_style()
