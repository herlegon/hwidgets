from __future__ import annotations
import sys
import os

plugins_path = os.path.join(os.path.dirname(__file__))
sys.path.append(plugins_path)
sys.path.append(r"A:\hwidgets")
sys.path.append(r"A:\hwidgets\qtdesigner")
os.environ["PYSIDE_DESIGNER_PLUGINS"] = plugins_path
from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection

# print(f"Plugin path: {plugins_path}")

# from .hlineedit_plugin import HLineEditPlugin
from hlabel_plugin import HLabelPlugin


QPyDesignerCustomWidgetCollection.addCustomWidget(HLabelPlugin())

# python -m venv venv
#.\venv\Scripts\activate
# $env:PYSIDE_DESIGNER_PLUGINS = "A:\hwidgets\qtdesigner"
# if __name__ == '__main__':
# QPyDesignerCustomWidgetCollection.addCustomWidget(HLineEditPlugin())
    # try:
    #     # Register the plugin class
    #     plugin_instance = HLineEditPlugin()  # Instantiate the plugin
    #     QPyDesignerCustomWidgetCollection.addCustomWidget(plugin_instance)
    #     # print("Custom widget registered successfully.")
    # except Exception as e:
    #     print(f"Failed to register custom widget: {e}")

# Create an instance of QPyDesignerCustomWidgetCollection to list custom widgets
# collection = QPyDesignerCustomWidgetCollection()

# # List all registered custom widgets (this is for debugging)
# print("Registered custom widgets:")
# for widget in collection.customWidgets():
#     print(f" - {widget.name()}")


# QPyDesignerCustomWidgetCollection.addCustomWidget(HButtonGroupPlugin())

# from checkbox_plugin import HCheckBoxPlugin
# QPyDesignerCustomWidgetCollection.addCustomWidget(HCheckBoxPlugin())

# from divider_plugin import HDividerPlugin
# QPyDesignerCustomWidgetCollection.addCustomWidget(HDividerPlugin())

# from double_spinbox_plugin import HDoubleSpinBoxPlugin
# QPyDesignerCustomWidgetCollection.addCustomWidget(HDoubleSpinBoxPlugin())

# from horizontal_divider_plugin import HHorizontalDividerPlugin
# QPyDesignerCustomWidgetCollection.addCustomWidget(HHorizontalDividerPlugin())

# from vertical_divider_plugin import HVerticalDividerPlugin
# QPyDesignerCustomWidgetCollection.addCustomWidget(HVerticalDividerPlugin())

# from indet_progress_plugin import HIndetProgressPlugin
# QPyDesignerCustomWidgetCollection.addCustomWidget(HIndetProgressPlugin())

# from label_plugin import HLabelPlugin
# QPyDesignerCustomWidgetCollection.addCustomWidget(HLabelPlugin())


# from plain_text_edit_plugin import HPlainTextEditPlugin
# QPyDesignerCustomWidgetCollection.addCustomWidget(HPlainTextEditPlugin())

# from progress_plugin import HProgressPlugin
# QPyDesignerCustomWidgetCollection.addCustomWidget(HProgressPlugin())

# from radial_progress_plugin import HRadialProgressPlugin
# QPyDesignerCustomWidgetCollection.addCustomWidget(HRadialProgressPlugin())

# from radio_button_plugin import HRadioButtonPlugin
# QPyDesignerCustomWidgetCollection.addCustomWidget(HRadioButtonPlugin())

# from scrollbar_plugin import HScrollBarPlugin
# QPyDesignerCustomWidgetCollection.addCustomWidget(HScrollBarPlugin())

# from spinbox_plugin import HSpinBoxPlugin
# QPyDesignerCustomWidgetCollection.addCustomWidget(HSpinBoxPlugin())

# from switch_plugin import HSwitchPlugin
# QPyDesignerCustomWidgetCollection.addCustomWidget(HSwitchPlugin())

# from title_plugin import HTitlePlugin
# QPyDesignerCustomWidgetCollection.addCustomWidget(HTitlePlugin())
