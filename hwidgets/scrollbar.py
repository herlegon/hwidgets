from string import Template
from typing import Type
from PySide6.QtCore import (
    Qt,
    QRect,
)
from PySide6.QtWidgets import (
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QScrollBar
)
from .style_manager import Theme
from .utils import (
    load_qss,
)


class HScrollBar(QScrollBar):
    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        theme: Type[Theme],
    ):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.ArrowCursor)

        # self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.theme: Theme = theme
        self.qss_template = Template(load_qss("scrollbar.qss"))
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        )
        self.setFixedWidth(self.theme.scrollbar.track_width)
        self.setSingleStep(0)


    def _update_stylesheet(self) -> None:
        theme = self.theme

        qss = self.qss_template.substitute(
            radius=f"{self.theme.common.radius}px",
            hover_bgd=f"{self.theme.common.hover}",
            selection_bgd=f"{self.theme.common.selection}",

            widget_bgd=f"{theme.common.bgd}",
            handle_bgd=f"{theme.common.hover}",
            handle_bgd_hover=f"{theme.common.selection}",

            widget_margin=1,
            track_width=self.width(),
            track_radius=int(self.width()/2),
            handle_width=self.width(),
            handle_radius=int(self.width() / 2),
        )
        self.setStyleSheet(qss)


    def setFixedWidth(self, w: int) -> None:
        super().setFixedWidth(w)
        self._update_stylesheet()


    def setOrientation(self, orientation: Qt.Orientation) -> None:
        return


    def updateGeometryRelativeToParent(self):
        """Adjust the scrollbar height relative to parent's rounded corners."""
        if not self.parent():
            return

        parent: QWidget = self.parent()
        radius = self.theme.common.radius
        full_rect = parent.rect()
        # shrink height by 2*corner_radius, and move down by corner_radius
        self.setGeometry(
            QRect(
                full_rect.width() - self.width(),
                radius,
                self.width(),
                full_rect.height() - 2 * radius
            )
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateGeometryRelativeToParent()
