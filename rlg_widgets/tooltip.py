from PySide6.QtCore import (
    QEvent,
    Qt,
    QSize,
    QPoint,
    QObject,
    Signal,
    QTimer,
)
from PySide6.QtGui import (
    QCursor,
)
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
    QLabel,
    QSizePolicy,
)

from .utils import (
    BORDER_RADIUS,
)

TOOLTIP_HEIGHT_MIN = 24
TOOLTIP_PADDING = 8


class ToolTip(QFrame):
    entered = Signal()

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        # This does not work (bug in Qt6)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        main_layout = QVBoxLayout(self)
        self.label = QLabel(self)
        main_layout.addWidget(self.label)
        main_layout.setContentsMargins(0,0,0,0)
        self.setLayout(main_layout)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum))
        self.setMinimumSize(QSize(2*TOOLTIP_PADDING, TOOLTIP_HEIGHT_MIN))

        self.set_style()
        self.installEventFilter(self)



    def setText(self, text: str) -> None:
        self.label.setText(text)
        self.label.adjustSize()
        self.adjustSize()


    def set_style(self) -> None:
        # self.button_style = deepcopy(button_style)
        self.bgd_color = "#7F7F7F"
        self.text_color = "#E1E1E1"
        self._update_stylesheet()
        self.setStyleSheet(self.stylesheet)
        self.repaint()


    def _update_stylesheet(self) -> None:
        self.stylesheet = """
            background-color: {bgd_color};
            color: {text_color};
            border-radius: {radius}px;
            padding-left: {padding_h}px;
            padding-right: {padding_h}px;
            padding-top: {padding_v}px;
            padding-bottom: {padding_v}px;
        """.format(
            bgd_color=self.bgd_color,
            text_color=self.text_color,
            padding_h=TOOLTIP_PADDING,
            padding_v=4,
            radius=int(BORDER_RADIUS/2)
        )

    # def eventFilter(self, watched: QObject, event: QEvent) -> bool:
    #     if event.type() in (QEvent.Type.Enter, QEvent.Type.HoverEnter):
    #         self.entered.emit()
    #         return True
    #     return super().eventFilter(watched, event)




class ToolTipEventFilter(QObject):
    def __init__(
        self,
        parent: QWidget,
        delay_ms: int = 500,
        follow_cursor: bool = False
    ) -> None:
        super().__init__(parent)
        widget: QWidget = parent
        self.tip = ToolTip(widget.window())
        self.tip.setText(widget.toolTip())

        # SetStyle is discouraged for real applications
        # https://doc.qt.io/qt-6/qwidget.html#setStyle
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(delay_ms)
        self.timer.timeout.connect(self.timeout)
        self.follow_cursor: bool = follow_cursor

    def timeout(self) -> None:
        self.tip.move(self.get_position())
        self.tip.show()


    def get_position(self) -> QPoint:
        parent: QWidget = self.parent()
        cursor_pos = QCursor().pos()
        position = parent.mapFromGlobal(cursor_pos)
        x, y = parent.mapToParent(position).toTuple()
        w, h = parent.window().size().toTuple()
        delta_x = max(2*TOOLTIP_PADDING, x + self.tip.width() + BORDER_RADIUS - w)

        if y + self.tip.height() > h:
            y = parent.mapToGlobal(QPoint(0,0)) - self.tip.height()
        else:
            # y = cursor_pos.y() + parent.height()
            y = parent.mapToGlobal(QPoint(0, parent.height())).y() + TOOLTIP_PADDING
        return QPoint(cursor_pos.x() - delta_x, y)


    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        event_type = event.type()

        if event_type == QEvent.Type.ToolTip:
            return True

        elif event_type == QEvent.Type.Enter:
            if self.tip.isHidden():
                # if not parent.isEnabled():
                #   return True

                self.timer.stop()
                if self.timer.interval() == 0:
                    self.timeout()
                else:
                    self.timer.start()
                return True

        elif event_type == QEvent.Type.HoverMove and self.follow_cursor:
            if self.tip.isVisible():
                self.tip.move(self.get_position())
                return True

        elif event_type in (QEvent.Type.HoverLeave,
                            QEvent.Type.MouseButtonRelease,
                            QEvent.Type.MouseButtonPress):
            self.timer.stop()
            try:
                self.tip.hide()
            except:
                pass

        return super().eventFilter(watched, event)
