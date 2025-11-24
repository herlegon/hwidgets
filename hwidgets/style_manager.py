from pprint import pprint
import tomllib
from pathlib import Path
from dataclasses import replace

from .styles import (
    ButtonStyle,
    CheckBoxStyle,
    DescriptionStyle,
    CommentStyle,
    FontConfig,
    GroupBoxStyle,
    Theme,
    LabelStyle,
    RadioButtonStyle,
    SubtitleStyle,
    TitleStyle,
    IconButtonStyle,
    SwitchStyle,
)

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
        if "common" in config:
            common_cfg = config["common"]

            # Font parsing
            font = theme.common.font
            if "font_family" in common_cfg or "font_size" in common_cfg or "font_weight" in common_cfg:
                font = FontConfig(
                    family=common_cfg.get("font_family", font.family),
                    size=common_cfg.get("font_size", font.size),
                    weight=common_cfg.get("font_weight", font.weight),
                )

            theme.common = replace(theme.common, **{
                "bgd":                  common_cfg.get("bgd", theme.common.bgd),
                "hover":                common_cfg.get("hover", theme.common.hover),
                "selection":            common_cfg.get("selection", theme.common.selection),
                "pressed":              common_cfg.get("pressed", theme.common.pressed),
                "disabled":             common_cfg.get("disabled_bgd", theme.common.disabled),
                "border":               common_cfg.get("border", theme.common.border),
                "font_color":           common_cfg.get("font_color", theme.common.font_color),
                "font_color_disabled":  common_cfg.get("font_color_disabled", theme.common.font_color_disabled),
                "font_color_checked":   common_cfg.get("font_color_checked", theme.common.font_color_checked),
                "font":                 font,
            })



        # Divider color
        if "divider" in config and "normal" in config["divider"]:
            theme.common.divider = config["divider"]["normal"]

        # ------------------------------
        # Inheritance rules
        # ------------------------------
        inheritance = {
            "title": "label",
            "subtitle": "label",
            "comment": "label",
            "description": "label",
        }

        # ------------------------------
        # Map TOML key → InstallStyle attribute
        # ------------------------------
        widget_map = {
            "button": ("button", ButtonStyle),
            "radio": ("radio_button", RadioButtonStyle),
            "checkbox": ("checkbox", CheckBoxStyle),
            "switch": ("switch", SwitchStyle),
            "label": ("label", LabelStyle),
            "title": ("title", TitleStyle),
            "subtitle": ("subtitle", SubtitleStyle),
            "description": ("description", DescriptionStyle),
            "comment": ("comment", CommentStyle),
            "group_box": ("groupbox", GroupBoxStyle),
            "icon_button": ("icon_button", IconButtonStyle),
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
            font_args = {}
            if hasattr(widget, "font"):
                if "font_family" in widget_cfg or "font_size" in widget_cfg or "font_weight" in widget_cfg:
                    font = widget.font
                    font = FontConfig(
                        family = widget_cfg.pop("font_family", font.family),
                        size   = widget_cfg.pop("font_size",  font.size),
                        weight = widget_cfg.pop("font_weight", font.weight),
                    )
                    font_args = {"font": font}
                else:
                    # Keep existing font (redundant for replace but safe)
                    pass
            else:
                # Remove font keys if present to avoid error in replace
                widget_cfg.pop("font_family", None)
                widget_cfg.pop("font_size", None)
                widget_cfg.pop("font_weight", None)

            # Fill missing colors from common
            for field in ("font_color", "font_color_disabled"):
                if field not in widget_cfg and hasattr(widget, field):
                    widget_cfg[field] = getattr(theme.common, field)

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


