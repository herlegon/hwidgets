from __future__ import annotations

from hwidgets import HIndeterminateProgress

from PySide6.QtDesigner import QDesignerCustomWidgetInterface
from PySide6.QtGui import QIcon

DOM_XML = """
<ui language='c++'>
    <widget class='HIndeterminateProgress' name='h_indeterminate_progress'>
        <property name='geometry'>
            <rect>
                <x>0</x>
                <y>0</y>
                <width>200</width>
                <height>24</height>
            </rect>
        </property>
    </widget>
</ui>
"""


class HIndeterminateProgressPlugin(QDesignerCustomWidgetInterface):
    def __init__(self):
        super().__init__()
        self._form_editor = None

    def createWidget(self, parent):
        from hwidgets import Theme
        t = HIndeterminateProgress(parent, hstyle=Theme())
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
        return 'HIndeterminateProgress'

    def toolTip(self):
        return 'HIndeterminateProgress widget'

    def whatsThis(self):
        return self.toolTip()
