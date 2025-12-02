from dataclasses import dataclass, field
from typing import NamedTuple
from PySide6.QtGui import QFont


BORDER_RADIUS: int = 6
DEFAULT_HEIGHT: int = 24
PROGRESS_TRACK_THICKNESS: int = 12
BUTTON_SIDE_PADDING: int = BORDER_RADIUS + 12

FONT_VARIANTS = ["current", "upcoming", "completed"]

@dataclass
class FontConfig:
    family: str = "Inter"
    size: int = 10
    weight: QFont.Weight = QFont.Weight.Normal
    style: QFont.Style = QFont.Style.StyleNormal

    def make_font(self) -> QFont:
        """
        Create a QFont from this FontConfig.
        Anti-aliasing and hinting are applied.
        """
        font = QFont(self.family, self.size)
        font.setWeight(self.weight)
        font.setStyleStrategy(QFont.StyleStrategy.PreferQuality)
        font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        font.setStyle(self.style)
        return font


def weight_from_css(css_weight: int) -> QFont.Weight:
    return {
        100: QFont.Weight.Thin,
        200: QFont.Weight.ExtraLight,
        300: QFont.Weight.Light,
        400: QFont.Weight.Normal,
        500: QFont.Weight.Medium,
        600: QFont.Weight.DemiBold,
        700: QFont.Weight.Bold,
        800: QFont.Weight.ExtraBold,
        900: QFont.Weight.Black,
    }.get(css_weight, QFont.Weight.Normal)



@dataclass
class DefaultStyle:
    height: int = DEFAULT_HEIGHT
    radius: int = BORDER_RADIUS

    bgd: str = ""
    normal: str = ""
    hover: str = ""
    selection: str = ""
    pressed: str = ""
    disabled: str = ""

    border: str = ""
    border_selected: str = ""

    # Text colors
    font: FontConfig = field(default_factory=FontConfig)
    font_color: str = ""
    font_color_checked: str = ""
    font_color_disabled: str = ""



@dataclass
class FrameStyle:
    radius: int = BORDER_RADIUS * 1.5
    bgd: str = ""
    border: str = ""


@dataclass
class CardStyle(FrameStyle):
    border: str = "red"


@dataclass
class DividerStyle:
    normal: str = ""
    disabled: str = ""
    thickness: int = 1
    min_length: int = 40
    padding: int = 16


@dataclass
class ScrollBarStyle:
    thickness: int = 12
    normal: str = ""
    hover: str = ""
    pressed: str = ""


@dataclass
class LabelStyle:
    padding = 0

    font: FontConfig = field(default_factory=FontConfig)
    font_color: str = ""
    font_color_disabled: str = ""



@dataclass
class AppTitleStyle(LabelStyle):
    font: FontConfig = field(
        default_factory=lambda: FontConfig(size=11, weight=QFont.Weight.Bold)
    )


@dataclass
class TitleStyle(LabelStyle):
    height: int = DEFAULT_HEIGHT + 2 * BORDER_RADIUS
    font: FontConfig = field(
        default_factory=lambda: FontConfig(size=16, weight=QFont.Weight.Bold)
    )


@dataclass
class SubtitleStyle(LabelStyle):
    font: FontConfig = field(
        default_factory=lambda: FontConfig(size=11)
    )


@dataclass
class DescriptionStyle(LabelStyle):
    font: FontConfig = field(
        default_factory=lambda: FontConfig(size=11)
    )


@dataclass
class CommentStyle(LabelStyle):
    font: FontConfig = field(
        default_factory=lambda: FontConfig(size=11)
    )


@dataclass
class SwitchStyle:
    track_height: int = 24
    track_width: int = 40
    handle_radius: int = 18

    track_on: str = ""
    track_off: str = ""

    handle_on: str = ""
    handle_off: str = ""

    track_disabled: str = ""
    handle_disabled: str = ""


@dataclass
class CheckBoxStyle(LabelStyle):
    box_size: int = 14
    box_thickness: int = 2

    border: str = ""
    pressed: str = ""
    checked: str = ""
    disabled: str = ""


