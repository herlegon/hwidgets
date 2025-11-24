from dataclasses import dataclass, field
from typing import NamedTuple


BORDER_RADIUS: int = 6
NORMAL_HEIGHT: int = 24


class FontConfig(NamedTuple):
    family: str = "Segoe UI"
    size: int = 10
    weight: int = 400



@dataclass
class WidgetCommonColors:
    height: int = NORMAL_HEIGHT
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
    font: FontConfig = FontConfig(size=14, weight=600)
    font_color: str = ""
    font_color_checked: str = ""
    font_color_disabled: str = ""



@dataclass
class GroupBoxStyle:
    height: int = BORDER_RADIUS * 2 + NORMAL_HEIGHT
    title_padding: int = BORDER_RADIUS + 4
    title_height: int = 10

    bgd: str = ""
    hover: str = ""
    selection: str = ""
    pressed: str = ""
    disabled_bgd: str = ""
    border: str = ""



@dataclass
class FrameStyle:
    bgd: str = ""
    hover: str = ""
    selection: str = ""
    pressed: str = ""
    disabled_bgd: str = ""
    border: str = ""
    font: FontConfig = FontConfig(size=14, weight=600)
    font_color: str = ""
    font_color_disabled: str = ""



@dataclass
class DividerStyle:
    normal: str = ""
    disabled: str = ""
    thickness: int = 1
    min_length: int = 40
    padding: int = 16



@dataclass
class ScrollBarStyle:
    track_width: int = 8



@dataclass
class ButtonStyle:
    height: int = NORMAL_HEIGHT

    normal: str = ""
    hover: str = ""
    pressed: str = ""
    checked: str = ""
    disabled: str = ""

    font: FontConfig = FontConfig(weight=500)
    font_color: str = ""
    font_color_disabled: str = ""


@dataclass
class IconButtonStyle:
    height: int = NORMAL_HEIGHT

    normal: str = ""
    hover: str = ""
    pressed: str = ""
    disabled: str = ""




@dataclass
class RadioButtonStyle:
    size: int = 14
    radius: int = BORDER_RADIUS - 1
    border_thickness: int = 2

    normal: str = ""
    disabled: str = ""
    checked: str = ""
    checked_text: str = ""



@dataclass
class ButtonGroupStyle(ButtonStyle):
    size: int = 14
    radius: int = BORDER_RADIUS - 1
    border_width: int = 2

    normal: str = ""
    hover: str = ""
    disabled: str = ""

    font_color_checked: str = ""
    font_color_disabled: str = ""



@dataclass
class CheckBoxStyle:
    size: int = 16
    box_size: int = 14
    box_thickness: int = 2

    pressed: str = ""
    border: str = ""
    normal: str = ""
    hover: str = ""
    disabled: str = ""
    checked: str = ""
    checked_text: str = ""


@dataclass
class SwitchStyle:
    track_height: int = NORMAL_HEIGHT
    track_width: int = 40
    handle_radius: int = 16

    normal: str = ""
    hover: str = ""
    pressed: str = ""
    checked: str = ""
    disabled: str = ""
    handle_disabled: str = ""
    unchecked: str = ""


@dataclass
class ComboBoxStyle:
    normal: str = ""
    hover: str = ""
    selection: str = ""
    pressed: str = ""
    disabled: str = ""

    font: FontConfig = FontConfig(weight=500)
    font_color: str = ""
    font_color_disabled: str = ""
    font_color_selected: str = ""



@dataclass
class LineEditStyle:
    normal: str = ""
    hover: str = ""
    pressed: str = ""
    selected: str = ""
    disabled: str = ""

    font: FontConfig = FontConfig(weight=500)
    font_color: str = ""
    font_color_selection: str = ""
    font_color_disabled: str = ""



@dataclass
class PlainTextEditStyle(LineEditStyle):
    ...



