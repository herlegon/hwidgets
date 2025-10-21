
from copy import copy
import os
from pathlib import Path
import time
from PySide6.QtCore import (
    QObject,
    QSize,
    Qt,
    QPropertyAnimation,
    QAbstractAnimation,
    Property,
    QEasingCurve,
    QEvent,
    Signal,
    QPoint,
)
from PySide6.QtGui import (
    QMouseEvent,
    QPixmap,
    QPainter,
    QColor,
    QResizeEvent,
    QPaintEvent,
    QWheelEvent,
    QImage,
)
from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QFrame,
    QLabel,
    QHBoxLayout,
    QSizePolicy,
    QScrollArea,
    QAbstractButton,
    QSpacerItem,
)

from .utils import load_png_icon
from .utils import (
    TITLE_BAR_ICON_PATH,
    dp_to_px,
    CheckboxColor,
)

ACCORDION_HEIGHT: int = 42
ACCORDION_RADIUS: int = 12

CHEVRON_SIZE: int = round(36/(2 * dp_to_px)) * 2
ICON_SIZE: int = 24
BUTTON_SIZE: int = 18


class _Chevron(QAbstractButton):

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.expanded: bool = False
        self.setCheckable(True)
        self.setChecked(False)
        self._angle: float = 0
        self._previous_angle: float = self._angle

        chevron_expand = "expand_more_FILL0_wght400_GRAD0_opsz24.png"
        chevron_collapse = "expand_less_FILL0_wght400_GRAD0_opsz24.png"
        color = "#E0E0E0"
        self.pixmaps: QPixmap = {
            # Expanded
            True: self._generate_pixmap(filename=chevron_collapse, color=color),
            False: self._generate_pixmap(filename=chevron_expand, color=color),
        }
        self.setFixedSize(QSize(CHEVRON_SIZE, CHEVRON_SIZE))
        origin = [int((CHEVRON_SIZE - ICON_SIZE)/2)] * 2
        self.pixmap_origin = QPoint(*origin)
        self.painter = QPainter()
        self.setText("")

        self.animation = QPropertyAnimation(self, b'angle')
        self.animation_duration: int = 333
        self.animation.setStartValue(0)
        self.animation.setEndValue(180)
        self.animation.setDuration(self.animation_duration)
        self.animation.setDirection(QAbstractAnimation.Direction.Forward)
        self.animation.setEasingCurve(QEasingCurve.Type.Linear)
        self.installEventFilter(self)


    def _generate_pixmap(self, filename: str, color: str) -> QPixmap:
        filepath = os.path.join(TITLE_BAR_ICON_PATH, filename)
        if not os.path.exists(filepath):
            raise ValueError(f"image {filepath} does not exist")
        qimage: QImage = QImage(filepath)
        color = QColor(color)

        painter: QPainter = QPainter()
        painter.begin(qimage)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.setBrush(color)
        painter.setPen(color)
        painter.drawRect(qimage.rect().adjusted(1, 1, -1, -1))
        painter.end()
        return QPixmap(qimage)


    def setExpanded(self, expand: bool, duration: int = 1) -> None:
        self.animation_duration = duration
        self.setChecked(expand)


    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        return self.parentWidget().mouseReleaseEvent(e)


    def setChecked(self, expand: bool) -> None:
        if self.expanded == expand:
            return

        self.expanded = expand
        # self.animation.stop()
        if expand:
            print(f"expand")
            self.animation.setDirection(QAbstractAnimation.Direction.Forward)
            self.animation.setDuration(self.animation_duration/2.355)
        else:
            print(f"collapse")
            self.animation.setDirection(QAbstractAnimation.Direction.Backward)
            self.animation.setDuration(self.animation_duration/3.925)
        self.animation.start()


    @Property(float)
    def angle(self) -> float:
        return self._angle


    @angle.setter
    def angle(self, value: float) -> None:
        self._angle = value
        # print(f"changed angle to {self._angle}")
        self.update()


    def paintEvent(self, event: QPaintEvent) -> None:
        # print(f"_Chevron: paintEvent, angle: {self.angle}")
        painter: QPainter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform
        )
        if self.angle == 0:
            painter.drawPixmap(self.pixmap_origin + QPoint(1, 1), self.pixmaps[False])
        elif self.angle == 180:
            painter.drawPixmap(self.pixmap_origin + QPoint(-1, 0), self.pixmaps[True])
        else:
            x, y = (self.size()/2).toTuple()
            painter.translate(x, y)
            painter.rotate(self.angle)
            painter.drawPixmap(
                QPoint(-x, -y),
                self.pixmaps[False]
            )


    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() in (
            QEvent.Type.Move,
            QEvent.Type.WindowActivate,
            QEvent.Type.WindowDeactivate,
            QEvent.Type.Enter,
            QEvent.Type.Leave,
            QEvent.Type.HoverEnter,
            QEvent.Type.HoverMove,
            QEvent.Type.HoverLeave,
            QEvent.Type.ToolTip,
        ):
            # Block signals to avoid too many repaint event
            return True
        # print(f"{time.time()} {watched} 0x{event.type():02x}")
        return super().eventFilter(watched, event)



