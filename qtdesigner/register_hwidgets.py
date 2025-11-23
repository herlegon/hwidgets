from __future__ import annotations

from hwidgets import HButtonGroup  # noqa: F401
from buttongroup_plugin import HButtonGroupPlugin

from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection

# Set PYSIDE_DESIGNER_PLUGINS to point to this directory and load the plugin


if __name__ == '__main__':
    QPyDesignerCustomWidgetCollection.addCustomWidget(HButtonGroupPlugin())

    from button_plugin import HButtonPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HButtonPlugin())

    from checkbox_plugin import HCheckBoxPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HCheckBoxPlugin())

    from divider_plugin import HDividerPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HDividerPlugin())

    from doublespinbox_plugin import HDoubleSpinBoxPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HDoubleSpinBoxPlugin())

    from groupbox_plugin import HGroupBoxPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HGroupBoxPlugin())

    from horizontal_divider_plugin import HHorizontalDividerPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HHorizontalDividerPlugin())

    from vertical_divider_plugin import HVerticalDividerPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HVerticalDividerPlugin())

    from indeterminate_progress_plugin import HIndeterminateProgressPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HIndeterminateProgressPlugin())

    from label_plugin import HLabelPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HLabelPlugin())

    from lineedit_plugin import HLineEditPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HLineEditPlugin())

    from plaintextedit_plugin import HPlainTextEditPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HPlainTextEditPlugin())

    from progress_plugin import HProgressPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HProgressPlugin())

    from radial_progress_plugin import HRadialProgressPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HRadialProgressPlugin())

    from radiobutton_plugin import HRadioButtonPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HRadioButtonPlugin())

    from scrollbar_plugin import HScrollBarPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HScrollBarPlugin())

    from spinbox_plugin import HSpinBoxPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HSpinBoxPlugin())

    from switch_plugin import HSwitchPlugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HSwitchPlugin())

    from title1_plugin import HTitle1Plugin
    QPyDesignerCustomWidgetCollection.addCustomWidget(HTitle1Plugin())
