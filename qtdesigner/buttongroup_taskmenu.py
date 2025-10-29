from __future__ import annotations

from hwidgets import HButtonGroup

from PySide6.QtCore import (
    Slot,
    Signal,
    Qt,
)
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QSizePolicy,
    QLineEdit,
)
from PySide6.QtDesigner import (
    QExtensionFactory,
    QPyDesignerTaskMenuExtension
)


# Keep all created task menu objects alive (Designer only keeps weak refs)
_created_task_menus: list[HButtonGroup] = []



class HButtonGroupTaskMenu(QPyDesignerTaskMenuExtension):
    def __init__(self, button_group: HButtonGroup, parent):
        super().__init__(parent)
        self._button_group = button_group
        # self._edit_state_action = QAction('Edit Buttons...', self)
        # self._edit_state_action.triggered.connect(self._edit_buttons)  # connect it

        # Action shown in Designer context menu
        self._edit_buttons_action = QAction("Edit Buttons...", self)
        self._edit_buttons_action.triggered.connect(self._edit_buttons)

    def taskActions(self):
        """Return list of actions available for this widget."""
        return [self._edit_buttons_action]

    def preferredEditAction(self):
        """Return the preferred action (triggered when double-clicked)."""
        return self._edit_buttons_action

    @Slot()
    def _edit_buttons(self):
        """Open a dialog to edit button labels for HButtonGroup."""
        dialog = QDialog()
        # dialog = QDialog(self._button_group)
        dialog.setWindowTitle("Edit HButtonGroup Buttons")
        dialog.resize(400, 300)

        root_layout = QVBoxLayout(dialog)

        main_layout = QHBoxLayout()

        # --- Left: list of buttons ---
        list_widget = QListWidget(dialog)
        list_widget.addItems([b.text() for b in self._button_group.buttons()])
        list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        main_layout.addWidget(list_widget, 3)

        # --- Right: controls ---
        side_layout = QVBoxLayout()

        input_widget = QLineEdit(dialog)
        input_widget.setPlaceholderText("Button name...")
        side_layout.addWidget(input_widget)

        btn_add = QPushButton("Add", dialog)
        btn_remove = QPushButton("Remove", dialog)
        btn_up = QPushButton("Move Up", dialog)
        btn_down = QPushButton("Move Down", dialog)

        for b in (btn_add, btn_remove, btn_up, btn_down):
            b.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            side_layout.addWidget(b)

        side_layout.addStretch()
        main_layout.addLayout(side_layout, 1)

        root_layout.addLayout(main_layout)

        # --- Bottom: OK / Cancel ---
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            dialog
        )
        root_layout.addWidget(buttons)


        # === Behaviors ===
        def on_add():
            text = input_widget.text().strip()
            if text:
                list_widget.addItem(text)
                input_widget.clear()

        def on_remove():
            for item in list_widget.selectedItems():
                list_widget.takeItem(list_widget.row(item))

        def on_up():
            row = list_widget.currentRow()
            if row > 0:
                item = list_widget.takeItem(row)
                list_widget.insertItem(row - 1, item)
                list_widget.setCurrentRow(row - 1)

        def on_down():
            row = list_widget.currentRow()
            if 0 <= row < list_widget.count() - 1:
                item = list_widget.takeItem(row)
                list_widget.insertItem(row + 1, item)
                list_widget.setCurrentRow(row + 1)

        btn_add.clicked.connect(on_add)
        btn_remove.clicked.connect(on_remove)
        btn_up.clicked.connect(on_up)
        btn_down.clicked.connect(on_down)

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        # === Apply changes ===
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        dialog.activateWindow()
        dialog.raise_()
        # dialog.exec()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_buttons = [list_widget.item(i).text() for i in range(list_widget.count())]
            self._button_group.setButtons(";".join(new_buttons))




class HButtonGroupTaskMenuFactory(QExtensionFactory):
    """Factory that provides HButtonGroupTaskMenu extensions to Qt Designer."""

    IID = "org.qt-project.Qt.Designer.TaskMenu"

    def __init__(self, extension_manager):
        super().__init__(extension_manager)

    @staticmethod
    def task_menu_iid():
        return HButtonGroupTaskMenuFactory.IID

    def createExtension(self, object, iid, parent):
        """Create the task menu extension for HButtonGroup widgets."""
        if iid != self.IID:
            return None
        if not isinstance(object, HButtonGroup):
            return None

        ext = HButtonGroupTaskMenu(object, parent)

        # Prevent garbage collection of Python-side object
        _created_task_menus.append(ext)

        return ext
