from __future__ import annotations

from hwidgets import HButtonGroup  # noqa: F401
from buttongroup_plugin import HButtonGroupPlugin

from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection

# Set PYSIDE_DESIGNER_PLUGINS to point to this directory and load the plugin


if __name__ == '__main__':
    QPyDesignerCustomWidgetCollection.addCustomWidget(HButtonGroupPlugin())