class AccordionItem(QScrollArea):

    class _TitleBar(QWidget):
        signal_pressed = Signal()

        def __init__(
            self,
            parent: QWidget | None,
            title: str = '',
            icon: str | Path | QPixmap | None = None,
        ) -> None:
            super().__init__(parent)
            self.setObjectName("accordion_title_bar")
            self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.is_under_mouse: bool = False

            self.icon_pixmap: QPixmap | None = None
            if icon is not None:
                self.icon_pixmap = (
                    icon
                    if isinstance(icon, QPixmap)
                    else load_png_icon(icon, QColor(230,230,230))
                )
            self.icon = QLabel('', self)
            self.title = QLabel(title, self)
            self.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            )
            self.chevron = _Chevron(parent)
            self.chevron.setExpanded(False)

            layout = QHBoxLayout(self)
            layout.setContentsMargins(0, 0, int(ACCORDION_RADIUS + 16 + 4), 0)
            layout.setSpacing(0)
            layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            layout.addWidget(self.icon)
            layout.addWidget(self.title, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            layout.addSpacerItem(
                QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            )
            layout.addWidget(self.chevron)
            # layout.addSpacerItem(
            #     QSpacerItem(32, 1, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            # )
            # layout.addStretch(1)
            self.setLayout(layout)

            self.color: str = "#f0f0f0"
            self.bgd_color: QColor = QColor("#3A3A3A")
            self.bgd_color_hover = copy(self.bgd_color)
            self.bgd_color_hover.setAlpha(180)

            self.setStyleSheet(
                """
                    QWidget {{
                        color: {color};
                        font-weight: bold;
                        font-size: 18px;
                    }}
                """.format(
                    name=self.objectName(),
                    color=self.color
                )
            )
            self.adjustSize()
            self.setFixedHeight(ACCORDION_HEIGHT)
            self.scroll_area_width: int = self.width()
            self.scroll_area_height: int = ACCORDION_HEIGHT
            self.installEventFilter(self)


        def setText(self, text: str) -> None:
            self.title.setText(text)


        def setScrollAreaSize(self, w: int, h: int) -> None:
            self.scroll_area_width = w
            self.scroll_area_height = h


        def setExpanded(self, expand: bool, duration: int) -> None:
            self.chevron.setExpanded(expand, duration)


        def wheelEvent(self, event: QWheelEvent) -> None:
            self.parent().wheelEvent(event)


        def eventFilter(self, watched: QObject, event: QEvent) -> bool:
            event_type = event.type()

            if event_type == QEvent.Type.Enter:
                self.is_under_mouse = True
                self.update()
                return True
            elif event_type == QEvent.Type.Leave:
                self.is_under_mouse = False
                self.update()
                return True

            event: QMouseEvent = event
            if (event_type== QEvent.Type.MouseButtonRelease
                and event.button() == Qt.MouseButton.LeftButton):
                self.signal_pressed.emit()

            # print(f"{time.time()} {watched} 0x{event.type():02x}")
            return super().eventFilter(watched, event)


        def paintEvent(self, event: QPaintEvent) -> None:
            painter = QPainter(self)
            painter.setRenderHints(QPainter.RenderHint.Antialiasing)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(
                self.bgd_color_hover
                if self.is_under_mouse
                else self.bgd_color
            )
            height = max(self.scroll_area_height, ACCORDION_HEIGHT)
            painter.drawRoundedRect(
                0, 0, self.scroll_area_width, height,
                ACCORDION_RADIUS, ACCORDION_RADIUS
            )




    class _ScrollAreaWidget(QWidget):
        def __init__(self, parent: QWidget) -> None:
            super().__init__(parent)
            self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.container_bgd_color: QColor = QColor("#7f7f7f")
            self.bgd_color: QColor = QColor("#3A3A3A")

            self.setStyleSheet("background-color: transparent;")


        def setContainerBackgroundColor(self, color: str) -> None:
            self.container_bgd_color = QColor(color)


        def resizeEvent(self, event: QResizeEvent) -> None:
            return super().resizeEvent(event)


        def eventFilter(self, watched: QObject, event: QEvent) -> bool:
            if event.type() in (
                QEvent.Type.Move,
                QEvent.Type.WindowActivate,
                QEvent.Type.WindowDeactivate,
                QEvent.Type.Enter,
                QEvent.Type.Leave,
                QEvent.Type.ToolTip,
            ):
                # Block signals to avoid too many repaint event
                return True
            return super().eventFilter(watched, event)


        def paintEvent(self, event: QPaintEvent) -> None:
            painter = QPainter(self)
            painter.setRenderHints(QPainter.RenderHint.Antialiasing)
            painter.setPen(Qt.PenStyle.NoPen)

            w = self.width()
            h = int((self.height() + ACCORDION_RADIUS) / 2)

            painter.setBrush(self.container_bgd_color)
            painter.drawRect(
                0, h - ACCORDION_RADIUS, w, ACCORDION_RADIUS
            )
            painter.setBrush(self.bgd_color)
            painter.drawRect(0, 0, w, ACCORDION_RADIUS)
            painter.drawRoundedRect(
                0, 0, w, h,
                ACCORDION_RADIUS,
                ACCORDION_RADIUS
            )


    def __init__(
        self,
        parent: QWidget | None,
        title: str = '',
        icon: str | Path | QPixmap | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("accordion_item")
        self._content_height = 0
        self._expanded: bool = False
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.border = False

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.horizontalScrollBar().setFixedHeight(0)
        self.verticalScrollBar().setValue(0)
        self.setWidgetResizable(True)

        self._widget = self._ScrollAreaWidget(self)
        self._layout = QVBoxLayout(self._widget)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        # Title bar
        self.title_bar = self._TitleBar(self, title=title)
        title_bar_height = self.title_bar.height()

        # Content
        self.content = QWidget(self._widget)
        self.content.setObjectName("content")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(
            ACCORDION_RADIUS, ACCORDION_RADIUS, ACCORDION_RADIUS, 0
        )
        self.content_height: int = 0
        self._padding = QWidget(self._widget)

        # Insert in layout
        self._layout.addWidget(self.content)
        self._layout.addWidget(self._padding)

        # Update size
        self.setWidget(self._widget)
        self.setFixedHeight(title_bar_height)
        self.setViewportMargins(0, title_bar_height, 0, 0)

        # Animation for expand/collapse
        self.animation = QPropertyAnimation(self.verticalScrollBar(), b"value", self)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.animation.setDuration(1500)
        self.animation.valueChanged.connect(self.value_changed)
        self.animation.finished.connect(self.finished)

        self.title_bar.signal_pressed.connect(self.toggle_state_event)

        self.setStyleSheet("""
            #accordion_item {
                background-color: transparent;
                color: white;


            }
        """)
        # self.installEventFilter(self)


    # def sizeHint(self) -> QSize:
    #     print("accordion item: sizeHint")
    #     return QSize(self.width(), self.content_height)


    # def minimumSizeHint(self) -> QSize:
    #     print("accordion item: minimumSizeHint")
    #     return QSize(self.width(), self.content_height)


    # def minimumHeight(self) -> int:
    #     print("accordion item: minimumHeight")
    #     return self.content_height


    def setContainerBackgroundColor(self, color: str) -> None:
        # Used to avoid set transparent color in stylesheet
        # TODO: remove this?
        self._widget.setContainerBackgroundColor(color)


    def value_changed(self):
        y_top = self.viewportMargins().top()
        height = max(
            y_top + self.content_height - self.verticalScrollBar().value(),
            y_top
        )
        self.setFixedHeight(height)


    def finished(self) -> None:
        pass


    def toggle_state(self, expand: bool, force: bool = False) -> None:
        if self._expanded == expand:
            return
        self._expanded = expand
        self.animation.stop()
        if expand:
            start_value = self.content_height
            self.verticalScrollBar().setValue(start_value)
            end_value = 0
        else:
            start_value = self.verticalScrollBar().value()
            self.verticalScrollBar().setMaximum(self._widget.height())
            end_value = self.verticalScrollBar().maximum()

        duration = 2 * abs(end_value - start_value) if not force else 1
        self.animation.setStartValue(start_value)
        self.animation.setEndValue(end_value)
        self.animation.setDuration(duration)
        self.title_bar.setExpanded(True if expand else False, duration)
        self.animation.start()


    def toggle_state_event(self):
        self.toggle_state(not (self._expanded))


    def resizeEvent(self, event: QResizeEvent) -> None:
        self.title_bar.setScrollAreaSize(self.width(), self.height())
        self._widget.setFixedWidth(self.width())
        self.repaint()


    def adjustSize(self) -> None:
        print("AccordionItem: adjustSize")
        self.content.adjustSize()
        self.content_height = (
            self.content_layout.sizeHint().height()
            + self.content_layout.contentsMargins().top()
            + self.content_layout.contentsMargins().bottom()
        )
        self.title_bar.setFixedWidth(self.width())
        self._padding.setFixedHeight(self.content_height)
        self.verticalScrollBar().setValue(self.content_height)



    def setWidth(self, w: int) -> None:
        self.title_bar.setFixedWidth(w)


    def setExpanded(self, expand: bool) -> None:
        self.toggle_state(expand, force=True)


    def wheelEvent(self, event: QWheelEvent) -> None:
        self.parent().wheelEvent(event)

    # keep for debug
    # def eventFilter(self, watched: QObject, event: QEvent) -> bool:
    #     print(f"{time.time()} {watched} 0x{event.type():02x}")
    #     return super().eventFilter(watched, event)
