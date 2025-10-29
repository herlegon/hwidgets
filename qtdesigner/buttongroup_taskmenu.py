# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

from hwidgets import HButtonGroup

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout
from PySide6.QtDesigner import (
    QExtensionFactory,
    QPyDesignerTaskMenuExtension
)


class HButtonGroupDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self._button_group = HButtonGroup(self)
        layout.addWidget(self._button_group)




class HButtonGroupTaskMenu(QPyDesignerTaskMenuExtension):
    def __init__(self, button_group, parent):
        super().__init__(parent)
        self._button_group = button_group
        self._edit_state_action = QAction('Edit State...', None)
        # self._edit_state_action.triggered.connect(self._edit_state)

    def taskActions(self):
        return [self._edit_state_action]

    def preferredEditAction(self):
        return self._edit_state_action

    @Slot()
    def _edit_state(self):
        return
        # dialog = HButtonGroup(self._button_group)
        # dialog.set_state(self._button_group.state)
        # if dialog.exec() == QDialog.DialogCode.Accepted:
        #     self._button_group.state = dialog.state()


class HButtonGroupTaskMenuFactory(QExtensionFactory):
    def __init__(self, extension_manager):
        super().__init__(extension_manager)

    @staticmethod
    def task_menu_iid():
        return 'org.qt-project.Qt.Designer.TaskMenu'

    def createExtension(self, object, iid, parent):
        if iid != HButtonGroupTaskMenuFactory.task_menu_iid():
            return None
        if object.__class__.__name__ != 'HButtonGroup':
            return None
        return HButtonGroupTaskMenu(object, parent)
