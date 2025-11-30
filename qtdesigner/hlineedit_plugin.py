from __future__ import annotations

from hwidgets import (
    Theme,
    StyleManager,
    HLineEdit
)

from PySide6.QtDesigner import (
    QDesignerCustomWidgetInterface,
    QDesignerFormEditorInterface,
)
from PySide6.QtGui import QIcon


DOM_XML = """
<ui language='c++'>
    <widget class='HLineEdit' name='h_line_edit'>
        <property name='geometry'>
            <rect>
                <x>0</x>
                <y>0</y>
                <width>100</width>
                <height>24</height>
            </rect>
        </property>
    </widget>
</ui>
"""


class HLineEditPlugin(QDesignerCustomWidgetInterface):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initialized = False


    def initialize(self, core: QDesignerFormEditorInterface):
        self._form_editor = core


    def isInitialized(self):
        return self._form_editor is not None


    def createWidget(self, parent):
        theme = StyleManager().get_theme()
        t = HLineEdit(parent, theme=theme)
        return t


    def domXml(self):
        return DOM_XML


    def group(self):
        return 'Hwidgets'


    def name(self):
        return 'HLineEdit'


    def icon(self):
        return QIcon()


    def includeFile(self):
        return 'hwidgets'


    def isContainer(self):
        return False


    def toolTip(self):
        return 'HLineEdit widget'


    def whatsThis(self):
        return self.toolTip()
