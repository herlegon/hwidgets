from PySide6.QtWidgets import (

    QSizePolicy,
    QSpacerItem,
)



class HSpacer(QSpacerItem):
    def __init__(self, w: int = -1) -> None:
        if w == -1:
            super().__init__(
                0,
                1,
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed,
            )
        else:
            super().__init__(
                w,
                1,
                QSizePolicy.Policy.Fixed,
                QSizePolicy.Policy.Fixed,
            )


class VSpacer(QSpacerItem):
    def __init__(self, h: int = -1) -> None:
        if h == -1:
            super().__init__(
                1,
                0,
                QSizePolicy.Policy.Fixed,
                QSizePolicy.Policy.Expanding,
            )
        else:
            super().__init__(
                1,
                h,
                QSizePolicy.Policy.Fixed,
                QSizePolicy.Policy.Fixed,
            )


