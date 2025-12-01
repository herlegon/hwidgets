from __future__ import annotations

from hwidgets import HRadialProgress, StyleManager

from PySide6.QtDesigner import QDesignerCustomWidgetInterface
from PySide6.QtGui import QIcon

DOM_XML = """
<ui language='c++'>
    <widget class='HRadialProgress' name='h_radial_progress'>
        <property name='geometry'>
            <rect>
                <x>0</x>
                <y>0</y>
                <width>100</width>
                <height>100</height>
            </rect>
        </property>
        <property name='value'>
            <number>0</number>
        </property>
    </widget>
</ui>
"""


class HRadialProgressPlugin(QDesignerCustomWidgetInterface):
    def __init__(self):
        super().__init__()
        self._form_editor = None

    def createWidget(self, parent):
        t = HRadialProgress(parent, theme=StyleManager().get_theme())
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
        return 'HRadialProgress'

    def toolTip(self):
        return 'HRadialProgress widget'

    def whatsThis(self):
        return self.toolTip()
