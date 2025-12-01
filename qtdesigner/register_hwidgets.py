from __future__ import annotations
import os
from pathlib import Path
import sys

if sys.platform == 'linux':
    plugins_path = str(Path("/home/adg/github/hwidgets/qtdesigner"))

else:
    plugins_path = os.path.join(os.path.dirname(__file__))

sys.path.append(plugins_path)
os.environ["PYSIDE_DESIGNER_PLUGINS"] = plugins_path

from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection

from checkbox_plugin import HCheckBoxPlugin
from divider_plugin import HDividerPlugin
from double_spinbox_plugin import HDoubleSpinBoxPlugin
from hlabel_plugin import HLabelPlugin
from hlineedit_plugin import HLineEditPlugin
from hindentprogressbarm2_plugin import HIndetProgressBarM2Plugin
from plaintextedit_plugin import HPlainTextEditPlugin
from radialprogress_plugin import HRadialProgressPlugin
from radiobutton_plugin import HRadioButtonPlugin
# from scrollbar_plugin import HScrollBarPlugin
from spinbox_plugin import HSpinBoxPlugin
from switch_plugin import HSwitchPlugin
from title_plugin import HTitlePlugin


if __name__ == '__main__':
    # python -m venv venv
    #.\venv\Scripts\activate
    # $env:PYSIDE_DESIGNER_PLUGINS = "A:\hwidgets\qtdesigner"

    QPyDesignerCustomWidgetCollection.addCustomWidget(HCheckBoxPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(HDividerPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(HDoubleSpinBoxPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(HLabelPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(HLineEditPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(HIndetProgressBarM2Plugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(HPlainTextEditPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(HRadialProgressPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(HRadioButtonPlugin())
    # QPyDesignerCustomWidgetCollection.addCustomWidget(HScrollBarPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(HSpinBoxPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(HSwitchPlugin())
    QPyDesignerCustomWidgetCollection.addCustomWidget(HTitlePlugin())


