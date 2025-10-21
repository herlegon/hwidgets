
# coding:utf-8
from enum import Enum
from functools import update_wrapper
from typing import List, Union

from PySide6.QtCore import (QEasingCurve, QEvent, QPropertyAnimation, QObject, QModelIndex,
                          Qt, QSize, QRectF, Signal, QPoint, QTimer, QObject, QParallelAnimationGroup,
                          Property,

                          )
from PySide6.QtGui import (QAction, QIcon, QColor, QPainter, QPen, QPixmap, QRegion, QCursor, QTextCursor, QHoverEvent,
                           QFontMetrics, QKeySequence,
                           QFont,
                           QMouseEvent,

                           )
from PySide6.QtWidgets import (
    QApplication, QStyle, QGraphicsDropShadowEffect, QListWidget, QWidget, QHBoxLayout,
QListWidgetItem, QLineEdit, QTextEdit, QStyledItemDelegate, QStyleOptionViewItem,
QAbstractScrollArea,
)




class MenuAnimationType(Enum):
    """ Menu animation type """

    NONE = 0
    DROP_DOWN = 1
    PULL_UP = 2
    FADE_IN_DROP_DOWN = 3
    FADE_IN_PULL_UP = 4


class MenuItemDelegate(QStyledItemDelegate):
    """ Menu item delegate """

    def _isSeparator(self, index: QModelIndex):
        return index.model().data(index, Qt.DecorationRole) == "seperator"

    def paint(self, painter, option, index):
        if not self._isSeparator(index):
            return super().paint(painter, option, index)

        # draw seperator
        painter.save()

        c =  255
        pen = QPen(QColor(c, c, c, 25), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        rect = option.rect
        painter.drawLine(0, rect.y() + 4, rect.width() + 12, rect.y() + 4)

        painter.restore()

def getFont(fontSize=14, weight=QFont.Weight.Normal):
    """ create font

    Parameters
    ----------
    fontSize: int
        font pixel size

    weight: `QFont.Weight`
        font weight
    """
    font = QFont()
    font.setFamilies(['Segoe UI', 'Microsoft YaHei', 'PingFang SC'])
    font.setPixelSize(fontSize)
    font.setWeight(weight)
    return font



class ShortcutMenuItemDelegate(MenuItemDelegate):
    """ Shortcut key menu item delegate """

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        super().paint(painter, option, index)
        if self._isSeparator(index):
            return

        # draw shortcut key
        action = index.data(Qt.UserRole)  # type: QAction
        if not isinstance(action, QAction) or action.shortcut().isEmpty():
            return

        painter.save()

        if not option.state & QStyle.State_Enabled:
            painter.setOpacity(0.5)

        font = getFont(12)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255, 200))

        fm = QFontMetrics(font)
        shortcut = action.shortcut().toString(QKeySequence.NativeText)

        sw = fm.boundingRect(shortcut).width()
        painter.translate(option.rect.width()-sw-20, 0)

        rect = QRectF(0, option.rect.y(), sw, option.rect.height())
        painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter, shortcut)

        painter.restore()






class MenuActionListWidget(QListWidget):
    """ Menu action list widget """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._itemHeight = 32
        self._maxVisibleItems = -1  # adjust visible items according to the size of screen

        self.setViewportMargins(0, 4, 0, 4)
        self.setTextElideMode(Qt.ElideNone)
        self.setDragEnabled(False)
        self.setMouseTracking(True)
        self.setVerticalScrollMode(self.ScrollMode.ScrollPerPixel)
        self.setIconSize(QSize(16, 16))
        self.setItemDelegate(ShortcutMenuItemDelegate(self))

        self.scrollDelegate = SmoothScrollDelegate(self)
        self.setStyleSheet(
            'MenuActionListWidget{font: 14px "Segoe UI", "Microsoft YaHei", "PingFang SC"}')

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def insertItem(self, row, item):
        """ inserts menu item at the position in the list given by row """
        super().insertItem(row, item)
        self.adjustSize()

    def addItem(self, item):
        """ add menu item at the end """
        super().addItem(item)
        self.adjustSize()

    def takeItem(self, row):
        """ delete item from list """
        item = super().takeItem(row)
        self.adjustSize()
        return item

    def adjustSize(self, pos=None, aniType=MenuAnimationType.NONE):
        size = QSize()
        for i in range(self.count()):
            s = self.item(i).sizeHint()
            size.setWidth(max(s.width(), size.width()))
            size.setHeight(size.height() + s.height())

        # adjust the height of viewport
        w, h = MenuAnimationManager.make(self, aniType).availableViewSize(pos)
        self.viewport().adjustSize()

        # adjust the height of list widget
        m = self.viewportMargins()
        size += QSize(m.left()+m.right()+2, m.top()+m.bottom())
        size.setHeight(min(h, size.height()+3))
        size.setWidth(max(min(w, size.width()), self.minimumWidth()))

        if self.maxVisibleItems() > 0:
            size.setHeight(min(
                size.height(), self.maxVisibleItems() * self._itemHeight + m.top()+m.bottom() + 3))

        self.setFixedSize(size)

    def setMaxVisibleItems(self, num: int):
        """ set the maximum visible items """
        self._maxVisibleItems = num
        self.adjustSize()

    def maxVisibleItems(self):
        return self._maxVisibleItems

    def setItemHeight(self, height):
        """ set the height of item """
        for i in range(self.count()):
            item = self.item(i)
            item.setSizeHint(item.sizeHint().width(), height)

        self.adjustSize()

    def itemsHeight(self):
        """ Return the height of all items """
        return sum(self.item(i).sizeHint().height() for i in range(self.count()))




