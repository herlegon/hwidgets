from pprint import pprint
import tomllib
from pathlib import Path
from dataclasses import replace

from .styles import (
    ButtonStyle,
    CheckBoxStyle,
    CommentStyle,
    FontConfig,
    GroupBoxStyle,
    Theme,
    LabelStyle,
    RadioButtonStyle,
    SubtitleStyle,
    TitleStyle,
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
        if "widget" in config:
            theme.common = replace(theme.common, **{
                "background":   config["widget"].get("bgd", theme.common.bgd),
                "hover":        config["widget"].get("hover", theme.common.hover),
                "selection":    config["widget"].get("selection", theme.common.selection),
                "pressed":      config["widget"].get("pressed", theme.common.pressed),
                "disabled_bgd": config["widget"].get("disabled_bgd", theme.common.disabled_bgd),
                "border":       config["widget"].get("border", theme.common.border),
                "font_color":   config["widget"].get("font_color", theme.common.font_color),
                "font_color_disabled": config["widget"].get("font_color_disabled", theme.common.font_color_disabled),
            })

        # Checkbox/Radio special fields
        if "checkbox" in config:
            theme.common.checked = config["checkbox"].get("checked", theme.common.checked)
        if "radio" in config:
            theme.common.checked = config["radio"].get("checked", theme.common.checked)

        # Divider color
        if "divider" in config and "normal" in config["divider"]:
            theme.common.divider = config["divider"]["normal"]

        # ------------------------------
        # Inheritance rules
        # ------------------------------
        inheritance = {
            "subtitle": "label",
            "comment": "label",
        }

        # ------------------------------
        # Map TOML key → InstallStyle attribute
        # ------------------------------
        widget_map = {
            "button": ("hbutton", ButtonStyle),
            "radio": ("hradiobutton", RadioButtonStyle),
            "checkbox": ("hcheckbox", CheckBoxStyle),
            "label": ("hlabel", LabelStyle),
            "title": ("htitle", TitleStyle),
            "subtitle": ("hsubtitle", SubtitleStyle),
            "comment": ("hcomment", CommentStyle),
            "group_box": ("hgroupbox", GroupBoxStyle),
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

            # Font override
            if "font_family" in widget_cfg or "font_size" in widget_cfg or "font_weight" in widget_cfg:
                font = getattr(theme, attr).font
                font = FontConfig(
                    family = widget_cfg.pop("font_family", font.family),
                    size   = widget_cfg.pop("font_size",  font.size),
                    weight = widget_cfg.pop("font_weight", font.weight),
                )
            else:
                font = getattr(theme, attr).font

            # Fill missing colors from common
            for field in ("font_color", "font_color_disabled"):
                if field not in widget_cfg:
                    widget_cfg[field] = getattr(theme.common, field)

            widget = getattr(theme, attr)
            setattr(theme, attr, replace(widget, **widget_cfg, font=font))

        return theme


    @staticmethod
    def list_schemes() -> list[str]:
        if not StyleManager.SCHEMES_DIR.exists():
            return []
        return [f.stem for f in StyleManager.SCHEMES_DIR.glob("*.toml")]


