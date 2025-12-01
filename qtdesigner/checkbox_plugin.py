from __future__ import annotations

from hwidgets import HCheckBox, StyleManager

from PySide6.QtDesigner import QDesignerCustomWidgetInterface
from PySide6.QtGui import QIcon

DOM_XML = """
<ui language='c++'>
    <widget class='HCheckBox' name='h_check_box'>
        <property name='geometry'>
            <rect>
                <x>0</x>
                <y>0</y>
                <width>100</width>
                <height>24</height>
            </rect>
        </property>
        <property name='text'>
            <string>CheckBox</string>
        </property>
    </widget>
</ui>
"""


class HCheckBoxPlugin(QDesignerCustomWidgetInterface):
    def __init__(self):
        super().__init__()
        self._form_editor = None

    def createWidget(self, parent):
        from hwidgets import StyleManager, HCheckBox
        t = HCheckBox(parent, theme=StyleManager().get_theme())
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
        return 'HCheckBox'

    def toolTip(self):
        return 'HCheckBox widget'

    def whatsThis(self):
        return self.toolTip()