@dataclass
class SpinBoxStyle:
    radius: int = NORMAL_HEIGHT
    padding: int = 12
    min_width: int = (NORMAL_HEIGHT + BORDER_RADIUS) * 2

    normal: str = ""
    hover: str = ""
    pressed: str = ""
    selected: str = ""
    disabled: str = ""

    font: FontConfig = FontConfig(weight=500)
    font_color: str = ""
    font_color_selection: str = ""
    font_color_disabled: str = ""



@dataclass
class LabelStyle:
    padding = BORDER_RADIUS

    font: FontConfig = FontConfig()
    font_color: str = ""
    font_color_disabled: str = ""



@dataclass
class TitleStyle:
    height: int = NORMAL_HEIGHT + BORDER_RADIUS
    padding = 0

    font: FontConfig = FontConfig(size=16, weight=800)
    font_color: str = ""
    font_color_disabled: str = ""



@dataclass
class SubtitleStyle:
    font: FontConfig = FontConfig(size=12, weight=400)
    font_color: str = ""
    font_color_disabled: str = ""


@dataclass
class DescriptionStyle:
    font: FontConfig = FontConfig(size=12, weight=400)
    font_color: str = ""
    font_color_disabled: str = ""



@dataclass
class CommentStyle:
    font: FontConfig = FontConfig(size=10, weight=400)
    font_color: str = ""
    font_color_disabled: str = ""



PROGRESS_TRACK_THICKNESS: int = 12
@dataclass
class ProgressStyle:
    thickness: int = PROGRESS_TRACK_THICKNESS

    track: str = ""
    bar: str = ""



# @dataclass
# class IndeterminateProgressStyle(ProgressStyle):
#     ...


# @dataclass
# class RadialProgressStyle(ProgressStyle):
#     ...



@dataclass
class Theme:
    window_bgd: str = "#303034"
    common: WidgetCommonColors = field(default_factory=WidgetCommonColors)

    groupbox: GroupBoxStyle = field(default_factory=GroupBoxStyle)
    frame: FrameStyle = field(default_factory=FrameStyle)

    divider: DividerStyle = field(default_factory=DividerStyle)
    # horizontal_divider: DividerStyle = field(default_factory=DividerStyle)
    # vertical_divider: DividerStyle = field(default_factory=DividerStyle)

    label: LabelStyle = field(default_factory=LabelStyle)
    title: TitleStyle = field(default_factory=TitleStyle)
    subtitle: SubtitleStyle = field(default_factory=SubtitleStyle)
    description: DescriptionStyle = field(default_factory=DescriptionStyle)
    comment: CommentStyle = field(default_factory=CommentStyle)


    scrollbar: ScrollBarStyle = field(default_factory=ScrollBarStyle)

    button: ButtonStyle = field(default_factory=ButtonStyle)
    icon_button: IconButtonStyle = field(default_factory=IconButtonStyle)
    switch: SwitchStyle = field(default_factory=SwitchStyle)
    radio_button: RadioButtonStyle = field(default_factory=RadioButtonStyle)
    button_group: ButtonGroupStyle = field(default_factory=ButtonGroupStyle)

    checkbox: CheckBoxStyle = field(default_factory=CheckBoxStyle)
    combobox: ComboBoxStyle = field(default_factory=ComboBoxStyle)

    line_edit: LineEditStyle = field(default_factory=LineEditStyle)
    plain_text_edit: PlainTextEditStyle = field(default_factory=PlainTextEditStyle)

    spinbox: SpinBoxStyle = field(default_factory=SpinBoxStyle)
    # double_spinbox: DoubleSpinBoxStyle = field(default_factory=DoubleSpinBoxStyle)



    progress: ProgressStyle = field(default_factory=ProgressStyle)
    # indeterminate_progress: IndeterminateProgressStyle = field(default_factory=IndeterminateProgressStyle)
    # radial_progress: RadialProgressStyle = field(default_factory=RadialProgressStyle)



