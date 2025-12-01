from dataclasses import replace, fields
from pathlib import Path
import tomllib
from PySide6.QtGui import QFont
from .styles import (
    Theme,
    FontConfig,
    weight_from_css,
    DefaultStyle,

    FrameStyle,
    CardStyle,
    DividerStyle,
    ScrollBarStyle,

    AppTitleStyle,
    TitleStyle,
    SubtitleStyle,
    DescriptionStyle,
    CommentStyle,
    LabelStyle,

    CheckBoxStyle,
    RadioButtonStyle,
    SwitchStyle,

    LineEditStyle,
    PlainTextEditStyle,
    LogViewerStyle,
    ComboBoxStyle,
    SpinBoxStyle,
    SliderStyle,

    StrongButtonStyle,
    StrongGreyButtonStyle,
    OutlinedButtonStyle,
    FramelessButtonStyle,
    ToggleButtonStyle,
    ToggleGreyButtonStyle,
    ButtonGroupStyle,
    GreyButtonGroupStyle,

    ProgressBarStyle,
    StepIndicatorStyle,

    IndetProgressBarStyle,

    GroupBoxStyle,
)


def hex_to_rgba(hex_str: str, alpha: float = 1.0) -> str:
    # Do not use rn because the colors are also used for QColor
    # find a way to use it only for stylesheets
    """
    Convert hex color string to 'rgba(r,g,b,a)' for Qt stylesheet.

    Args:
        hex_str (str): Hex color string, e.g. "#2196F3" or "2196F3"
        alpha (float): Opacity between 0.0 and 1.0

    Returns:
        str: CSS rgba string, e.g. "rgba(33,150,243,0.2)"
    """
    # Remove leading '#'
    if not hex_str.startswith('#'):
        return hex_str

    hex_str = hex_str.lstrip('#')

    if len(hex_str) != 6:
        raise ValueError("Hex string must be 6 characters long (RRGGBB)")

    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)

    return f"rgba({r},{g},{b},{alpha})"


