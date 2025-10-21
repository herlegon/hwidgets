from dataclasses import dataclass


TOOLBAR_HEIGHT: int = 32




@dataclass
class TitleBarColors:
    """RGB colors used for the title bar"""
    background: str
    background_inactive: str
    button_hover: str
    close_button_hover: str
    button_color: str
    title_color: str
    title_color_inactive: str
    separation: str | None = None
