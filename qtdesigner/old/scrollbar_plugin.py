from __future__ import annotations

from hwidgets import HScrollBar

from PySide6.QtDesigner import QDesignerCustomWidgetInterface
from PySide6.QtGui import QIcon

DOM_XML = """
<ui language='c++'>
    <widget class='HScrollBar' name='h_scroll_bar'>
        <property name='geometry'>
            <rect>
                <x>0</x>
                <y>0</y>
                <width>12</width>
                <height>100</height>
            </rect>
        </property>
        <property name='orientation'>
            <enum>Qt::Vertical</enum>
        </property>
    </widget>
</ui>
"""


class HScrollBarPlugin(QDesignerCustomWidgetInterface):
    def __init__(self):
        super().__init__()
        self._form_editor = None

    def createWidget(self, parent):
        from hwidgets import Theme
        t = HScrollBar(parent, theme=Theme())
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
        return 'HScrollBar'

    def toolTip(self):
        return 'HScrollBar widget'

    def whatsThis(self):
        return self.toolTip()