class StyleManager:
    SCHEMES_DIR = Path(__file__).parent / "schemes"

    @staticmethod
    def get_theme(scheme: str = "default") -> Theme:
        scheme_path = StyleManager.SCHEMES_DIR / f"{scheme}.toml"
        if not scheme_path.exists():
            raise ValueError(
                f"Scheme '{scheme}' not found. Available: {StyleManager.list_schemes()}"
            )

        with open(scheme_path, "rb") as f:
            config = tomllib.load(f)

        return StyleManager._build_style(config)


    @staticmethod
    def _build_style(config: dict) -> Theme:
        theme = Theme()

        # Window background
        if "window" in config and "window" in config["window"]:
            theme.window_bgd = config["window"]["window"]

        # Common widget colors
        if "default" in config:
            default_style = config["default"]

            # Font parsing
            font = theme.default.font
            if (
                "font_family" in default_style
                or "font_size" in default_style
                or "font_weight" in default_style
            ):
                font = FontConfig(
                    family=default_style.get("font_family", font.family),
                    size=default_style.get("font_size", font.size),
                    weight=weight_from_css(default_style.get("font_weight", font.weight)),
                )

            theme.default = replace(theme.default, **{
                "bgd":                  default_style.get("bgd", theme.default.bgd),
                "hover":                default_style.get("hover", theme.default.hover),
                "selection":            default_style.get("selection", theme.default.selection),
                "pressed":              default_style.get("pressed", theme.default.pressed),
                "disabled":             default_style.get("disabled_bgd", theme.default.disabled),
                "border":               default_style.get("border", theme.default.border),
                "font_color":           default_style.get("font_color", theme.default.font_color),
                "font_color_disabled":  default_style.get("font_color_disabled", theme.default.font_color_disabled),
                "font_color_checked":   default_style.get("font_color_checked", theme.default.font_color_checked),
                "font":                 font,
            })

        # ------------------------------
        # Inheritance rules
        # ------------------------------
        inheritance = {
            "card": "frame",

            "app_title": "label",
            "title": "label",
            "subtitle": "label",
            "comment": "label",
            "description": "label",

            "checkbox": "label",
            "radio_button": "label",

            "line_edit": "label",
            "plain_text_edit": "line_edit",
            "log_viewer": "plain_text_edit",

            "combobox": "line_edit",
            "spinbox": "line_edit",

            "strong_grey_button": "strong_button",
            "grey_button_group": "button_group",

            "toggle_button": "strong_button",
            "toggle_grey_button": "toggle_button",

            "step_indicator": "label",
        }

        # ------------------------------
        # Map TOML key → InstallStyle attribute
        # ------------------------------
        widget_map = {
            "frame": ("frame", FrameStyle),
            "card": ("card", CardStyle),
            "divider": ("divider", DividerStyle),
            "scrollbar": ("scrollbar", ScrollBarStyle),

            "label": ("label", LabelStyle),
            "app_title": ("app_title", AppTitleStyle),
            "title": ("title", TitleStyle),
            "subtitle": ("subtitle", SubtitleStyle),
            "description": ("description", DescriptionStyle),
            "comment": ("comment", CommentStyle),

            "switch": ("switch", SwitchStyle),
            "checkbox": ("checkbox", CheckBoxStyle),
            "radio_button": ("radio_button", RadioButtonStyle),

            "line_edit": ("line_edit", LineEditStyle),
            "plain_text_edit": ("plain_text_edit", PlainTextEditStyle),
            "log_viewer": ("log_viewer", LogViewerStyle),

            "combobox": ("combobox", ComboBoxStyle),
            "spinbox": ("spinbox", SpinBoxStyle),
            # "double_spinbox": ("double_spinbox", DoubleSpinBoxStyle),
            "slider": ("slider", SliderStyle),

            "strong_button": ("strong_button", StrongButtonStyle),
            "strong_grey_button": ("strong_grey_button", StrongGreyButtonStyle),
            "outlined_button": ("outlined_button", OutlinedButtonStyle),

            "toggle_button": ("toggle_button", ToggleButtonStyle),
            "toggle_grey_button": ("toggle_grey_button", ToggleGreyButtonStyle),

            "frameless_button": ("frameless_button", FramelessButtonStyle),

            "button_group": ("button_group", ButtonGroupStyle),
            "grey_button_group": ("grey_button_group", GreyButtonGroupStyle),

            "progress_bar": ("progress_bar", ProgressBarStyle),
            "step_indicator": ("step_indicator", StepIndicatorStyle),
            "indet_progress_bar": ("indet_progress_bar", IndetProgressBarStyle),

            "group_box": ("groupbox", GroupBoxStyle),
        }

        # ------------------------------
        # Apply each widget block
        # ------------------------------
        for key, (attr, cls) in widget_map.items():
            if key not in config:
                continue

            widget_cfg = config[key].copy()

            # Apply inheritance
            if key in inheritance:
                parent_cfg = config.get(inheritance[key], {}).copy()
                parent_cfg.update(widget_cfg)
                widget_cfg = parent_cfg

            widget = getattr(theme, attr)

            # Font override
            # not working
            font_args = {}
            for variant in ('_upcoming', '_completed', '_current', ''):
                if hasattr(widget, "font"):
                    if (
                        f"font{variant}_family" in widget_cfg
                        or f"font{variant}_size" in widget_cfg
                        or f"font{variant}_weight" in widget_cfg
                    ):
                        font = widget.font
                        font = FontConfig(
                            family = widget_cfg.pop(f"font{variant}_family", font.family),
                            size   = widget_cfg.pop(f"font{variant}_size",  font.size),
                            weight = weight_from_css(widget_cfg.pop(f"font{variant}_weight", font.weight)),
                        )
                        font_args[f"font{variant}"] = font
                    else:
                        # Keep existing font (redundant for replace but safe)
                        pass

                else:
                    # Remove font keys if present to avoid error in replace
                    widget_cfg.pop(f"font{variant}_family", None)
                    widget_cfg.pop(f"font{variant}_size", None)
                    widget_cfg.pop(f"font{variant}_weight", None)


            # Fill missing colors from common
            common_fields = [f.name for f in fields(DefaultStyle)]

            for field in common_fields:
                if field not in widget_cfg and hasattr(widget, field):
                    # Only override if the default value is empty
                    if getattr(widget, field) == "":
                        widget_cfg[field] = getattr(theme.default, field)

            # Remove keys that are not in the dataclass fields to avoid TypeError in replace
            # (Optional but good practice if toml has extra keys)
            # For now, assuming toml is correct or replace will raise TypeError which is fine.
            setattr(theme, attr, replace(widget, **widget_cfg, **font_args))

        return theme


    @staticmethod
    def list_schemes() -> list[str]:
        if not StyleManager.SCHEMES_DIR.exists():
            return []
        return [f.stem for f in StyleManager.SCHEMES_DIR.glob("*.toml")]


