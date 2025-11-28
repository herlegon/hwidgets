from pprint import pprint
import re
from pathlib import Path
import signal
import sys


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    if len(sys.argv) != 2:
        print("Usage: python q_to_h.py <path_to_ui_python_file>")
        sys.exit(1)

    ui_path: Path = Path(sys.argv[1]).resolve()
    if not ui_path.exists():
        print(f"❌ File not found: {ui_path}")
        sys.exit(1)

    text = Path(ui_path).read_text(encoding="utf-8")


    # Widgets
    WIDGET_MAP = {
        "QComboBox": "HComboBox",
        "QRadioButton": "HRadioButton",
        "QCheckBox": "HCheckBox",
        "QLabel": "HLabel",
        "QPushButton": "HButton",
        "QGroupBox": "HGroupBox",
        "QLineEdit": "HLineEdit",
        "QPlainTextEdit": "HPlainTextEdit",
        "QDoubleSpinBox": "HDoubleSpinBox",
        "QSpinBox": "HSpinBox",
        "QScrollBar": "HScrollBar",
        "QFrame": "HFrame",
    }

    WIDGET_NAME_MAP = {
        "h_title": "HTitle",
        "h_subtitle": "HSubtitle",
        "h_comment": "HComment",
        "h_description": "HDescription",
        "h_divider": "HDivider",
        "h_switch": "HSwitch",

        "h_vertical_divider": "HVerticalDivider",
        "h_horizontal_divider": "HHorizontalDivider",

        "h_progress_bar": "HProgressBar",
        "h_progress_bar_m3": "HProgressBarM3",

        "h_indeterminate_progress": "HIndeterminateProgress",
        "h_indeterminate_circular_progress": "HIndeterminateCircularProgress",
        "h_radial_progress": "HRadialProgress",

        "h_strong_button": "HStrongButton",
        "h_strong_grey_button": "HStrongGreyButton",

        "h_toggle_button": "HToggleButton",
        "h_toggle_grey_button": "HToggleGreyButton",

        "h_button_group": "HButtonGroup",
        "h_grey_button_group": "HGreyButtonGroup",
    }


    # Clean imports
    if False:
        qt_import_re = re.compile(r"(from PySide6\.QtWidgets import \((.*?)\))", re.DOTALL)
        def _clean_qt_imports(match):
            widgets = [w.strip() for w in match.group(2).split(",")]
            filtered = [w for w in widgets if w and w not in WIDGET_MAP]
            return f"from PySide6.QtWidgets import ({', '.join(filtered)})"
        text = qt_import_re.sub(_clean_qt_imports, text)

    # Add imports
    hwidgets_to_import = sorted(WIDGET_MAP.values())
    hwidgets_to_import.extend(sorted(WIDGET_NAME_MAP.values()))
    hwidgets_to_import.append("Theme")

    grouped_import = "from typing import Type\n"
    grouped_import += "from hwidgets import (\n" + "".join(
        [f"    {cls},\n" for cls in hwidgets_to_import]
    ) + ")\n"


    # Insert import block right before the first `class` declaration
    text = re.sub(
        r"(\nclass\s+\w+\s*\(object\):)",
        "\n" + grouped_import + r"\1",
        text,
        count=1,
    )

    # Add hstyle argument to the main class
    text = re.sub(
        r"def setupUi\(self,\s*(\w+)\):",
        r"def setupUi(self, \1, theme: Type[Theme]):",
        text,
    )

    # Replace by widget name
    for widget_name, h_widget in WIDGET_NAME_MAP.items():
        pattern = rf"(\s*self\.{widget_name}\w*\s*=\s*)(?!q)\w*\((.*?)\)"
        replacement = rf"\1{h_widget}(\2, theme=theme)"
        text = re.sub(pattern, replacement, text)

    # Replace by class name
    for q_widget, h_widget in WIDGET_MAP.items():
        pattern = rf"(\s*self\.(?!q)\w*\s*=\s*){q_widget}\((.*?)\)"
        replacement = rf"\1{h_widget}(\2, theme=theme)"
        text = re.sub(pattern, replacement, text)

    Path(ui_path).write_text(text, encoding="utf-8")
    print("✅ Replaced QWidgets by HWidgets")
