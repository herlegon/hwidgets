from __future__ import annotations

from hwidgets import HDivider, StyleManager

from PySide6.QtDesigner import QDesignerCustomWidgetInterface
from PySide6.QtGui import QIcon

DOM_XML = """
<ui language='c++'>
    <widget class='HDivider' name='h_divider'>
    </widget>
</ui>
"""


class HDividerPlugin(QDesignerCustomWidgetInterface):
    def __init__(self):
        super().__init__()
        self._form_editor = None

    def createWidget(self, parent):
        from hwidgets import StyleManager, HDivider
        t = HDivider(parent, theme=StyleManager().get_theme())
        return t

    def domXml(self):
        return DOM_XML

    def group(self):
        return 'Hwidgets'

    def icon(self):
        return QIcon()

    def includeFile(self):
        return 'hwidgets'

    def initialize(self, form_editor):
        self._form_editor = form_editor

    def isContainer(self):
        return False

    def isInitialized(self):
        return self._form_editor is not None

    def name(self):
        return 'HDivider'

    def toolTip(self):
        return 'HDivider widget'

    def whatsThis(self):
        return self.toolTip()