class singledispatchmethod:
    """Single-dispatch generic method descriptor.

    Supports wrapping existing descriptors and handles non-descriptor
    callables as instance methods.
    """

    def __init__(self, func):
        if not callable(func) and not hasattr(func, "__get__"):
            raise TypeError(f"{func!r} is not callable or a descriptor")

        self.dispatcher = singledispatch(func)
        self.func = func

    def register(self, cls, method=None):
        """generic_method.register(cls, func) -> func

        Registers a new implementation for the given *cls* on a *generic_method*.
        """
        return self.dispatcher.register(cls, func=method)

    def __get__(self, obj, cls=None):
        def _method(*args, **kwargs):
            if args:
                method = self.dispatcher.dispatch(args[0].__class__)
            else:
                method = self.func
                for v in kwargs.values():
                    if v.__class__ in self.dispatcher.registry:
                        method = self.dispatcher.dispatch(v.__class__)
                        if method is not self.func:
                            break

            return method.__get__(obj, cls)(*args, **kwargs)

        _method.__isabstractmethod__ = self.__isabstractmethod__
        _method.register = self.register
        update_wrapper(_method, self.func)
        return _method

    @property
    def __isabstractmethod__(self):
        return getattr(self.func, '__isabstractmethod__', False)


# class Action(QAction):
#     """ Fluent action """

#     # @singledispatchmethod
#     def __init__(self, parent: QObject = None, **kwargs):
#         super().__init__(parent, **kwargs)
#         self.materialIcon = None

#     @__init__.register
#     def _(self, text: str, parent: QObject = None, **kwargs):
#         super().__init__(text, parent, **kwargs)
#         self.materialIcon = None

#     @__init__.register
#     def _(self, icon: QIcon, text: str, parent: QObject = None, **kwargs):
#         super().__init__(icon, text, parent, **kwargs)
#         self.materialIcon = None

#     @__init__.register
#     def _(self, icon, text: str, parent: QObject = None, **kwargs):
#         super().__init__(icon.icon(), text, parent, **kwargs)
#         self.materialIcon = icon

#     def icon(self) -> QIcon:
#         # if self.materialIcon:
#         #     return Icon(self.materialIcon)

#         return super().icon()

#     def setIcon(self, icon: QIcon):
#         # if isinstance(icon):
#         self.materialIcon = icon
#         icon = icon.icon()

#         super().setIcon(icon)



