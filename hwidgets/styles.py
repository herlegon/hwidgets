from dataclasses import dataclass, field
from typing import NamedTuple


BORDER_RADIUS: int = 6
NORMAL_HEIGHT: int = 24


class FontConfig(NamedTuple):
    family: str = "Segoe UI"
    size: int = 10
    weight: int = 400



@dataclass
class DefaultStyle:
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
class FrameStyle:
    bgd: str = ""
    radius: int = BORDER_RADIUS * 1.5


@dataclass
class CardStyle(FrameStyle):
    # bgd: str = ""
    border: str = ""


@dataclass
class DividerStyle:
    normal: str = ""
    disabled: str = ""
    thickness: int = 1
    min_length: int = 40
    padding: int = 16


@dataclass
class LabelStyle:
    padding = 0

    font: FontConfig = FontConfig()
    font_color: str = ""
    font_color_disabled: str = ""


@dataclass
class TitleStyle(LabelStyle):
    height: int = NORMAL_HEIGHT + BORDER_RADIUS
    font: FontConfig = FontConfig(size=16, weight=800)


@dataclass
class SubtitleStyle(LabelStyle):
    font: FontConfig = FontConfig(size=12, weight=400)


@dataclass
class DescriptionStyle(LabelStyle):
    font: FontConfig = FontConfig(size=12, weight=400)


@dataclass
class CommentStyle(LabelStyle):
    font: FontConfig = FontConfig(size=10, weight=400)


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
class ScrollBarStyle:
    thickness: int = 8
    normal: str = ""
    hover: str = ""



@dataclass
class SpinBoxStyle:
    radius: int = NORMAL_HEIGHT
    padding: int = 12
    min_width: int = (NORMAL_HEIGHT + BORDER_RADIUS) * 2

    normal: str = ""
    hover: str = ""
    pressed: str = ""
    disabled: str = ""

    selection: str = ""
    button_color: str = ""
    button_hover: str = ""
    button_pressed: str = ""
    button_disabled: str = ""


    font: FontConfig = FontConfig(weight=500)
    font_color: str = ""
    font_color_selection: str = ""
    font_color_disabled: str = ""



@dataclass
class ComboBoxStyle:
    normal: str = ""
    hover: str = ""
    selection: str = ""
    disabled: str = ""
    # button_hover: str = ""
    # button_disabled: str = ""

    font: FontConfig = FontConfig(weight=500)
    font_color: str = ""
    font_color_disabled: str = ""



@dataclass
class ButtonGroupStyle:
    height: int = NORMAL_HEIGHT

    normal: str = ""
    hover: str = ""
    pressed: str = ""
    checked: str = ""
    disabled: str = ""

    font: FontConfig = FontConfig(weight=500)
    font_color: str = ""
    font_color_checked: str = ""
    font_color_disabled: str = ""


@dataclass
class StrongButtonStyle:
    height: int = 32

    bgd: str = ""

    normal: str = ""
    hover: str = ""
    pressed: str = ""
    checked: str = ""
    disabled: str = ""

    font: FontConfig = FontConfig(weight=600)
    font_color: str = ""
    font_color_checked: str = ""
    font_color_disabled: str = ""



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
    font_color_checked: str = ""
    font_color_disabled: str = ""


@dataclass
class FlatButtonStyle:
    normal: str = ""
    hover: str = ""
    pressed: str = ""
    checked: str = ""
    disabled: str = ""


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
class IconButtonStyle:
    height: int = NORMAL_HEIGHT

    normal: str = ""
    hover: str = ""
    pressed: str = ""
    disabled: str = ""

    border: str = ""









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
    default: DefaultStyle = field(default_factory=DefaultStyle)

    groupbox: GroupBoxStyle = field(default_factory=GroupBoxStyle)
    frame: FrameStyle = field(default_factory=FrameStyle)
    card: CardStyle = field(default_factory=CardStyle)
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
    strong_button: StrongButtonStyle = field(default_factory=StrongButtonStyle)


    switch: SwitchStyle = field(default_factory=SwitchStyle)
    radio_button: RadioButtonStyle = field(default_factory=RadioButtonStyle)
    button_group: ButtonGroupStyle = field(default_factory=ButtonGroupStyle)

    checkbox: CheckBoxStyle = field(default_factory=CheckBoxStyle)

    line_edit: LineEditStyle = field(default_factory=LineEditStyle)
    plain_text_edit: PlainTextEditStyle = field(default_factory=PlainTextEditStyle)

    combobox: ComboBoxStyle = field(default_factory=ComboBoxStyle)

    spinbox: SpinBoxStyle = field(default_factory=SpinBoxStyle)
    # double_spinbox: DoubleSpinBoxStyle = field(default_factory=DoubleSpinBoxStyle)

    flat_button: FlatButtonStyle = field(default_factory=FlatButtonStyle)

    progress: ProgressStyle = field(default_factory=ProgressStyle)
    # indeterminate_progress: IndeterminateProgressStyle = field(default_factory=IndeterminateProgressStyle)
    # radial_progress: RadialProgressStyle = field(default_factory=RadialProgressStyle)



