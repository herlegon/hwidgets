from string import Template
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
from .hstyle import (
    COMBOBOX_RADIUS,
    SCROLLBAR_TRACK_WIDTH,
    HStyle,
    load_qss,
)


class HScrollBar(QScrollBar):
    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        hstyle: HStyle,
    ):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.ArrowCursor)

        # self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.hstyle= hstyle
        self.qss_template = Template(load_qss("hscrollbar.qss"))
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        )
        self.setFixedWidth(SCROLLBAR_TRACK_WIDTH)
        self.setSingleStep(0)


    def _update_stylesheet(self) -> None:
        hstyle = self.hstyle

        qss = self.qss_template.substitute(
            radius=f"{COMBOBOX_RADIUS}px",
            hover_bgd=f"{hstyle.hover_bgd}",
            selection_bgd=f"{hstyle.selection_bgd}",

            widget_bgd=f"{hstyle.widget_bgd}",
            handle_bgd=f"{hstyle.hover_bgd}",
            handle_bgd_hover=f"{hstyle.selection_bgd}",

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
        cr = COMBOBOX_RADIUS
        full_rect = parent.rect()
        # shrink height by 2*corner_radius, and move down by corner_radius
        self.setGeometry(
            QRect(
                full_rect.width() - self.width(),
                cr,
                self.width(),
                full_rect.height() - 2 * cr
            )
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateGeometryRelativeToParent()
