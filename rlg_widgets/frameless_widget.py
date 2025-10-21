from typing import Optional
from .title_bar.title_bar import OsStyle
from .utils import BORDER_RADIUS
from .window.rlg_window import RlgWindow
from PySide6.QtWidgets import (
    QWidget
)


class MainFlWindow(RlgWindow):

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        os_style: OsStyle = 'windows'
    ):
        super().__init__(
            parent,
            border_radius=BORDER_RADIUS,
            os_style=os_style,
        )



class FlDialog(RlgWindow):

    def __init__(
        self,
        parent: Optional[QWidget],
        os_style: OsStyle = 'windows'
    ):
        super().__init__(
            parent,
            resizable=False,
            border_radius=BORDER_RADIUS,
            os_style=os_style,
        )
