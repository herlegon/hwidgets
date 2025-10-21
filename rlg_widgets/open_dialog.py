


import os
from pathlib import Path
import sys
from typing import Literal, Optional
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, Signal,
    QSize, QTime, QUrl, Qt,
    QEvent,


    )
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QDragEnterEvent, QFocusEvent,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QMouseEvent, QPaintEvent, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform,
)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QPushButton,
    QSizePolicy, QWidget,
    QLabel,
        QStyledItemDelegate,
        QLineEdit,

    QFileDialog)

from .utils import BORDER_RADIUS


COMBOBOX_HEIGHT = 32
COMBOBOX_RADIUS = 4
COMBOBOX_PADDING = 12



class OpenDialog(QWidget):
    signal_f_selected = Signal(str)

    class _ComboBox(QComboBox):
        mouseReleased = Signal()

        def __init__(self, parent: QWidget) -> None:
            super().__init__(parent)
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.icon_height = COMBOBOX_HEIGHT - COMBOBOX_RADIUS
            self.icon_width = self.icon_height
            self.radius = COMBOBOX_RADIUS
            size = QSize(self.icon_height, self.icon_height)
            self.icon_size: QSize = size
            self.icon: QPixmap | None = None
            self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
            if sys.platform == 'win32':
                self.set_icon("A:\\mco\\tools\\icons\\icon_32.png")
            else:
                self.set_icon("/home/adg/mco/tools/icons/icon_32.png")

        def setHeight(self, height: int, radius:int) -> None:
            self.radius = radius
            self.icon_height = height - 2 * radius
            size = QSize(self.icon_height, self.icon_height)
            self.icon_size: QSize = size
            if sys.platform == 'win32':
                self.set_icon("A:\\mco\\tools\\icons\\icon_32.png")
            else:
                self.set_icon("/home/adg/mco/tools/icons/icon_32.png")
            return super().setFixedHeight(height)


        def set_icon(self, icon: str | Path | QPixmap) -> None:
            if isinstance(icon, str | Path):
                if not os.path.exists(icon):
                    raise ValueError(f"{icon} not found")
                icon = QPixmap(icon)
            if icon.size() != self.icon_size:
                icon = icon.scaled(
                    self.icon_size,
                    aspectMode=Qt.AspectRatioMode.KeepAspectRatio
                )
            self.icon = icon
            self.icon_rect = QRect(
                self.width() - icon.size().width(),
                0,
                self.width(),
                self.height()
            )
            x, y  = ((self.size() - self.icon.size())/2).toTuple()
            self.pixmap_origin = QPoint(max(0, int(x)), max(0, int(y)))

        def mouseReleaseEvent(self, e: QMouseEvent) -> None:
            self.mouseReleased.emit()

        # def mousePressEvent(self, e: QMouseEvent) -> None:
        #     return

        def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
            return

        def paintEvent(self, e: QPaintEvent) -> None:
            super().paintEvent(e)
            painter: QPainter = QPainter(self)
            painter.drawPixmap(
                QRect(
                    self.width() - self.icon_width - COMBOBOX_PADDING,
                    self.radius,
                    self.icon_height,
                    self.icon_height),
                # self.pixmap_origin,
                self.icon,
                # QRect(0,0,self.icon_width,self.icon_width)
            )


    def __init__(
        self,
        parent: QWidget | None = None,
        mode: Literal['file', 'folder'] = 'file'
    ) -> None:
        super().__init__(parent)
        self.setObjectName("open_dialog")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mode = mode
        self.last_dir = str(Path.home())
        self.file_filter = "All files (*.*)"
        self.allowed_extensions = []

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(24,24)
        self.main_layout.addWidget(self.icon_label)

        self.combobox_path = self._ComboBox(self)
        # self.combobox_path.setSizePolicy(
        #     QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # )
        # self.combobox_path.setMinimumSize(QSize(220, 0))
        self.combobox_path.setHeight(COMBOBOX_HEIGHT, COMBOBOX_RADIUS)
        self.combobox_path.setFixedWidth(230)
        self.combobox_path.setAcceptDrops(True)
        self.combobox_path.setEditable(True)
        self.combobox_path.lineEdit().setReadOnly(True)
        self.main_layout.addWidget(self.combobox_path)

        # self.button_browse = QPushButton(self)
        # self.button_browse.setSizePolicy(
        #     QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # )
        # self.button_browse.setMaximumSize(QSize(25, COMBOBOX_HEIGHT-4))

        # layout.addWidget(self.button_browse)

        self.combobox_path.setInsertPolicy(QComboBox.InsertPolicy.InsertAtCurrent)
        self.setAcceptDrops(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        )
        self.setFixedHeight(COMBOBOX_HEIGHT)

        self.icon: QPixmap | None = None
        self._update_stylesheet()

        # self.button_browse.clicked.connect(self.activated)
        self.combobox_path.mouseReleased.connect(self.activated)
        self.combobox_path.currentIndexChanged.connect(self.selected)
        self.combobox_path.installEventFilter(self)
        self.combobox_path.lineEdit().installEventFilter(self)
        # self.combobox_path.mouseReleased.connect(self.picker_event)
        # self.combobox_path.activated.connect(self.activated)
        # activated                # activated(int)
        # currentIndexChanged      # currentIndexChanged(int)
        # currentTextChanged       # currentTextChanged(QString)
        # editTextChanged          # editTextChanged(QString)
        # highlighted              # highlighted(int)
        # textActivated            # textActivated(QString)
        # textHighlighted          # textHighlighted(QString)
        self.is_activated: bool = False




    def _update_stylesheet(self):
        stylesheet = """
            #{name} {{
                border: 1px solid red;
                border-radius: {radius}px;
                background-color: {bgd};
                color: white;
            }}


            QComboBox {{
                color: white;
                /* margin-left: {padding}px; */
                padding-left: {padding}px;

                 border: 1px solid gray;
                border-radius: {radius}px;
                background-color: {bgd};
                /* padding: 8px; */
            }}
            QComboBox::down-arrow {{

                width: 0px;
            }}


            QComboBox QAbstractItemView {{
                background: {bgd};
                selection-background-color: lightgray;
                /* color: white; */
                /* border-top: 30px solid; */
                /* border-color: transparent;*/
                border-radius: {radius}px;
                /*width: {popup_width}px; */
                background-color: orange;
            }}

            QComboBox::drop-down {{
                width: 0px;
            }}

        """.format(
            name=self.objectName(),
            combobox_height=COMBOBOX_HEIGHT-COMBOBOX_RADIUS,
            margin=COMBOBOX_RADIUS,
            padding=COMBOBOX_PADDING,
            radius=COMBOBOX_RADIUS,
            list_margin = COMBOBOX_RADIUS*4,
            icon_margin = 0,
            bgd="#1E1E1E",
            popup_width = self.combobox_path.width(),
        )
        self.setStyleSheet(stylesheet)


        self.combobox_path.view().setStyleSheet(
            """
            QListView {{
                background-color: {bgd};
                border: 1px solid gray;
                border-radius: {radius}px;
                margin-top: 0px;
                padding-top: {radius}px;
                padding-bottom: {radius}px;
                padding-left: {padding}px;
                show-decoration-selected: 1;
            }}

            QListView::item {{
                margin-right: {padding_right}px;
                color: white;
            }}

            QListView::item:selected {{
                background: #E1E1E1;
                color: #1E1E1E;
                border-radius: {radius}px;
            }}



        """.format(
            name=self.objectName(),
            combobox_height=COMBOBOX_HEIGHT-COMBOBOX_RADIUS,
            margin=COMBOBOX_RADIUS,
            radius=COMBOBOX_RADIUS,
            padding=COMBOBOX_PADDING,
            padding_right=COMBOBOX_PADDING+COMBOBOX_RADIUS,
            list_margin = COMBOBOX_RADIUS*4,
            icon_margin = 0,
            bgd="#1E1E1E",
            popup_width = self.combobox_path.width(),
        )
        )

        self.combobox_path.lineEdit().setStyleSheet(
            """
            QLineEdit {{
                color: white;
            }}
            QLineEdit:read-only {{
                color: white;
            }}
        """)


        try:
            self.main_layout.removeWidget(self.icon_label)
        except:
            pass
        if self.icon is not None:
            self.main_layout.insertWidget(0, self.icon_label)




    def selected(self, index:int):
        print(self.combobox_path.itemText(index))
        self.combobox_path.setCurrentText(self.combobox_path.itemText(index))
        self.is_activated = False


    def activated(self):
        self.combobox_path.showPopup()
        self.is_activated = True


    def mousePressEvent(self, event):
        print("Hello world !")

    def set_file_filter(self, filter: dict[str, list[str]]) -> None:
        # Images (*.png  *.jpg)
        ffilter = []
        all_exts = []
        for f, ext in filter.items():
            all_exts.extend(ext)
            exts = '; '.join(map(lambda x: f"*{x}", ext))
            ffilter.append(f"{f.capitalize()} ({exts})")
        self.file_filter = ';;'.join(ffilter)
        self.allowed_extensions = set(all_exts)


    def dropEvent(self, event):
        urls = event.mimeData().urls()
        path = urls[0].toLocalFile()
        print("dropped: %s" % (path))
        self.signal_f_selected.emit(path)


    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            path = urls[0].toLocalFile()
            if self.mode == 'file':
                if (len(self.allowed_extensions) == 0
                    or os.path.splitext(path)[1].lower() in self.allowed_extensions):
                    event.acceptProposedAction()
            elif os.path.isdir(path):
                event.acceptProposedAction()
        # return super().dragEnterEvent(event)


    def picker_event(self):
        dialog = QFileDialog(self)
        if self.mode == 'file':
            dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
            path = dialog.getOpenFileName(
                self,
                caption='Open image',
                dir=self.last_dir,
                filter=self.file_filter,
            )
        else:
            dialog.setFileMode(QFileDialog.FileMode.Directory)
            path = dialog.getExistingDirectory(
                self,
                caption="Open folder",
                dir=self.last_dir,
                options=QFileDialog.Option.ShowDirsOnly
            )
        if path is not None:
            self.signal_f_selected.emit(path)


    def set_recent_directory(self, dir: str) -> None:
        self.last_dir = dir


    def insert_path(self, path: str):
        # If already exists,remove previous
        self.combobox_path.insertItem(0, path)


    def get_recent_paths(self) -> list[str]:
        return [self.combobox_path.itemText(i) for i in range(self.combobox_path.count())]


    def set_recent_paths(self, paths: list[str]) -> None:
        self.combobox_path.clear()
        # self.combobox_path.addItem("")
        self.combobox_path.addItems(paths)
        self.combobox_path.setCurrentIndex(0)

    # def focusOutEvent(self, event: QFocusEvent) -> None:
    #     print("focusOutEvent")
    #     self.combobox_path.hidePopup()
    #     self.is_activated = False

    #     return super().focusOutEvent(event)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        event_type = event.type()
        if isinstance(watched, QLineEdit):
            # print(f"{watched} {event}")
            if event_type == QEvent.Type.MouseButtonRelease:
                # print("mouse button release")
                if not self.is_activated:
                    self.activated()
                else:
                    self.combobox_path.hidePopup()
                    self.is_activated = False
                return True
            elif event_type in (QEvent.Type.MouseButtonPress,
                                QEvent.Type.MouseButtonDblClick):
                return True

        if event_type == QEvent.Type.FocusOut:
            focus_event: QFocusEvent = event
            if focus_event.reason() != Qt.FocusReason.PopupFocusReason:
                self.combobox_path.hidePopup()
                self.is_activated = False

            # elif event_type == QEvent.Type.MouseButtonPress:
            #     print("mouse button release")
            #     self.activated()
    # def eventFilter(self, obj, e: QEvent):
    #     print("event")
    #     if obj is self:
    #         if e.type() == QEvent.Type.MouseButtonPress:
    #             self.isPressed = True
    #         elif e.type() == QEvent.Type.MouseButtonRelease:
    #             self.isPressed = False
    #         elif e.type() == QEvent.Type.Enter:
    #             self.isHover = True
    #         elif e.type() == QEvent.Type.Leave:
    #             self.isHover = False

        return super().eventFilter(watched, event)
