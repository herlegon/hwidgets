from __future__ import annotations

from hwidgets import HButtonGroup, StyleManager
from buttongroup_taskmenu import HButtonGroupTaskMenuFactory

from PySide6.QtDesigner import QDesignerCustomWidgetInterface
from PySide6.QtGui import QIcon

DOM_XML = """
<ui language='c++'>
    <widget class='HButtonGroup' name='h_button_group'>
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


class HButtonGroupPlugin(QDesignerCustomWidgetInterface):
    def __init__(self):
        super().__init__()
        self._form_editor = None
        self._task_menus = []  # Keep a reference

    def createWidget(self, parent):
        t = HButtonGroup(parent, theme=StyleManager().get_theme())
        t.set_buttons([
            'button1', 'button2', 'button3'
        ])
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
        manager = form_editor.extensionManager()
        iid = HButtonGroupTaskMenuFactory.task_menu_iid()
        manager.registerExtensions(HButtonGroupTaskMenuFactory(manager), iid)

    def isContainer(self):
        return False

    def isInitialized(self):
        return self._form_editor is not None

    def name(self):
        return 'HButtonGroup'

    def toolTip(self):
        return 'HButtonGroup tip'

    def whatsThis(self):
        return self.toolTip()




