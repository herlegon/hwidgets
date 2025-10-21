from PySide6.QtCore import QObject
from PySide6.QtWidgets import (
    QButtonGroup,
    QAbstractButton,
)


class ButtonGroup(QButtonGroup):

    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.buttonClicked.connect(self.button_clicked)


    def button_clicked(self, button: QAbstractButton) -> None:
        id = self.id(button)
        for b in self.buttons():
            if self.id(b) != id:
                b.setChecked(False)

