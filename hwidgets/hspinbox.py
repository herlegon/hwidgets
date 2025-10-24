from string import Template
from typing import Literal
from warnings import warn
from functools import partial


from PySide6.QtCore import (
    QSize,
    Qt,
    QEvent,
    QTimer,
    QRect,
    QPoint,
    QSize,
)
from PySide6.QtGui import (
    QIcon,
    QColor, QFont,
    QPainter,
    QPixmap,
    QPainterPath,
    QPen,
)
from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QSizePolicy,
    QAbstractSpinBox,
    QStyle, QStyleOptionSpinBox
)

from .hstyle import (
    COMBOBOX_RADIUS,
    COMBOBOX_HEIGHT,
    HStyle,
    load_png_icon,
    load_qss,
)




class HSpinBoxButton(QPushButton):
    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        kind: Literal['plus', 'minus'],
        hstyle: HStyle,
        size: QSize,
    ):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.kind = kind
        radius = COMBOBOX_RADIUS
        button_width, button_height = size.toTuple()

        self.setFixedSize(button_width, button_height)
        self.setFlat(True)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setCheckable(False)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)

        states = {
            'normal': hstyle.widget_bgd,
            'hover': hstyle.hover_bgd,
            'pressed': hstyle.checked,
            'disabled': hstyle.disabled_bgd
        }

        self.pixmaps = {}
        radius += 2
        for state, bg_color in states.items():

            pixmap = QPixmap(button_width, button_height)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Draw plus button with top-right corner rounded
            path = QPainterPath()
            rect = QRect(0, 0, button_width, button_height)

            offset = 5
            if kind == "plus":
                top = rect.top()
                left = rect.left()
                bottom = rect.bottom() + 1
                right = rect.right() + 1

                path.moveTo(left, top)
                path.lineTo(right - radius - offset, top)
                path.arcTo(
                    right - radius - offset, top,
                    radius + offset, radius + offset,
                    90, -90
                )
                path.lineTo(right, bottom)
                path.lineTo(left, bottom)

            else:
                top = rect.top()
                left = rect.left()
                bottom = rect.bottom() + 1
                right = rect.right() + 1

                path.moveTo(left, top)
                path.lineTo(right, top)
                path.lineTo(right, bottom - radius//2)
                path.arcTo(right - radius, bottom - radius, radius, radius, 0, -90)
                path.lineTo(left, bottom)

            path.closeSubpath()
            painter.fillPath(path, QColor(bg_color))

            painter.setPen(QPen(QColor(hstyle.text_color)))
            font = QFont()
            font.setPixelSize(14)
            font.setBold(True)
            painter.setFont(font)

            painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
            # painter.drawText(
            #     QRect(0, 0, button_width,
            #           button_height+ (3 if kind == 'plus' else 2)
            #     ),
            #     "-" if kind == 'minus' else '+',
            #     Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,
            # )
            pen = QPen(QColor(hstyle.text_color))
            pen.setWidth(1)
            painter.setPen(pen)

            center_x = button_width // 2
            center_y = button_height // 2
            length = min(button_width, button_height) // 4

            # Draw minus sign
            if kind == 'minus':
                center_y -= 1
                painter.drawLine(center_x - length, center_y, center_x + length, center_y)

            # Draw plus sign
            else:
                painter.drawLine(center_x - length, center_y, center_x + length, center_y)  # horizontal
                painter.drawLine(center_x, center_y - length, center_x, center_y + length)  # vertical

            painter.end()

            self.pixmaps[f"{self.kind}_{state}"] = pixmap


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        # Determine current state
        if not self.isEnabled():
            state = "disabled"
        elif self.isDown():
            state = "pressed"
        elif self.underMouse():
            state = "hover"
        else:
            state = "normal"

        # Draw the correct pixmap
        pixmap = self.pixmaps[f"{self.kind}_{state}"]
        painter.drawPixmap(0, 0, pixmap)
        painter.end()



class HDoubleSpinBox(QDoubleSpinBox):

    def __init__(
        self,
        /,
        parent: QWidget | None = None,
        *,
        hstyle: HStyle,
        prefix: str | None = None,
        suffix: str | None = None,
        cleanText: str | None = None,
        decimals: int | None = None,
        minimum: float | None = None,
        maximum: float | None = None,
        singleStep: float | None = None,
        stepType: QAbstractSpinBox.StepType | None = None,
        value: float | None = 0,
    ) -> None:
        super().__init__(parent)

        self.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)

        self.lineEdit().setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFocusPolicy(Qt.StrongFocus)

        # self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)


        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(COMBOBOX_HEIGHT)


        self.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.addStretch(1)

        button_size = QSize(COMBOBOX_HEIGHT//2 + COMBOBOX_RADIUS, COMBOBOX_HEIGHT//2)
        self.plus_button = HSpinBoxButton(self, kind='plus', hstyle=hstyle, size=button_size)
        self.plus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.plus_button.setFlat(True)
        self.plus_button.setFixedSize(button_size)
        # icon_plus = QIcon()
        # icon_plus.addPixmap(
        #     load_png_icon("add_FILL0_wght500_GRAD0_opsz20.png", hstyle.text_color),
        #     QIcon.Mode.Normal, QIcon.State.Off
        # )
        # self.plus_button.setIconSize(icon_size)
        # self.plus_button.setIcon(icon_plus)
        self.plus_button.setAutoRepeat(True)

        self.minus_button = HSpinBoxButton(self, kind='minus', hstyle=hstyle, size=button_size)
        self.minus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.minus_button.setFlat(True)
        self.minus_button.setFixedSize(button_size)
        # icon_minus = QIcon()
        # icon_minus.addPixmap(
        #     load_png_icon("remove_FILL0_wght500_GRAD0_opsz20.png", hstyle.text_color),
        #     QIcon.Mode.Normal, QIcon.State.Off
        # )
        # self.minus_button.setIconSize(icon_size)
        # self.minus_button.setIcon(icon_minus)
        self.minus_button.setAutoRepeat(True)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(0)
        button_layout.setContentsMargins(0,0,0,0)
        button_layout.addWidget(
            self.plus_button, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
        button_layout.addWidget(
            self.minus_button, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )

        self.main_layout.addLayout(button_layout)
        self.plus_button.clicked.connect(self.stepUp)
        self.minus_button.clicked.connect(self.stepDown)

        self.setLayout(self.main_layout)

        qss_template = Template(load_qss("hdoublespinbox.qss"))
        qss = qss_template.substitute(
            widget_bgd=f"{hstyle.widget_bgd}",
            text_color=f"{hstyle.text_color}",
            radius=f"{COMBOBOX_RADIUS}px",
            hover_bgd=f"{hstyle.hover_bgd}",
            border_color=f"{hstyle.border}",
            disabled_bgd=f"{hstyle.disabled_bgd}",
            disabled_text=f"{hstyle.disabled_text}",
            padding_right=f"{COMBOBOX_RADIUS + COMBOBOX_HEIGHT//2}px",
            editing_border=f"{hstyle.checked}",
            selected_text=f"{hstyle.selected_text}",
            padding=f"{COMBOBOX_RADIUS}px",
            selection_bgd=f"{hstyle.selection_bgd}",
            button_width=f"{20}px",
        )
        self.setStyleSheet(qss)


        self._last_valid_value = self.value()
        self._editing = False
        self._hovered = False
        self.lineEdit().deselect()


        # # Track hover and editing state
        # self.setMouseTracking(True)
        # self.installEventFilter(self)



        self._editing = False
        self._saved_value = self.value()
        # When focus in/out happens the QLineEdit will emit signals and generate events.


        self._hovered = None
        self._pressed = None
        # self.setMouseTracking(True)

        self.lineEdit().installEventFilter(self)

        self._user_selecting = False

        self.plus_button.pressed.connect(self.event_value_changed)
        self.minus_button.pressed.connect(self.event_value_changed)
        self.plus_button.released.connect(self.event_value_changed)
        self.minus_button.released.connect(self.event_value_changed)
        self.valueChanged.connect(self.event_value_changed)



    def mousePressEvent(self, event):
        # Mark that the user is starting to select text
        if event.button() == Qt.LeftButton:
            self._user_selecting = True
        super().mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        # Once released, give a tiny delay before allowing deselection again
        if event.button() == Qt.LeftButton:
            QTimer.singleShot(150, lambda: setattr(self, "_user_selecting", False))
        super().mouseReleaseEvent(event)


    def focusInEvent(self, event):
        super().focusInEvent(event)
        # Don’t auto-select on focus
        self.lineEdit().deselect()


    def event_value_changed(self, value=0):
        """
        Deselect the text only if the user is not actively selecting it.
        """

        QTimer.singleShot(0, self.deselect_value)



    def wheelEvent(self, event):
        # Let QSpinBox handle the wheel normally first
        super().wheelEvent(event)
        # Ensure deselection after wheel-induced value change
        QTimer.singleShot(0, self.deselect_value)


    def deselect_value(self, event_type: str = '') -> None:

        line_edit = self.lineEdit()
        line_edit.blockSignals(True)
        cursor_pos = len(line_edit.text())
        line_edit.setSelection(cursor_pos, 0)
        line_edit.setCursorPosition(cursor_pos)
        line_edit.deselect()

        # line_edit.clearFocus()
        # self.setFocus()
        line_edit.blockSignals(False)

    def deselect_all(self):
        self.deselect_value()
        self.lineEdit().clearFocus()
        # self.setFocus()


    def _validate_value(self):
        try:
            self.interpretText()
        except ValueError:
            self.lineEdit().setText(str(self._last_valid_value))
        else:
            self._last_valid_value = self.value()


    def discard(self):
        self.blockSignals(True)
        self.setValue(self._last_valid_value)
        self.blockSignals(False)
        self.deselect_value()
        self._editing = False



    def keyPressEvent(self, event: QEvent) -> None:
        key = event.key()

        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if self.lineEdit().hasFocus():

                # self._validate_value()
                # self.deselect_value()
                # self.lineEdit().clearFocus()
                # self.setFocus()

                QTimer.singleShot(0, self.deselect_all)

                event.accept()
                return

        # elif key == Qt.Key.Key_Escape:
        #     if self.lineEdit().hasFocus() and self._editing:
        #         self.lineEdit().deselect()
        #         self.clearFocus()
        #         event.accept()
        #         self._editing = False
        #         return

        super().keyPressEvent(event)



    # def enterEvent(self, event):
    #     self.update()
    #     super().enterEvent(event)

    # def leaveEvent(self, event):
    #     self._hovered = None
    #     self._pressed = None
    #     self.update()
    #     super().leaveEvent(event)

    # def mouseMoveEvent(self, event):
    #     style = self.style()
    #     opt = QStyleOptionSpinBox()
    #     self.initStyleOption(opt)
    #     up_rect = style.subControlRect(QStyle.CC_SpinBox, opt, QStyle.SC_SpinBoxUp, self)
    #     down_rect = style.subControlRect(QStyle.CC_SpinBox, opt, QStyle.SC_SpinBoxDown, self)

    #     if up_rect.contains(event.pos()):
    #         self._hovered = "up"
    #     elif down_rect.contains(event.pos()):
    #         self._hovered = "down"
    #     else:
    #         self._hovered = None
    #     self.update()
    #     super().mouseMoveEvent(event)

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self._pressed = self._hovered
    #         self.update()
    #     super().mousePressEvent(event)

    # def mouseReleaseEvent(self, event):
    #     self._pressed = None
    #     self.update()
    #     super().mouseReleaseEvent(event)

    # def paintEvent(self, event):
    #     opt = QStyleOptionSpinBox()
    #     self.initStyleOption(opt)
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.Antialiasing)

    #     # Draw the base spinbox (text area)
    #     self.style().drawComplexControl(QStyle.CC_SpinBox, opt, painter, self)

    #     # Get button rectangles
    #     style = self.style()
    #     up_rect = style.subControlRect(QStyle.CC_SpinBox, opt, QStyle.SC_SpinBoxUp, self)
    #     down_rect = style.subControlRect(QStyle.CC_SpinBox, opt, QStyle.SC_SpinBoxDown, self)

    #     # Helper function for button color states
    #     def button_color(name):
    #         base = QColor("#e0e0e0")
    #         hover = QColor("#d5d5d5")
    #         press = QColor("#c0c0c0")
    #         if self._pressed == name:
    #             return press
    #         if self._hovered == name:
    #             return hover
    #         return base

    #     # Draw up button (+)
    #     painter.setBrush(button_color("up"))
    #     painter.setPen(QColor("#aaaaaa"))
    #     painter.drawRoundedRect(up_rect.adjusted(0, 0, 0, 1), 6, 6)
    #     painter.setFont(QFont("Arial", 10, QFont.Bold))
    #     painter.setPen(QColor("#333"))
    #     painter.drawText(up_rect, Qt.AlignCenter, "+")

    #     # Draw down button (–)
    #     painter.setBrush(button_color("down"))
    #     painter.setPen(QColor("#aaaaaa"))
    #     painter.drawRoundedRect(down_rect.adjusted(0, -1, 0, 0), 6, 6)
    #     painter.setFont(QFont("Arial", 12, QFont.Bold))
    #     painter.drawText(down_rect, Qt.AlignCenter, "–")

    #     painter.end()



































    # def setReadOnly(self, state: bool):
    #     super().setReadOnly(state)
    #     self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, state)


    # def setButtonSymbols(self, bs: QAbstractSpinBox.ButtonSymbols) -> None:
    #     warn(f"{__class__.__name__} Ignoring \'setButtonSymbols\'")
    #     super().setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)



    # def eventFilter(self, obj, event):
    #     le = self.lineEdit()
    #     if obj is le:
    #         # user started editing: save current value
    #         if event.type() == QEvent.Type.FocusIn:
    #             self._editing = True
    #             self._saved_value = self.value()
    #             # do not swallow event; let default handling continue
    #             return super().eventFilter(obj, event)

    #         # intercept key presses while editing
    #         if event.type() == QEvent.Type.KeyPress:
    #             key = event.key()
    #             # Enter/Return -> commit immediately
    #             if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
    #                 try:
    #                     le.interpretText = le.interpretText  # no-op to keep code style
    #                 except Exception:
    #                     pass
    #                 # use interpretText via parent widget (QAbstractSpinBox)
    #                 try:
    #                     self.interpretText()
    #                 except Exception:
    #                     # if conversion fails, revert
    #                     self.setValue(self._saved_value)
    #                 else:
    #                     self._saved_value = self.value()
    #                 # clear focus from editor so editingFinished won't double-run ambiguous logic
    #                 le.deselect()
    #                 le.clearFocus()
    #                 self.clearFocus()
    #                 self._editing = False
    #                 return True  # event handled

    #             # Escape -> revert only if editing
    #             if key == Qt.Key.Key_Escape and self._editing:
    #                 self.blockSignals(True)
    #                 self.setValue(self._saved_value)
    #                 self.blockSignals(False)
    #                 le.deselect()
    #                 le.clearFocus()
    #                 self.clearFocus()
    #                 self._editing = False
    #                 return True  # event handled

    #     return super().eventFilter(obj, event)

    # def _on_editing_finished(self):
    #     """
    #     Called when the QLineEdit editingFinished() signal fires,
    #     which happens on Enter/Return or when focus is lost.
    #     We commit the typed text to the spinbox value (interpretText()).
    #     """
    #     # If we are not in editing mode, nothing to do.
    #     # (Sometimes editingFinished can be emitted in other scenarios)
    #     if not self._editing:
    #         return

    #     try:
    #         self.interpretText()
    #     except Exception:
    #         # if user input couldn't be interpreted, restore previous value
    #         self.setValue(self._saved_value)
    #     else:
    #         # success: update saved value
    #         self._saved_value = self.value()

    #     # end editing state
    #     self._editing = False
    #     # deselect and clear focus so UI is clean
    #     le = self.lineEdit()
    #     if le:
    #         le.deselect()
    #         le.clearFocus()
    #     self.clearFocus()
































    # # def keyPressEvent(self, event: QEvent):
    # #     key = event.key()

    # #     # Validate value on Enter or Return
    # #     if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
    # #         self._validate_value()
    # #         event.accept()
    # #         return

    # #     # Revert to last valid value on Escape
    # #     elif key == Qt.Key.Key_Escape:
    # #         self._cancel_edit()
    # #         event.accept()
    # #         return

    # #     # Otherwise, normal behavior
    # #     super().keyPressEvent(event)


    #     # def __init__(...)
    #     # ...
    #     # Prevent valueChanged from selecting text
    #     # self.valueChanged.connect(self.event_value_modified)

    # # def event_value_modified(self, value: float | int) -> None:

    # #     self.blockSignals(True)
    # #     self.lineEdit().deselect()
    # #     self.lineEdit().clearFocus()
    # #     self.clearFocus()
    # #     self.blockSignals(False)

    # # def _prevent_auto_selection(self):
    # #     QTimer.singleShot(0, self._clear_selection)
    # #     QTimer.singleShot(10, self._clear_selection)

    # # def _clear_selection(self):
    # #     lineedit = self.lineEdit()
    # #     if lineedit and (lineedit.hasSelectedText() or lineedit.hasFocus()):
    # #         lineedit.deselect()
    # #         lineedit.clearFocus()
    # #         self.clearFocus()



    # def _validate_value(self):
    #     """Confirm and store the new value."""
    #     try:
    #         self.interpretText()
    #     except ValueError:
    #         self.lineEdit().setText(str(self._last_valid_value))
    #     else:
    #         self._last_valid_value = self.value()

    #     self.lineEdit().deselect()
    #     self.clearFocus()
    #     self._editing = False

    # def _cancel_edit(self):
    #     """Revert to the last valid value."""
    #     self.blockSignals(True)
    #     self.setValue(self._last_valid_value)
    #     self.blockSignals(False)
    #     self.lineEdit().deselect()
    #     self.clearFocus()
    #     self._editing = False




    # def _commit_edit(self):
    #     """Convert text → value and store it as last valid value."""
    #     try:
    #         self.interpretText()  # parse user input
    #         self._saved_value = self.value()
    #     except Exception:
    #         self.setValue(self._saved_value)
    #     self.lineEdit().deselect()
    #     self.clearFocus()


    # def _cancel_edit(self):
    #     """Revert to last saved value."""
    #     self.blockSignals(True)
    #     self.setValue(self._saved_value)
    #     self.blockSignals(False)
    #     self.lineEdit().deselect()
    #     self.clearFocus()


    # def keyPressEvent(self, event):
    #     key = event.key()

    #     # ENTER → commit new value
    #     if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
    #         if self.lineEdit().hasFocus():
    #             self._commit_edit()
    #             event.accept()
    #             return

    #     # ESCAPE → revert only if editing
    #     elif key == Qt.Key.Key_Escape:
    #         if self.lineEdit().hasFocus() and self._editing:
    #             self._cancel_edit()
    #             event.accept()
    #             return

    #     super().keyPressEvent(event)


    # def eventFilter(self, obj, event):
    #     if obj is self.lineEdit():
    #         if event.type() == QEvent.Type.FocusIn:
    #             # user started editing
    #             self._editing = True
    #             self._saved_value = self.value()

    #         elif event.type() == QEvent.Type.FocusOut:
    #             # user clicked away → commit
    #             if self._editing:
    #                 self._commit_edit()
    #             self._editing = False

    #     return super().eventFilter(obj, event)



    # # # -------------------------------
    # # # Keyboard control
    # # # -------------------------------
    # # def keyPressEvent(self, event):
    # #     key = event.key()

    # #     # Validate value on Enter or Return
    # #     if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
    # #         self._validate_value()
    # #         event.accept()
    # #         return

    # #     # Cancel edit (revert) on Escape only if hovered or editing
    # #     elif key == Qt.Key.Key_Escape:
    # #         if self._editing or self._hovered:
    # #             self._cancel_edit()
    # #         event.accept()
    # #         return

    # #     super().keyPressEvent(event)



class HSpinBox(HDoubleSpinBox):
    ...