class RoundMenu(QWidget):
    """ Round corner menu """

    closedSignal = Signal()

    def __init__(self, title="", parent=None):
        super().__init__(parent=parent)
        self._title = title
        self._icon = QIcon()
        self._actions = []  # type: List[QAction]
        self._subMenus = []

        self.isSubMenu = False
        self.parentMenu = None
        self.menuItem = None
        self.lastHoverItem = None
        self.lastHoverSubMenuItem = None
        self.isHideBySystem = True
        self.itemHeight = 32

        self.hBoxLayout = QHBoxLayout(self)
        self.view = MenuActionListWidget(self)

        self.aniManager = None
        self.timer = QTimer(self)

        self.__initWidgets()

    def __initWidgets(self):
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.NoDropShadowWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self.timer.setSingleShot(True)
        self.timer.setInterval(400)
        self.timer.timeout.connect(self._onShowMenuTimeOut)

        self.setShadowEffect()
        self.hBoxLayout.addWidget(self.view, 1, Qt.AlignmentFlag.AlignCenter)

        self.hBoxLayout.setContentsMargins(8, 8, 8, 20)
        # MaterialStyleSheet.MENU.apply(self)

        self.view.itemClicked.connect(self._onItemClicked)
        self.view.itemEntered.connect(self._onItemEntered)

    def setMaxVisibleItems(self, num: int):
        """ set the maximum visible items """
        self.view.setMaxVisibleItems(num)
        self.adjustSize()

    def setItemHeight(self, height):
        """ set the height of menu item """
        if height == self.itemHeight:
            return

        self.itemHeight = height
        self.view.setItemHeight(height)

    def setShadowEffect(self, blurRadius=16, offset=(0, 1), color=QColor(0, 0, 0, 90)):
        """ add shadow to dialog """
        self.shadowEffect = QGraphicsDropShadowEffect(self.view)
        self.shadowEffect.setBlurRadius(blurRadius)
        self.shadowEffect.setOffset(*offset)
        self.shadowEffect.setColor(color)
        self.view.setGraphicsEffect(None)
        self.view.setGraphicsEffect(self.shadowEffect)

    def _setParentMenu(self, parent, item):
        self.parentMenu = parent
        self.menuItem = item
        self.isSubMenu = True if parent else False

    def adjustSize(self):
        m = self.layout().contentsMargins()
        w = self.view.width() + m.left() + m.right()
        h = self.view.height() + m.top() + m.bottom()
        self.setFixedSize(w, h)

    def icon(self):
        return self._icon

    def title(self):
        return self._title

    def clear(self):
        """ clear all actions """
        for i in range(len(self._actions)-1, -1, -1):
            self.removeAction(self._actions[i])

    # def setIcon(self, icon: Union[QIcon, MaterialIconBase]):
    #     """ set the icon of menu """
    #     if isinstance(icon, MaterialIconBase):
    #         icon = Icon(icon)

    #     self._icon = icon

    def addAction(self, action: QAction):
        print("Add action")
        item = self._createActionItem(action)
        self.view.addItem(item)
        self.adjustSize()

    def _createActionItem(self, action: QAction, before=None):
        """ create menu action item  """
        if not before:
            self._actions.append(action)
        elif before in self._actions:
            index = self._actions.index(before)
            self._actions.insert(index, action)
        else:
            raise ValueError('`before` is not in the action list')

        item = QListWidgetItem(self._createItemIcon(action), action.text())
        self._adjustItemText(item, action)

        # disable item if the action is not enabled
        if not action.isEnabled():
            item.setFlags(Qt.NoItemFlags)

        item.setData(Qt.UserRole, action)
        action.setProperty('item', item)
        action.changed.connect(self._onActionChanged)
        return item

    def _hasItemIcon(self):
        return any(not i.icon().isNull() for i in self._actions+self._subMenus)

    def _adjustItemText(self, item: QListWidgetItem, action: QAction):
        """ adjust the text of item """
        # leave some space for shortcut key
        if isinstance(self.view.itemDelegate(), ShortcutMenuItemDelegate):
            sw = self._longestShortcutWidth()
            if sw:
                sw += 22
        else:
            sw = 0

        # adjust the width of item
        if not self._hasItemIcon():
            item.setText(action.text())
            w = 40 + self.view.fontMetrics().boundingRect(action.text()).width() + sw
        else:
            # add a blank character to increase space between icon and text
            item.setText(" " + action.text())
            w = 60 + self.view.fontMetrics().boundingRect(item.text()).width() + sw

        item.setSizeHint(QSize(w, self.itemHeight))
        return w

    def _longestShortcutWidth(self):
        """ longest shortcut key """
        fm = QFontMetrics(getFont(12))
        return max(fm.boundingRect(a.shortcut().toString()).width() for a in self.menuActions())

    def _createItemIcon(self, w):
        """ create the icon of menu item """
        hasIcon = self._hasItemIcon()
        icon = QIcon(MaterialIconEngine(w.icon()))

        if hasIcon and w.icon().isNull():
            pixmap = QPixmap(self.view.iconSize())
            pixmap.fill(Qt.transparent)
            icon = QIcon(pixmap)
        elif not hasIcon:
            icon = QIcon()

        return icon

    def insertAction(self, before: QAction, action: QAction):
        """ inserts action to menu, before the action before """
        if before not in self._actions:
            return

        beforeItem = before.property('item')
        if not beforeItem:
            return

        index = self.view.row(beforeItem)
        item = self._createActionItem(action, before)
        self.view.insertItem(index, item)
        self.adjustSize()

    def addActions(self, actions: List[QAction]):
        """ add actions to menu

        Parameters
        ----------
        actions: Iterable[QAction]
            menu actions
        """
        for action in actions:
            self.addAction(action)

    def insertActions(self, before: QAction, actions: List[QAction]):
        """ inserts the actions actions to menu, before the action before """
        for action in actions:
            self.insertAction(before, action)

    def removeAction(self, action: QAction):
        """ remove action from menu """
        if action not in self._actions:
            return

        index = self._actions.index(action)
        self._actions.remove(action)
        action.setProperty('item', None)
        item = self.view.takeItem(index)
        item.setData(Qt.UserRole, None)

        # delete widget
        widget = self.view.itemWidget(item)
        if widget:
            widget.deleteLater()

    def setDefaultAction(self, action: QAction):
        """ set the default action """
        if action not in self._actions:
            return

        index = self._actions.index(action)
        self.view.setCurrentRow(index)

    def addMenu(self, menu):
        """ add sub menu

        Parameters
        ----------
        menu: RoundMenu
            sub round menu
        """
        if not isinstance(menu, RoundMenu):
            raise ValueError('`menu` should be an instance of `RoundMenu`.')

        item, w = self._createSubMenuItem(menu)
        self.view.addItem(item)
        self.view.setItemWidget(item, w)
        self.adjustSize()

    def insertMenu(self, before: QAction, menu):
        """ insert menu before action `before` """
        if not isinstance(menu, RoundMenu):
            raise ValueError('`menu` should be an instance of `RoundMenu`.')

        if before not in self._actions:
            raise ValueError('`before` should be in menu action list')

        item, w = self._createSubMenuItem(menu)
        self.view.insertItem(self.view.row(before.property('item')), item)
        self.view.setItemWidget(item, w)
        self.adjustSize()

    # def _createSubMenuItem(self, menu):
    #     self._subMenus.append(menu)

    #     item = QListWidgetItem(self._createItemIcon(menu), menu.title())
    #     if not self._hasItemIcon():
    #         w = 60 + self.view.fontMetrics().boundingRect(menu.title()).width()
    #     else:
    #         # add a blank character to increase space between icon and text
    #         item.setText(" " + item.text())
    #         w = 72 + self.view.fontMetrics().boundingRect(item.text()).width()

    #     # add submenu item
    #     menu._setParentMenu(self, item)
    #     item.setSizeHint(QSize(w, self.itemHeight))
    #     item.setData(Qt.UserRole, menu)
    #     w = SubMenuItemWidget(menu, item, self)
    #     w.showMenuSig.connect(self._showSubMenu)
    #     w.resize(item.sizeHint())

    #     return item, w

    def _showSubMenu(self, item):
        """ show sub menu """
        self.lastHoverItem = item
        self.lastHoverSubMenuItem = item
        # delay 400 ms to anti-shake
        self.timer.stop()
        self.timer.start()

    def _onShowMenuTimeOut(self):
        if self.lastHoverSubMenuItem is None or not self.lastHoverItem is self.lastHoverSubMenuItem:
            return

        w = self.view.itemWidget(self.lastHoverSubMenuItem)

        if w.menu.parentMenu.isHidden():
            return

        pos = w.mapToGlobal(QPoint(w.width()+5, -5))
        w.menu.exec(pos)

    def addSeparator(self):
        """ add seperator to menu """
        m = self.view.viewportMargins()
        w = self.view.width()-m.left()-m.right()

        # add separator to list widget
        item = QListWidgetItem(self.view)
        item.setFlags(Qt.NoItemFlags)
        item.setSizeHint(QSize(w, 9))
        self.view.addItem(item)
        item.setData(Qt.DecorationRole, "seperator")
        self.adjustSize()

    def _onItemClicked(self, item):
        action = item.data(Qt.UserRole)
        if action not in self._actions or not action.isEnabled():
            return

        self._hideMenu(False)

        if not self.isSubMenu:
            action.trigger()
            return

        # close parent menu
        self._closeParentMenu()
        action.trigger()

    def _closeParentMenu(self):
        menu = self
        while menu:
            menu.close()
            menu = menu.parentMenu

    def _onItemEntered(self, item):
        self.lastHoverItem = item
        if not isinstance(item.data(Qt.UserRole), RoundMenu):
            return

        self._showSubMenu(item)

    def _hideMenu(self, isHideBySystem=False):
        self.isHideBySystem = isHideBySystem
        self.view.clearSelection()
        if self.isSubMenu:
            self.hide()
        else:
            self.close()

    def hideEvent(self, e):
        if self.isHideBySystem and self.isSubMenu:
            self._closeParentMenu()

        self.isHideBySystem = True
        e.accept()

    def closeEvent(self, e):
        e.accept()
        self.closedSignal.emit()
        self.view.clearSelection()

    def menuActions(self):
        return self._actions

    def mousePressEvent(self, e):
        w = self.childAt(e.pos())
        if (w is not self.view) and (not self.view.isAncestorOf(w)):
            self._hideMenu(True)

    def mouseMoveEvent(self, e):
        if not self.isSubMenu:
            return

        # hide submenu when mouse moves out of submenu item
        pos = e.globalPos()
        view = self.parentMenu.view

        # get the rect of menu item
        margin = view.viewportMargins()
        rect = view.visualItemRect(self.menuItem).translated(view.mapToGlobal(QPoint()))
        rect = rect.translated(margin.left(), margin.top()+2)
        if self.parentMenu.geometry().contains(pos) and not rect.contains(pos) and \
                not self.geometry().contains(pos):
            view.clearSelection()
            self._hideMenu(False)

    def _onActionChanged(self):
        """ action changed slot """
        action = self.sender()  # type: QAction
        item = action.property('item')  # type: QListWidgetItem
        item.setIcon(self._createItemIcon(action))

        self._adjustItemText(item, action)

        if action.isEnabled():
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        else:
            item.setFlags(Qt.NoItemFlags)

        self.view.adjustSize()
        self.adjustSize()

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        """ show menu

        Parameters
        ----------
        pos: QPoint
            pop-up position

        ani: bool
            Whether to show pop-up animation

        aniType: MenuAnimationType
            menu animation type
        """
        #if self.isVisible():
        #    aniType = MenuAnimationType.NONE

        self.aniManager = MenuAnimationManager.make(self, aniType)
        self.aniManager.exec(pos)

        self.show()

        if self.isSubMenu:
            self.menuItem.setSelected(True)

    def exec_(self, pos: QPoint, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        """ show menu

        Parameters
        ----------
        pos: QPoint
            pop-up position

        ani: bool
            Whether to show pop-up animation

        aniType: MenuAnimationType
            menu animation type
        """
        self.exec(pos, ani, aniType)







class SmoothScrollDelegate(QObject):
    """ Smooth scroll delegate """

    def __init__(self, parent: QAbstractScrollArea, useAni=False):
        """
        Parameters
        ----------
        parent: QAbstractScrollArea
            the scrolling area being delegated

        useAni: bool
            whether to use `QPropertyAnimation` to achieve smooth scrolling
        """
        super().__init__(parent)
        self.useAni = useAni
        self.vScrollBar = SmoothScrollBar(Qt.Orientation.Vertical, parent)
        self.hScrollBar = SmoothScrollBar(Qt.Orientation.Horizontal, parent)
        self.verticalSmoothScroll = SmoothScroll(parent, Qt.Orientation.Vertical)
        self.horizonSmoothScroll = SmoothScroll(parent, Qt.Orientation.Horizontal)

        if isinstance(parent, QAbstractItemView):
            parent.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
            parent.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        if isinstance(parent, QListView):
            parent.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            parent.horizontalScrollBar().setStyleSheet("QScrollBar:horizontal{height: 0px}")

        parent.viewport().installEventFilter(self)
        parent.setVerticalScrollBarPolicy = self.setVerticalScrollBarPolicy
        parent.setHorizontalScrollBarPolicy = self.setHorizontalScrollBarPolicy

    def eventFilter(self, obj, e: QEvent):
        if e.type() == QEvent.Type.Wheel:
            if e.angleDelta().y() != 0:
                if not self.useAni:
                    self.verticalSmoothScroll.wheelEvent(e)
                else:
                    self.vScrollBar.scrollValue(-e.angleDelta().y())
            else:
                if not self.useAni:
                    self.horizonSmoothScroll.wheelEvent(e)
                else:
                    self.hScrollBar.scrollValue(-e.angleDelta().x())

            e.setAccepted(True)
            return True

        return super().eventFilter(obj, e)

    def setVerticalScrollBarPolicy(self, policy):
        QAbstractScrollArea.setVerticalScrollBarPolicy(self.parent(), Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.vScrollBar.setForceHidden(policy == Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def setHorizontalScrollBarPolicy(self, policy):
        QAbstractScrollArea.setHorizontalScrollBarPolicy(self.parent(), Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.hScrollBar.setForceHidden(policy == Qt.ScrollBarPolicy.ScrollBarAlwaysOff)





class ScrollBar(QWidget):
    """ Fluent scroll bar """

    rangeChanged = Signal(tuple)
    valueChanged = Signal(int)
    sliderPressed = Signal()
    sliderReleased = Signal()
    sliderMoved = Signal()

    def __init__(self, orient: Qt.Orientation, parent: QAbstractScrollArea):
        super().__init__(parent)
        self.groove = ScrollBarGroove(orient, self)
        self.handle = ScrollBarHandle(orient, self)
        self.timer = QTimer(self)

        self._orientation = orient
        self._singleStep = 1
        self._pageStep = 50
        self._padding = 14

        self._minimum = 0
        self._maximum = 0
        self._value = 0

        self._isPressed = False
        self._isEnter = False
        self._isExpanded = False
        self._pressedPos = QPoint()
        self._isForceHidden = False

        if orient == Qt.Orientation.Vertical:
            self.partnerBar = parent.verticalScrollBar()
            QAbstractScrollArea.setVerticalScrollBarPolicy(parent, Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        else:
            self.partnerBar = parent.horizontalScrollBar()
            QAbstractScrollArea.setHorizontalScrollBarPolicy(parent, Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.__initWidget(parent)

    def __initWidget(self, parent):
        self.groove.upButton.clicked.connect(self._onPageUp)
        self.groove.downButton.clicked.connect(self._onPageDown)
        self.groove.opacityAni.valueChanged.connect(self._onOpacityAniValueChanged)

        self.partnerBar.rangeChanged.connect(self.setRange)
        self.partnerBar.valueChanged.connect(self._onValueChanged)
        self.valueChanged.connect(self.partnerBar.setValue)

        parent.installEventFilter(self)

        self.setRange(self.partnerBar.minimum(), self.partnerBar.maximum())
        self.setVisible(self.maximum() > 0 and not self._isForceHidden)
        self._adjustPos(self.parent().size())

    def _onPageUp(self):
        self.setValue(self.value() - self.pageStep())

    def _onPageDown(self):
        self.setValue(self.value() + self.pageStep())

    def _onValueChanged(self, value):
        self.val = value

    def value(self):
        return self._value

    @Property(int, notify=valueChanged)
    def val(self):
        return self._value

    @val.setter
    def val(self, value: int):
        if value == self.value():
            return

        value = max(self.minimum(), min(value, self.maximum()))
        self._value = value
        self.valueChanged.emit(value)

        # adjust the position of handle
        self._adjustHandlePos()

    def minimum(self):
        return self._minimum

    def maximum(self):
        return self._maximum

    def orientation(self):
        return self._orientation

    def pageStep(self):
        return self._pageStep

    def singleStep(self):
        return self._singleStep

    def isSliderDown(self):
        return self._isPressed

    def setValue(self, value: int):
        self.val = value

    def setMinimum(self, min: int):
        if min == self.minimum():
            return

        self._minimum = min
        self.rangeChanged.emit((min, self.maximum()))

    def setMaximum(self, max: int):
        if max == self.maximum():
            return

        self._maximum = max
        self.rangeChanged.emit((self.minimum(), max))

    def setRange(self, min: int, max: int):
        if min > max or (min == self.minimum() and max == self.maximum()):
            return

        self.setMinimum(min)
        self.setMaximum(max)

        self._adjustHandleSize()
        self._adjustHandlePos()
        self.setVisible(max > 0 and not self._isForceHidden)

        self.rangeChanged.emit((min, max))

    def setPageStep(self, step: int):
        if step >= 1:
            self._pageStep = step

    def setSingleStep(self, step: int):
        if step >= 1:
            self._singleStep = step

    def setSliderDown(self, isDown: bool):
        self._isPressed = True
        if isDown:
            self.sliderPressed.emit()
        else:
            self.sliderReleased.emit()

    def expand(self):
        """ expand scroll bar """
        if self._isExpanded or not self.isEnter:
            return

        self._isExpanded = True
        self.groove.fadeIn()

    def collapse(self):
        """ collapse scroll bar """
        if not self._isExpanded or self.isEnter:
            return

        self._isExpanded = False
        self.groove.fadeOut()

    def enterEvent(self, e):
        self.isEnter = True
        self.timer.stop()
        self.timer.singleShot(200, self.expand)

    def leaveEvent(self, e):
        self.isEnter = False
        self.timer.stop()
        self.timer.singleShot(200, self.collapse)

    def eventFilter(self, obj, e: QEvent):
        if obj is not self.parent():
            return super().eventFilter(obj, e)

        # adjust the position of slider
        if e.type() == QEvent.Type.Resize:
            self._adjustPos(e.size())

        return super().eventFilter(obj, e)

    def resizeEvent(self, e):
        self.groove.resize(self.size())

    def mousePressEvent(self, e: QMouseEvent):
        super().mousePressEvent(e)
        self._isPressed = True
        self._pressedPos = e.pos()

        if self.childAt(e.pos()) is self.handle or not self._isSlideResion(e.pos()):
            return

        if self.orientation() == Qt.Orientation.Vertical:
            if e.pos().y() > self.handle.geometry().bottom():
                value = e.pos().y() - self.handle.height() - self._padding
            else:
                value = e.pos().y() - self._padding
        else:
            if e.pos().x() > self.handle.geometry().right():
                value = e.pos().x() - self.handle.width() - self._padding
            else:
                value = e.pos().x() - self._padding

        self.setValue(int(value / max(self._slideLength(), 1) * self.maximum()))
        self.sliderPressed.emit()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self._isPressed = False
        self.sliderReleased.emit()

    def mouseMoveEvent(self, e: QMouseEvent):
        if self.orientation() == Qt.Orientation.Vertical:
            dv = e.pos().y() - self._pressedPos.y()
        else:
            dv = e.pos().x() - self._pressedPos.x()

        # don't use `self.setValue()`, because it could be reimplemented
        dv = int(dv / max(self._slideLength(), 1) * (self.maximum() - self.minimum()))
        ScrollBar.setValue(self, self.value() + dv)

        self._pressedPos = e.pos()
        self.sliderMoved.emit()

    def _adjustPos(self, size):
        if self.orientation() == Qt.Orientation.Vertical:
            self.resize(12, size.height() - 2)
            self.move(size.width() - 13, 1)
        else:
            self.resize(size.width() - 2, 12)
            self.move(1, size.height() - 13)

    def _adjustHandleSize(self):
        p = self.parent()
        if self.orientation() == Qt.Orientation.Vertical:
            total = self.maximum() - self.minimum() + p.height()
            s = int(self._grooveLength() * p.height() / max(total, 1))
            self.handle.setFixedHeight(max(30, s))
        else:
            total = self.maximum() - self.minimum() + p.width()
            s = int(self._grooveLength() * p.width() / max(total, 1))
            self.handle.setFixedWidth(max(30, s))

    def _adjustHandlePos(self):
        total = max(self.maximum() - self.minimum(), 1)
        delta = int(self.value() / total * self._slideLength())

        if self.orientation() == Qt.Orientation.Vertical:
            x = self.width() - self.handle.width() - 3
            self.handle.move(x, self._padding + delta)
        else:
            y = self.height() - self.handle.height() - 3
            self.handle.move(self._padding + delta, y)

    def _grooveLength(self):
        if self.orientation() == Qt.Orientation.Vertical:
            return self.height() - 2 * self._padding

        return self.width() - 2 * self._padding

    def _slideLength(self):
        if self.orientation() == Qt.Orientation.Vertical:
            return self._grooveLength() - self.handle.height()

        return self._grooveLength() - self.handle.width()

    def _isSlideResion(self, pos: QPoint):
        if self.orientation() == Qt.Orientation.Vertical:
            return self._padding <= pos.y() <= self.height() - self._padding

        return self._padding <= pos.x() <= self.width() - self._padding

    def _onOpacityAniValueChanged(self):
        opacity = self.groove.opacityEffect.opacity()
        if self.orientation() == Qt.Orientation.Vertical:
            self.handle.setFixedWidth(int(3 + opacity * 3))
        else:
            self.handle.setFixedHeight(int(3 + opacity * 3))

        self._adjustHandlePos()

    def setForceHidden(self, isHidden: bool):
        """ whether to force the scrollbar to be hidden """
        self._isForceHidden = isHidden
        self.setVisible(self.maximum() > 0 and not isHidden)

    def wheelEvent(self, e):
        QApplication.sendEvent(self.parent().viewport(), e)



class SmoothScrollBar(ScrollBar):
    """ Smooth scroll bar """

    def __init__(self, orient: Qt.Orientation, parent):
        super().__init__(orient, parent)
        self.duration = 500
        self.ani = QPropertyAnimation()
        self.ani.setTargetObject(self)
        self.ani.setPropertyName(b"val")
        self.ani.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.ani.setDuration(self.duration)

        self.__value = self.value()

    def setValue(self, value):
        if value == self.value():
            return

        # stop running animation
        self.ani.stop()

        # adjust the duration
        dv = abs(value - self.value())
        if dv < 50:
            self.ani.setDuration(int(self.duration * dv / 70))
        else:
            self.ani.setDuration(self.duration)

        self.ani.setStartValue(self.value())
        self.ani.setEndValue(value)
        self.ani.start()

    def scrollValue(self, value):
        """ scroll the specified distance """
        self.__value += value
        self.__value = max(self.minimum(), self.__value)
        self.__value = min(self.maximum(), self.__value)
        self.setValue(self.__value)

    def scrollTo(self, value):
        """ scroll to the specified position """
        self.__value = value
        self.__value = max(self.minimum(), self.__value)
        self.__value = min(self.maximum(), self.__value)
        self.setValue(self.__value)

    def resetValue(self, value):
        self.__value = value

    def mousePressEvent(self, e):
        self.ani.stop()
        super().mousePressEvent(e)
        self.__value = self.value()

    def mouseMoveEvent(self, e):
        self.ani.stop()
        super().mouseMoveEvent(e)
        self.__value = self.value()

    def setScrollAnimation(self, duration, easing=QEasingCurve.Type.OutCubic):
        """ set scroll animation

        Parameters
        ----------
        duration: int
            scroll duration

        easing: QEasingCurve
            animation type
        """
        self.duration = duration
        self.ani.setDuration(duration)
        self.ani.setEasingCurve(easing)




class MenuAnimationManager(QObject):
    """ Menu animation manager """

    managers = {}

    def __init__(self, menu: RoundMenu):
        super().__init__()
        self.menu = menu
        self.ani = QPropertyAnimation(menu, b'pos', menu)

        self.ani.setDuration(250)
        self.ani.setEasingCurve(QEasingCurve.OutQuad)
        self.ani.valueChanged.connect(self._onValueChanged)
        self.ani.valueChanged.connect(self._updateMenuViewport)

    def _onValueChanged(self):
        pass

    def availableViewSize(self, pos: QPoint):
        """ Return the available size of view """
        ss = QApplication.screenAt(QCursor.pos()).availableGeometry()
        w, h = ss.width() - 100, ss.height() - 100
        return w, h

    def _updateMenuViewport(self):
        self.menu.view.viewport().update()
        self.menu.view.setAttribute(Qt.WidgetAttribute.WA_UnderMouse, True)
        e = QHoverEvent(QEvent.HoverEnter, QPoint(), QPoint(1, 1))
        QApplication.sendEvent(self.menu.view, e)

    def _endPosition(self, pos):
        m = self.menu
        rect = QApplication.screenAt(QCursor.pos()).availableGeometry()
        w, h = m.width() + 5, m.sizeHint().height()
        x = min(pos.x() - m.layout().contentsMargins().left(), rect.right() - w)
        y = min(pos.y() - 4, rect.bottom() - h)

        return QPoint(x, y)

    def _menuSize(self):
        m = self.menu.layout().contentsMargins()
        w = self.menu.view.width() + m.left() + m.right() + 120
        h = self.menu.view.height() + m.top() + m.bottom() + 20
        return w, h

    def exec(self, pos: QPoint):
        pass

    @classmethod
    def register(cls, name):
        """ register menu animation manager

        Parameters
        ----------
        name: Any
            the name of manager, it should be unique
        """
        def wrapper(Manager):
            if name not in cls.managers:
                cls.managers[name] = Manager

            return Manager

        return wrapper

    @classmethod
    def make(cls, menu: RoundMenu, aniType: MenuAnimationType):
        if aniType not in cls.managers:
            raise ValueError(f'`{aniType}` is an invalid menu animation type.')

        return cls.managers[aniType](menu)




class IndicatorMenuItemDelegate(MenuItemDelegate):
    """ Menu item delegate with indicator """

    def paint(self, painter: QPainter, option, index):
        super().paint(painter, option, index)
        if not option.state & QStyle.State_Selected:
            return

        painter.save()
        painter.setRenderHints(
            QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(127,127,127))
        painter.drawRoundedRect(-3, option.rect.y(), 6, option.rect.height(), 3, 3)

        painter.restore()