@dataclass
class RadioButtonStyle(LabelStyle):
    circle_size: int = 14
    circle_thickness: int = 2

    border: str = ""
    pressed: str = ""
    checked: str = ""
    disabled: str = ""


@dataclass
class LineEditStyle(LabelStyle):
    bgd: str = ""
    hover: str = ""
    disabled: str = ""

    border: str = ""
    border_hover: str = ""
    border_edition: str = ""
    border_read_only: str = ""

    selection: str = ""
    # font_color: str = ""
    font_color_read_only: str = ""
    font_color_disabled: str = ""

    button: str = ""
    button_hover: str = ""
    button_disabled: str = ""


@dataclass
class PlainTextEditStyle(LineEditStyle):
    ...


@dataclass
class LogViewerStyle(PlainTextEditStyle):
    ...


@dataclass
class ComboBoxStyle(LineEditStyle):
    ...


@dataclass
class SpinBoxStyle(LineEditStyle):
    radius: int = DEFAULT_HEIGHT
    padding: int = 12
    min_width: int = (DEFAULT_HEIGHT + BORDER_RADIUS) * 2

    button_pressed: str = ""


@dataclass
class SliderStyle:
    track_thickness: int = 4
    track: str = ""
    track_disabled: str = ""

    handle_radius: int = 12
    handle: str = ""
    handle_hover: str = ""
    handle_pressed: str = ""
    handle_disabled: str = ""

    ticks_thickness: int = 1
    ticks_length: int = 16
    ticks: str = ""


@dataclass
class StrongButtonStyle:
    height: int = 32
    padding: int = BUTTON_SIDE_PADDING

    bgd: str = ""
    hover: str = ""
    pressed: str = ""
    disabled: str = ""

    font: FontConfig = field(
        default_factory=lambda: FontConfig(size=16, weight=QFont.Weight.Bold)
    )
    font_color: str = ""
    font_color_disabled: str = ""


@dataclass
class StrongGreyButtonStyle(StrongButtonStyle):
    ...


@dataclass
class OutlinedButtonStyle:
    height: int = DEFAULT_HEIGHT
    padding: int = BUTTON_SIDE_PADDING

    bgd: str = ""
    hover: str = ""
    pressed: str = ""
    disabled: str = ""

    border: str = ""
    border_disabled: str = ""

    font: FontConfig = field(default_factory=FontConfig)
    font_color: str = ""
    font_color_disabled: str = ""


@dataclass
class ToggleButtonStyle(StrongButtonStyle):
    height: int = DEFAULT_HEIGHT

    checked: str = ""

    border: str = ""

    font: FontConfig = field(default_factory=FontConfig)
    font_color_checked: str = ""


@dataclass
class ToggleGreyButtonStyle(ToggleButtonStyle):
    ...


@dataclass
class FramelessButtonStyle:
    height: int = DEFAULT_HEIGHT

    # use teh same colors for lines and font
    active: str = ""
    hover: str = ""
    pressed: str = ""
    checked: str = ""
    disabled: str = ""

    font: FontConfig = field(default_factory=FontConfig)


@dataclass
class ButtonGroupStyle:
    height: int = DEFAULT_HEIGHT
    padding: int = BUTTON_SIDE_PADDING // 2

    bgd: str = ""
    hover: str = ""
    pressed: str = ""
    checked: str = ""
    disabled: str = ""
    disabled_checked: str = ""

    border: str = ""

    font: FontConfig = field(
        default_factory=lambda: FontConfig(size=11, weight=QFont.Weight.Normal)
    )
    font_color: str = ""
    # font_color_checked: str = ""
    font_color_disabled: str = ""


@dataclass
class GreyButtonGroupStyle(ButtonGroupStyle):
    ...


@dataclass
class ProgressBarStyle:
    thickness: int = PROGRESS_TRACK_THICKNESS
    track: str = ""
    bar: str = ""


@dataclass
class RadialProgressBarStyle:
    font_label: FontConfig = field(
        default_factory=lambda: FontConfig(size=10)
    )
    font_legend: FontConfig = field(
        default_factory=lambda: FontConfig(size=10)
    )


@dataclass
class StepIndicatorStyle(LabelStyle):
    height: int = 32
    spacing: int = BORDER_RADIUS * 2

    font_completed: FontConfig = field(
        default_factory=lambda: FontConfig(size=9, weight=QFont.Weight.Normal)
    )
    font_completed_color: str = ""

    font_current: FontConfig = field(
        default_factory=lambda: FontConfig(size=11, weight=QFont.Weight.Bold)
    )
    font_current_color: str = ""

    font_upcoming: FontConfig = field(
        default_factory=lambda: FontConfig(size=9, weight=QFont.Weight.Normal)
    )
    font_upcoming_color: str = ""


@dataclass
class IndetProgressBarStyle(ProgressBarStyle):
    ...



################################


@dataclass
class GroupBoxStyle:
    height: int = BORDER_RADIUS * 2 + DEFAULT_HEIGHT
    title_padding: int = BORDER_RADIUS + 4
    title_height: int = 10

    bgd: str = ""
    hover: str = ""
    selection: str = ""
    pressed: str = ""
    disabled_bgd: str = ""
    border: str = ""



@dataclass
class Theme:
    window_bgd: str = "black"
    default: DefaultStyle = field(default_factory=DefaultStyle)

    groupbox: GroupBoxStyle = field(default_factory=GroupBoxStyle)
    frame: FrameStyle = field(default_factory=FrameStyle)
    card: CardStyle = field(default_factory=CardStyle)
    divider: DividerStyle = field(default_factory=DividerStyle)
    # horizontal_divider: DividerStyle = field(default_factory=DividerStyle)
    # vertical_divider: DividerStyle = field(default_factory=DividerStyle)
    scrollbar: ScrollBarStyle = field(default_factory=ScrollBarStyle)

    label: LabelStyle = field(default_factory=LabelStyle)
    app_title: AppTitleStyle = field(default_factory=AppTitleStyle)
    title: TitleStyle = field(default_factory=TitleStyle)
    subtitle: SubtitleStyle = field(default_factory=SubtitleStyle)
    description: DescriptionStyle = field(default_factory=DescriptionStyle)
    comment: CommentStyle = field(default_factory=CommentStyle)

    switch: SwitchStyle = field(default_factory=SwitchStyle)
    checkbox: CheckBoxStyle = field(default_factory=CheckBoxStyle)
    radio_button: RadioButtonStyle = field(default_factory=RadioButtonStyle)

    line_edit: LineEditStyle = field(default_factory=LineEditStyle)
    plain_text_edit: PlainTextEditStyle = field(default_factory=PlainTextEditStyle)
    log_viewer: LogViewerStyle = field(default_factory=LogViewerStyle)

    combobox: ComboBoxStyle = field(default_factory=ComboBoxStyle)
    spinbox: SpinBoxStyle = field(default_factory=SpinBoxStyle)
    slider: SliderStyle = field(default_factory=SliderStyle)

    strong_button: StrongButtonStyle = field(default_factory=StrongButtonStyle)
    strong_grey_button: StrongGreyButtonStyle = field(default_factory=StrongGreyButtonStyle)
    outlined_button: OutlinedButtonStyle = field(default_factory=OutlinedButtonStyle)

    toggle_button: ToggleButtonStyle = field(default_factory=ToggleButtonStyle)
    toggle_grey_button: ToggleGreyButtonStyle = field(default_factory=ToggleGreyButtonStyle)

    frameless_button: FramelessButtonStyle = field(default_factory=FramelessButtonStyle)

    button_group: ButtonGroupStyle = field(default_factory=ButtonGroupStyle)
    grey_button_group: GreyButtonGroupStyle = field(default_factory=GreyButtonGroupStyle)

    progress_bar: ProgressBarStyle = field(default_factory=ProgressBarStyle)
    radial_progress_bar: RadialProgressBarStyle = field(default_factory=RadialProgressBarStyle)
    step_indicator: StepIndicatorStyle = field(default_factory=StepIndicatorStyle)

    indet_progress_bar: IndetProgressBarStyle = field(default_factory=IndetProgressBarStyle)

    # radial_progress: RadialProgressStyle = field(default_factory=RadialProgressStyle)

