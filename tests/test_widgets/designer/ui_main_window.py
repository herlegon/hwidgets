# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QButtonGroup, QCheckBox,
    QComboBox, QDoubleSpinBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPlainTextEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

from typing import Type
from hwidgets import (
    HButton,
    HCheckBox,
    HComboBox,
    HDoubleSpinBox,
    HFrame,
    HGroupBox,
    HLabel,
    HLineEdit,
    HPlainTextEdit,
    HRadioButton,
    HScrollBar,
    HSpinBox,
    HButtonGroup,
    HComment,
    HDescription,
    HDivider,
    HHorizontalDivider,
    HIndeterminateCircularProgress,
    HIndeterminateProgress,
    HProgress,
    HRadialProgress,
    HStrongButton,
    HSubtitle,
    HSwitch,
    HTitle,
    HVerticalDivider,
    Theme,
)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, theme: Type[Theme]):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1600, 741)
        MainWindow.setMinimumSize(QSize(1600, 0))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.h_frame = HFrame(self.centralwidget, theme=theme)
        self.h_frame.setObjectName(u"h_frame")
        self.h_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.h_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.h_frame)
        self.horizontalLayout_10.setSpacing(12)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(18, 18, 18, 18)
        self.main_layout = QVBoxLayout()
        self.main_layout.setObjectName(u"main_layout")
        self.titles_layout = QVBoxLayout()
        self.titles_layout.setObjectName(u"titles_layout")
        self.h_title = HTitle(self.h_frame, theme=theme)
        self.h_title.setObjectName(u"h_title")

        self.titles_layout.addWidget(self.h_title)

        self.h_title_icon = HTitle(self.h_frame, theme=theme)
        self.h_title_icon.setObjectName(u"h_title_icon")
        self.h_title_icon.setPixmap(QPixmap(u"../../hwidgets/icons/gpu.png"))

        self.titles_layout.addWidget(self.h_title_icon)


        self.main_layout.addLayout(self.titles_layout)

        self.text_layout = QVBoxLayout()
        self.text_layout.setObjectName(u"text_layout")
        self.h_subtitles = HSubtitle(self.h_frame, theme=theme)
        self.h_subtitles.setObjectName(u"h_subtitles")

        self.text_layout.addWidget(self.h_subtitles)

        self.h_description = HDescription(self.h_frame, theme=theme)
        self.h_description.setObjectName(u"h_description")
        self.h_description.setWordWrap(True)

        self.text_layout.addWidget(self.h_description)

        self.h_comment_bold = HComment(self.h_frame, theme=theme)
        self.h_comment_bold.setObjectName(u"h_comment_bold")
        self.h_comment_bold.setWordWrap(True)

        self.text_layout.addWidget(self.h_comment_bold)

        self.h_comment_italic = HComment(self.h_frame, theme=theme)
        self.h_comment_italic.setObjectName(u"h_comment_italic")
        self.h_comment_italic.setWordWrap(True)

        self.text_layout.addWidget(self.h_comment_italic)

        self.h_comment_small_italic = HComment(self.h_frame, theme=theme)
        self.h_comment_small_italic.setObjectName(u"h_comment_small_italic")
        self.h_comment_small_italic.setWordWrap(True)

        self.text_layout.addWidget(self.h_comment_small_italic)


        self.main_layout.addLayout(self.text_layout)

        self.labels_layout = QHBoxLayout()
        self.labels_layout.setObjectName(u"labels_layout")
        self.h_label = HLabel(self.h_frame, theme=theme)
        self.h_label.setObjectName(u"h_label")

        self.labels_layout.addWidget(self.h_label)

        self.h_label_disabled = HLabel(self.h_frame, theme=theme)
        self.h_label_disabled.setObjectName(u"h_label_disabled")
        self.h_label_disabled.setEnabled(False)

        self.labels_layout.addWidget(self.h_label_disabled)


        self.main_layout.addLayout(self.labels_layout)

        self.h_divider = HDivider(self.h_frame, theme=theme)
        self.h_divider.setObjectName(u"h_divider")
        self.h_divider.setFrameShape(QFrame.Shape.HLine)
        self.h_divider.setFrameShadow(QFrame.Shadow.Sunken)

        self.main_layout.addWidget(self.h_divider)

        self.checkbox_layout = QHBoxLayout()
        self.checkbox_layout.setObjectName(u"checkbox_layout")
        self.h_checkbox = HCheckBox(self.h_frame, theme=theme)
        self.h_checkbox.setObjectName(u"h_checkbox")

        self.checkbox_layout.addWidget(self.h_checkbox)

        self.h_checkbox_clicked = HCheckBox(self.h_frame, theme=theme)
        self.h_checkbox_clicked.setObjectName(u"h_checkbox_clicked")
        self.h_checkbox_clicked.setChecked(True)

        self.checkbox_layout.addWidget(self.h_checkbox_clicked)

        self.h_checkbox_disabled = HCheckBox(self.h_frame, theme=theme)
        self.h_checkbox_disabled.setObjectName(u"h_checkbox_disabled")
        self.h_checkbox_disabled.setEnabled(False)

        self.checkbox_layout.addWidget(self.h_checkbox_disabled)

        self.h_checkbox_disabled_clicked = HCheckBox(self.h_frame, theme=theme)
        self.h_checkbox_disabled_clicked.setObjectName(u"h_checkbox_disabled_clicked")
        self.h_checkbox_disabled_clicked.setEnabled(False)
        self.h_checkbox_disabled_clicked.setChecked(True)

        self.checkbox_layout.addWidget(self.h_checkbox_disabled_clicked)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.checkbox_layout.addItem(self.horizontalSpacer_3)

        self.h_switch = HSwitch(self.h_frame, theme=theme)
        self.h_switch.setObjectName(u"h_switch")

        self.checkbox_layout.addWidget(self.h_switch)

        self.h_switch_checked = HSwitch(self.h_frame, theme=theme)
        self.h_switch_checked.setObjectName(u"h_switch_checked")
        self.h_switch_checked.setChecked(True)

        self.checkbox_layout.addWidget(self.h_switch_checked)

        self.h_switch_disabled = HSwitch(self.h_frame, theme=theme)
        self.h_switch_disabled.setObjectName(u"h_switch_disabled")
        self.h_switch_disabled.setEnabled(False)
        self.h_switch_disabled.setCheckable(True)

        self.checkbox_layout.addWidget(self.h_switch_disabled)

        self.h_switch_disabled_checked = HSwitch(self.h_frame, theme=theme)
        self.h_switch_disabled_checked.setObjectName(u"h_switch_disabled_checked")
        self.h_switch_disabled_checked.setEnabled(False)
        self.h_switch_disabled_checked.setChecked(True)

        self.checkbox_layout.addWidget(self.h_switch_disabled_checked)


        self.main_layout.addLayout(self.checkbox_layout)

        self.radio_layout = QHBoxLayout()
        self.radio_layout.setObjectName(u"radio_layout")
        self.h_radiobutton_enabled_off = HRadioButton(self.h_frame, theme=theme)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.h_radiobutton_enabled_off)
        self.h_radiobutton_enabled_off.setObjectName(u"h_radiobutton_enabled_off")
        self.h_radiobutton_enabled_off.setChecked(False)

        self.radio_layout.addWidget(self.h_radiobutton_enabled_off)

        self.h_radiobutton_enabled_on = HRadioButton(self.h_frame, theme=theme)
        self.buttonGroup.addButton(self.h_radiobutton_enabled_on)
        self.h_radiobutton_enabled_on.setObjectName(u"h_radiobutton_enabled_on")
        self.h_radiobutton_enabled_on.setChecked(True)

        self.radio_layout.addWidget(self.h_radiobutton_enabled_on)

        self.h_radiobutton_disabled_on = HRadioButton(self.h_frame, theme=theme)
        self.h_radiobutton_disabled_on.setObjectName(u"h_radiobutton_disabled_on")
        self.h_radiobutton_disabled_on.setEnabled(False)
        self.h_radiobutton_disabled_on.setChecked(False)

        self.radio_layout.addWidget(self.h_radiobutton_disabled_on)

        self.h_radiobutton_disabled_off = HRadioButton(self.h_frame, theme=theme)
        self.h_radiobutton_disabled_off.setObjectName(u"h_radiobutton_disabled_off")
        self.h_radiobutton_disabled_off.setEnabled(False)

        self.radio_layout.addWidget(self.h_radiobutton_disabled_off)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.radio_layout.addItem(self.horizontalSpacer)


        self.main_layout.addLayout(self.radio_layout)

        self.lineedit_layout = QHBoxLayout()
        self.lineedit_layout.setObjectName(u"lineedit_layout")
        self.h_lineedit_editable = HLineEdit(self.h_frame, theme=theme)
        self.h_lineedit_editable.setObjectName(u"h_lineedit_editable")
        self.h_lineedit_editable.setClearButtonEnabled(False)

        self.lineedit_layout.addWidget(self.h_lineedit_editable)

        self.h_lineedit_editable_clear_button = HLineEdit(self.h_frame, theme=theme)
        self.h_lineedit_editable_clear_button.setObjectName(u"h_lineedit_editable_clear_button")
        self.h_lineedit_editable_clear_button.setClearButtonEnabled(True)

        self.lineedit_layout.addWidget(self.h_lineedit_editable_clear_button)

        self.h_lineedit_disabled = HLineEdit(self.h_frame, theme=theme)
        self.h_lineedit_disabled.setObjectName(u"h_lineedit_disabled")
        self.h_lineedit_disabled.setEnabled(False)
        self.h_lineedit_disabled.setClearButtonEnabled(True)

        self.lineedit_layout.addWidget(self.h_lineedit_disabled)

        self.h_lineedit_read_only = HLineEdit(self.h_frame, theme=theme)
        self.h_lineedit_read_only.setObjectName(u"h_lineedit_read_only")
        self.h_lineedit_read_only.setReadOnly(True)
        self.h_lineedit_read_only.setClearButtonEnabled(True)

        self.lineedit_layout.addWidget(self.h_lineedit_read_only)


        self.main_layout.addLayout(self.lineedit_layout)

        self.combobox_layout = QHBoxLayout()
        self.combobox_layout.setObjectName(u"combobox_layout")
        self.h_combobox_rw = HComboBox(self.h_frame, theme=theme)
        self.h_combobox_rw.setObjectName(u"h_combobox_rw")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.h_combobox_rw.sizePolicy().hasHeightForWidth())
        self.h_combobox_rw.setSizePolicy(sizePolicy)
        self.h_combobox_rw.setMaximumSize(QSize(300, 16777215))
        self.h_combobox_rw.setEditable(True)

        self.combobox_layout.addWidget(self.h_combobox_rw)

        self.h_combobox_ro = HComboBox(self.h_frame, theme=theme)
        self.h_combobox_ro.setObjectName(u"h_combobox_ro")
        sizePolicy.setHeightForWidth(self.h_combobox_ro.sizePolicy().hasHeightForWidth())
        self.h_combobox_ro.setSizePolicy(sizePolicy)
        self.h_combobox_ro.setMaximumSize(QSize(300, 16777215))

        self.combobox_layout.addWidget(self.h_combobox_ro)

        self.h_combobox_disabled = HComboBox(self.h_frame, theme=theme)
        self.h_combobox_disabled.setObjectName(u"h_combobox_disabled")
        self.h_combobox_disabled.setEnabled(False)
        self.h_combobox_disabled.setEditable(True)

        self.combobox_layout.addWidget(self.h_combobox_disabled)


        self.main_layout.addLayout(self.combobox_layout)

        self.plaintextedit_layout = QHBoxLayout()
        self.plaintextedit_layout.setObjectName(u"plaintextedit_layout")
        self.h_plaintextedit_editable = HPlainTextEdit(self.h_frame, theme=theme)
        self.h_plaintextedit_editable.setObjectName(u"h_plaintextedit_editable")
        self.h_plaintextedit_editable.setMaximumSize(QSize(100, 150))

        self.plaintextedit_layout.addWidget(self.h_plaintextedit_editable)

        self.h_plaintextedit_editable_vscrollbar = HPlainTextEdit(self.h_frame, theme=theme)
        self.h_plaintextedit_editable_vscrollbar.setObjectName(u"h_plaintextedit_editable_vscrollbar")
        self.h_plaintextedit_editable_vscrollbar.setMaximumSize(QSize(100, 150))

        self.plaintextedit_layout.addWidget(self.h_plaintextedit_editable_vscrollbar)

        self.h_plaintextedit_editable_scrollbars = HPlainTextEdit(self.h_frame, theme=theme)
        self.h_plaintextedit_editable_scrollbars.setObjectName(u"h_plaintextedit_editable_scrollbars")
        self.h_plaintextedit_editable_scrollbars.setMaximumSize(QSize(150, 150))
        self.h_plaintextedit_editable_scrollbars.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)

        self.plaintextedit_layout.addWidget(self.h_plaintextedit_editable_scrollbars)

        self.h_plaintextedit_readonly = HPlainTextEdit(self.h_frame, theme=theme)
        self.h_plaintextedit_readonly.setObjectName(u"h_plaintextedit_readonly")
        self.h_plaintextedit_readonly.setMaximumSize(QSize(100, 150))
        self.h_plaintextedit_readonly.setReadOnly(True)

        self.plaintextedit_layout.addWidget(self.h_plaintextedit_readonly)

        self.h_plaintextedit_disabled = HPlainTextEdit(self.h_frame, theme=theme)
        self.h_plaintextedit_disabled.setObjectName(u"h_plaintextedit_disabled")
        self.h_plaintextedit_disabled.setEnabled(False)
        self.h_plaintextedit_disabled.setMaximumSize(QSize(100, 150))

        self.plaintextedit_layout.addWidget(self.h_plaintextedit_disabled)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.plaintextedit_layout.addItem(self.horizontalSpacer_6)


        self.main_layout.addLayout(self.plaintextedit_layout)

        self.h_spinbox_layout = QHBoxLayout()
        self.h_spinbox_layout.setObjectName(u"h_spinbox_layout")
        self.h_spinbox_no_button = HSpinBox(self.h_frame, theme=theme)
        self.h_spinbox_no_button.setObjectName(u"h_spinbox_no_button")
        self.h_spinbox_no_button.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.h_spinbox_no_button.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.h_spinbox_layout.addWidget(self.h_spinbox_no_button)

        self.h_spinbox_rw = HSpinBox(self.h_frame, theme=theme)
        self.h_spinbox_rw.setObjectName(u"h_spinbox_rw")
        self.h_spinbox_rw.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.h_spinbox_rw.setMinimum(10)

        self.h_spinbox_layout.addWidget(self.h_spinbox_rw)

        self.h_spinbox_ro = HSpinBox(self.h_frame, theme=theme)
        self.h_spinbox_ro.setObjectName(u"h_spinbox_ro")
        self.h_spinbox_ro.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.h_spinbox_ro.setReadOnly(True)

        self.h_spinbox_layout.addWidget(self.h_spinbox_ro)

        self.h_spinbox_disabled = HSpinBox(self.h_frame, theme=theme)
        self.h_spinbox_disabled.setObjectName(u"h_spinbox_disabled")
        self.h_spinbox_disabled.setEnabled(False)
        self.h_spinbox_disabled.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.h_spinbox_layout.addWidget(self.h_spinbox_disabled)

        self.rlg_spinbox_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.h_spinbox_layout.addItem(self.rlg_spinbox_spacer)

        self.h_doublespinbox_nobutton = HDoubleSpinBox(self.h_frame, theme=theme)
        self.h_doublespinbox_nobutton.setObjectName(u"h_doublespinbox_nobutton")
        self.h_doublespinbox_nobutton.setFrame(True)
        self.h_doublespinbox_nobutton.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.h_doublespinbox_nobutton.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.h_spinbox_layout.addWidget(self.h_doublespinbox_nobutton)

        self.h_doublespinbox_rw = HDoubleSpinBox(self.h_frame, theme=theme)
        self.h_doublespinbox_rw.setObjectName(u"h_doublespinbox_rw")
        self.h_doublespinbox_rw.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.h_doublespinbox_rw.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.h_doublespinbox_rw.setProperty(u"showGroupSeparator", False)
        self.h_doublespinbox_rw.setDecimals(1)
        self.h_doublespinbox_rw.setMinimum(10.000000000000000)

        self.h_spinbox_layout.addWidget(self.h_doublespinbox_rw)

        self.h_doublespinbox_ro = HDoubleSpinBox(self.h_frame, theme=theme)
        self.h_doublespinbox_ro.setObjectName(u"h_doublespinbox_ro")
        self.h_doublespinbox_ro.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.h_doublespinbox_ro.setReadOnly(True)

        self.h_spinbox_layout.addWidget(self.h_doublespinbox_ro)

        self.h_doublespinbox_disabled = HDoubleSpinBox(self.h_frame, theme=theme)
        self.h_doublespinbox_disabled.setObjectName(u"h_doublespinbox_disabled")
        self.h_doublespinbox_disabled.setEnabled(False)
        self.h_doublespinbox_disabled.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.h_spinbox_layout.addWidget(self.h_doublespinbox_disabled)


        self.main_layout.addLayout(self.h_spinbox_layout)

        self.button_group_layout = QHBoxLayout()
        self.button_group_layout.setObjectName(u"button_group_layout")
        self.h_button_group = HButtonGroup(self.h_frame, theme=theme)
        self.h_button_group.setObjectName(u"h_button_group")

        self.button_group_layout.addWidget(self.h_button_group)

        self.h_button_group_disabled = HButtonGroup(self.h_frame, theme=theme)
        self.h_button_group_disabled.setObjectName(u"h_button_group_disabled")
        self.h_button_group_disabled.setEnabled(False)

        self.button_group_layout.addWidget(self.h_button_group_disabled)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.button_group_layout.addItem(self.horizontalSpacer_5)


        self.main_layout.addLayout(self.button_group_layout)

        self.strong_buttons_layout = QHBoxLayout()
        self.strong_buttons_layout.setObjectName(u"strong_buttons_layout")
        self.h_strong_button_text = HStrongButton(self.h_frame, theme=theme)
        self.h_strong_button_text.setObjectName(u"h_strong_button_text")
        self.h_strong_button_text.setFlat(True)

        self.strong_buttons_layout.addWidget(self.h_strong_button_text)

        self.h_strong_button_text_icon = HStrongButton(self.h_frame, theme=theme)
        self.h_strong_button_text_icon.setObjectName(u"h_strong_button_text_icon")
        self.h_strong_button_text_icon.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        icon = QIcon()
        icon.addFile(u"../../hwidgets/icons/linux.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.h_strong_button_text_icon.setIcon(icon)
        self.h_strong_button_text_icon.setFlat(True)

        self.strong_buttons_layout.addWidget(self.h_strong_button_text_icon)

        self.h_strong_button_icon = HStrongButton(self.h_frame, theme=theme)
        self.h_strong_button_icon.setObjectName(u"h_strong_button_icon")
        self.h_strong_button_icon.setIcon(icon)
        self.h_strong_button_icon.setFlat(True)

        self.strong_buttons_layout.addWidget(self.h_strong_button_icon)

        self.h_strong_button_text_icon_2 = HStrongButton(self.h_frame, theme=theme)
        self.h_strong_button_text_icon_2.setObjectName(u"h_strong_button_text_icon_2")
        self.h_strong_button_text_icon_2.setEnabled(False)
        self.h_strong_button_text_icon_2.setIcon(icon)
        self.h_strong_button_text_icon_2.setFlat(True)

        self.strong_buttons_layout.addWidget(self.h_strong_button_text_icon_2)

        self.h_strong_button_text_icon_4 = HStrongButton(self.h_frame, theme=theme)
        self.h_strong_button_text_icon_4.setObjectName(u"h_strong_button_text_icon_4")
        self.h_strong_button_text_icon_4.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        icon1 = QIcon()
        icon1.addFile(u"../../hwidgets/icons/arrow_right_alt_22dp_000000_FILL0_wght400_GRAD0_opsz24.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.h_strong_button_text_icon_4.setIcon(icon1)
        self.h_strong_button_text_icon_4.setFlat(True)

        self.strong_buttons_layout.addWidget(self.h_strong_button_text_icon_4)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.strong_buttons_layout.addItem(self.horizontalSpacer_7)


        self.main_layout.addLayout(self.strong_buttons_layout)

        self.text_buttons_layout = QHBoxLayout()
        self.text_buttons_layout.setObjectName(u"text_buttons_layout")
        self.h_text_button = HButton(self.h_frame, theme=theme)
        self.h_text_button.setObjectName(u"h_text_button")

        self.text_buttons_layout.addWidget(self.h_text_button)

        self.h_text_button_checked = HButton(self.h_frame, theme=theme)
        self.h_text_button_checked.setObjectName(u"h_text_button_checked")
        self.h_text_button_checked.setCheckable(True)
        self.h_text_button_checked.setChecked(True)

        self.text_buttons_layout.addWidget(self.h_text_button_checked)

        self.h_text_button_disabled = HButton(self.h_frame, theme=theme)
        self.h_text_button_disabled.setObjectName(u"h_text_button_disabled")
        self.h_text_button_disabled.setEnabled(False)

        self.text_buttons_layout.addWidget(self.h_text_button_disabled)

        self.h_text_button_disabled_checked = HButton(self.h_frame, theme=theme)
        self.h_text_button_disabled_checked.setObjectName(u"h_text_button_disabled_checked")
        self.h_text_button_disabled_checked.setEnabled(False)
        self.h_text_button_disabled_checked.setCheckable(True)
        self.h_text_button_disabled_checked.setChecked(True)

        self.text_buttons_layout.addWidget(self.h_text_button_disabled_checked)


        self.main_layout.addLayout(self.text_buttons_layout)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.h_text_icon_button = HButton(self.h_frame, theme=theme)
        self.h_text_icon_button.setObjectName(u"h_text_icon_button")
        icon2 = QIcon()
        icon2.addFile(u"../../hwidgets/icons/gpu.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.h_text_icon_button.setIcon(icon2)

        self.horizontalLayout_18.addWidget(self.h_text_icon_button)

        self.h_text_icon_button_checked = HButton(self.h_frame, theme=theme)
        self.h_text_icon_button_checked.setObjectName(u"h_text_icon_button_checked")
        self.h_text_icon_button_checked.setIcon(icon2)
        self.h_text_icon_button_checked.setCheckable(True)
        self.h_text_icon_button_checked.setChecked(True)

        self.horizontalLayout_18.addWidget(self.h_text_icon_button_checked)

        self.h_text_icon_button_disabled = HButton(self.h_frame, theme=theme)
        self.h_text_icon_button_disabled.setObjectName(u"h_text_icon_button_disabled")
        self.h_text_icon_button_disabled.setEnabled(False)
        self.h_text_icon_button_disabled.setIcon(icon2)

        self.horizontalLayout_18.addWidget(self.h_text_icon_button_disabled)

        self.h_text_icon_button_disabled_checked = HButton(self.h_frame, theme=theme)
        self.h_text_icon_button_disabled_checked.setObjectName(u"h_text_icon_button_disabled_checked")
        self.h_text_icon_button_disabled_checked.setEnabled(False)
        self.h_text_icon_button_disabled_checked.setIcon(icon2)
        self.h_text_icon_button_disabled_checked.setCheckable(True)
        self.h_text_icon_button_disabled_checked.setChecked(True)

        self.horizontalLayout_18.addWidget(self.h_text_icon_button_disabled_checked)


        self.main_layout.addLayout(self.horizontalLayout_18)

        self.h_button_layout = QHBoxLayout()
        self.h_button_layout.setObjectName(u"h_button_layout")
        self.h_label_4 = HLabel(self.h_frame, theme=theme)
        self.h_label_4.setObjectName(u"h_label_4")

        self.h_button_layout.addWidget(self.h_label_4)

        self.h_button = HButton(self.h_frame, theme=theme)
        self.h_button.setObjectName(u"h_button")
        sizePolicy.setHeightForWidth(self.h_button.sizePolicy().hasHeightForWidth())
        self.h_button.setSizePolicy(sizePolicy)
        self.h_button.setMaximumSize(QSize(24, 24))
        icon3 = QIcon()
        icon3.addFile(u"../../hwidgets/icons/settings_FILL0_wght400_GRAD0_opsz24.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.h_button.setIcon(icon3)
        self.h_button.setIconSize(QSize(24, 24))
        self.h_button.setFlat(True)

        self.h_button_layout.addWidget(self.h_button)

        self.h_button_checked = HButton(self.h_frame, theme=theme)
        self.h_button_checked.setObjectName(u"h_button_checked")
        self.h_button_checked.setMaximumSize(QSize(24, 24))
        self.h_button_checked.setIcon(icon3)
        self.h_button_checked.setIconSize(QSize(24, 24))
        self.h_button_checked.setCheckable(True)
        self.h_button_checked.setChecked(True)
        self.h_button_checked.setFlat(True)

        self.h_button_layout.addWidget(self.h_button_checked)

        self.h_button_disabled = HButton(self.h_frame, theme=theme)
        self.h_button_disabled.setObjectName(u"h_button_disabled")
        self.h_button_disabled.setEnabled(False)
        self.h_button_disabled.setMaximumSize(QSize(24, 24))
        self.h_button_disabled.setIcon(icon3)
        self.h_button_disabled.setIconSize(QSize(24, 24))
        self.h_button_disabled.setFlat(True)

        self.h_button_layout.addWidget(self.h_button_disabled)

        self.h_button_disabled_checked = HButton(self.h_frame, theme=theme)
        self.h_button_disabled_checked.setObjectName(u"h_button_disabled_checked")
        self.h_button_disabled_checked.setEnabled(False)
        self.h_button_disabled_checked.setMaximumSize(QSize(24, 24))
        self.h_button_disabled_checked.setIcon(icon3)
        self.h_button_disabled_checked.setIconSize(QSize(24, 24))
        self.h_button_disabled_checked.setCheckable(True)
        self.h_button_disabled_checked.setChecked(True)
        self.h_button_disabled_checked.setFlat(True)

        self.h_button_layout.addWidget(self.h_button_disabled_checked)

        self.h_button_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.h_button_layout.addItem(self.h_button_spacer)

        self.h_label_3 = HLabel(self.h_frame, theme=theme)
        self.h_label_3.setObjectName(u"h_label_3")

        self.h_button_layout.addWidget(self.h_label_3)

        self.h_button_checked_2 = HButton(self.h_frame, theme=theme)
        self.h_button_checked_2.setObjectName(u"h_button_checked_2")
        self.h_button_checked_2.setMaximumSize(QSize(24, 24))
        self.h_button_checked_2.setIcon(icon3)
        self.h_button_checked_2.setIconSize(QSize(24, 24))
        self.h_button_checked_2.setCheckable(True)
        self.h_button_checked_2.setChecked(True)
        self.h_button_checked_2.setFlat(False)

        self.h_button_layout.addWidget(self.h_button_checked_2)

        self.h_button_disabled_2 = HButton(self.h_frame, theme=theme)
        self.h_button_disabled_2.setObjectName(u"h_button_disabled_2")
        self.h_button_disabled_2.setEnabled(False)
        self.h_button_disabled_2.setMaximumSize(QSize(24, 24))
        self.h_button_disabled_2.setIcon(icon3)
        self.h_button_disabled_2.setIconSize(QSize(24, 24))
        self.h_button_disabled_2.setFlat(False)

        self.h_button_layout.addWidget(self.h_button_disabled_2)

        self.h_button_2 = HButton(self.h_frame, theme=theme)
        self.h_button_2.setObjectName(u"h_button_2")
        sizePolicy.setHeightForWidth(self.h_button_2.sizePolicy().hasHeightForWidth())
        self.h_button_2.setSizePolicy(sizePolicy)
        self.h_button_2.setMaximumSize(QSize(24, 24))
        self.h_button_2.setIcon(icon3)
        self.h_button_2.setIconSize(QSize(24, 24))
        self.h_button_2.setFlat(False)

        self.h_button_layout.addWidget(self.h_button_2)

        self.h_button_disabled_checked_2 = HButton(self.h_frame, theme=theme)
        self.h_button_disabled_checked_2.setObjectName(u"h_button_disabled_checked_2")
        self.h_button_disabled_checked_2.setEnabled(False)
        self.h_button_disabled_checked_2.setMaximumSize(QSize(24, 24))
        self.h_button_disabled_checked_2.setIcon(icon3)
        self.h_button_disabled_checked_2.setIconSize(QSize(24, 24))
        self.h_button_disabled_checked_2.setCheckable(True)
        self.h_button_disabled_checked_2.setChecked(True)
        self.h_button_disabled_checked_2.setFlat(False)

        self.h_button_layout.addWidget(self.h_button_disabled_checked_2)


        self.main_layout.addLayout(self.h_button_layout)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.main_layout.addItem(self.verticalSpacer_2)


        self.horizontalLayout_10.addLayout(self.main_layout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, 60, -1)
        self.h_frame_styled_raised = HFrame(self.h_frame, theme=theme)
        self.h_frame_styled_raised.setObjectName(u"h_frame_styled_raised")
        self.h_frame_styled_raised.setFrameShape(QFrame.Shape.StyledPanel)
        self.h_frame_styled_raised.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayout_9 = QVBoxLayout(self.h_frame_styled_raised)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.h_comment_bold_2 = HComment(self.h_frame_styled_raised, theme=theme)
        self.h_comment_bold_2.setObjectName(u"h_comment_bold_2")
        self.h_comment_bold_2.setWordWrap(True)

        self.verticalLayout_9.addWidget(self.h_comment_bold_2)

        self.h_comment_italic_2 = HComment(self.h_frame_styled_raised, theme=theme)
        self.h_comment_italic_2.setObjectName(u"h_comment_italic_2")
        self.h_comment_italic_2.setWordWrap(True)

        self.verticalLayout_9.addWidget(self.h_comment_italic_2)

        self.h_description_2 = HDescription(self.h_frame_styled_raised, theme=theme)
        self.h_description_2.setObjectName(u"h_description_2")
        self.h_description_2.setWordWrap(True)

        self.verticalLayout_9.addWidget(self.h_description_2)

        self.labels_layout_2 = QHBoxLayout()
        self.labels_layout_2.setObjectName(u"labels_layout_2")
        self.h_label_2 = HLabel(self.h_frame_styled_raised, theme=theme)
        self.h_label_2.setObjectName(u"h_label_2")

        self.labels_layout_2.addWidget(self.h_label_2)

        self.h_label_disabled_2 = HLabel(self.h_frame_styled_raised, theme=theme)
        self.h_label_disabled_2.setObjectName(u"h_label_disabled_2")
        self.h_label_disabled_2.setEnabled(False)

        self.labels_layout_2.addWidget(self.h_label_disabled_2)


        self.verticalLayout_9.addLayout(self.labels_layout_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.h_checkbox_2 = HCheckBox(self.h_frame_styled_raised, theme=theme)
        self.h_checkbox_2.setObjectName(u"h_checkbox_2")

        self.horizontalLayout_5.addWidget(self.h_checkbox_2)

        self.h_checkbox_clicked_2 = HCheckBox(self.h_frame_styled_raised, theme=theme)
        self.h_checkbox_clicked_2.setObjectName(u"h_checkbox_clicked_2")
        self.h_checkbox_clicked_2.setChecked(True)

        self.horizontalLayout_5.addWidget(self.h_checkbox_clicked_2)

        self.h_checkbox_disabled_2 = HCheckBox(self.h_frame_styled_raised, theme=theme)
        self.h_checkbox_disabled_2.setObjectName(u"h_checkbox_disabled_2")
        self.h_checkbox_disabled_2.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.h_checkbox_disabled_2)

        self.h_checkbox_disabled_clicked_2 = HCheckBox(self.h_frame_styled_raised, theme=theme)
        self.h_checkbox_disabled_clicked_2.setObjectName(u"h_checkbox_disabled_clicked_2")
        self.h_checkbox_disabled_clicked_2.setEnabled(False)
        self.h_checkbox_disabled_clicked_2.setChecked(True)

        self.horizontalLayout_5.addWidget(self.h_checkbox_disabled_clicked_2)

        self.horizontalSpacer_4 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.h_switch_2 = HSwitch(self.h_frame_styled_raised, theme=theme)
        self.h_switch_2.setObjectName(u"h_switch_2")

        self.horizontalLayout_5.addWidget(self.h_switch_2)

        self.h_switch_checked_2 = HSwitch(self.h_frame_styled_raised, theme=theme)
        self.h_switch_checked_2.setObjectName(u"h_switch_checked_2")
        self.h_switch_checked_2.setChecked(True)

        self.horizontalLayout_5.addWidget(self.h_switch_checked_2)

        self.h_switch_disabled_2 = HSwitch(self.h_frame_styled_raised, theme=theme)
        self.h_switch_disabled_2.setObjectName(u"h_switch_disabled_2")
        self.h_switch_disabled_2.setEnabled(False)
        self.h_switch_disabled_2.setCheckable(True)

        self.horizontalLayout_5.addWidget(self.h_switch_disabled_2)

        self.h_switch_disabled_checked_2 = HSwitch(self.h_frame_styled_raised, theme=theme)
        self.h_switch_disabled_checked_2.setObjectName(u"h_switch_disabled_checked_2")
        self.h_switch_disabled_checked_2.setEnabled(False)
        self.h_switch_disabled_checked_2.setChecked(True)

        self.horizontalLayout_5.addWidget(self.h_switch_disabled_checked_2)


        self.verticalLayout_9.addLayout(self.horizontalLayout_5)

        self.radio_layout_2 = QHBoxLayout()
        self.radio_layout_2.setObjectName(u"radio_layout_2")
        self.h_radiobutton_enabled_off_2 = HRadioButton(self.h_frame_styled_raised, theme=theme)
        self.h_radiobutton_enabled_off_2.setObjectName(u"h_radiobutton_enabled_off_2")
        self.h_radiobutton_enabled_off_2.setChecked(False)

        self.radio_layout_2.addWidget(self.h_radiobutton_enabled_off_2)

        self.h_radiobutton_enabled_on_2 = HRadioButton(self.h_frame_styled_raised, theme=theme)
        self.h_radiobutton_enabled_on_2.setObjectName(u"h_radiobutton_enabled_on_2")
        self.h_radiobutton_enabled_on_2.setChecked(True)

        self.radio_layout_2.addWidget(self.h_radiobutton_enabled_on_2)

        self.h_radiobutton_disabled_on_2 = HRadioButton(self.h_frame_styled_raised, theme=theme)
        self.h_radiobutton_disabled_on_2.setObjectName(u"h_radiobutton_disabled_on_2")
        self.h_radiobutton_disabled_on_2.setEnabled(False)
        self.h_radiobutton_disabled_on_2.setChecked(False)

        self.radio_layout_2.addWidget(self.h_radiobutton_disabled_on_2)

        self.h_radiobutton_disabled_off_2 = HRadioButton(self.h_frame_styled_raised, theme=theme)
        self.h_radiobutton_disabled_off_2.setObjectName(u"h_radiobutton_disabled_off_2")
        self.h_radiobutton_disabled_off_2.setEnabled(False)

        self.radio_layout_2.addWidget(self.h_radiobutton_disabled_off_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.radio_layout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_9.addLayout(self.radio_layout_2)

        self.lineedit_layout_2 = QHBoxLayout()
        self.lineedit_layout_2.setObjectName(u"lineedit_layout_2")
        self.h_lineedit_editable_2 = HLineEdit(self.h_frame_styled_raised, theme=theme)
        self.h_lineedit_editable_2.setObjectName(u"h_lineedit_editable_2")
        self.h_lineedit_editable_2.setClearButtonEnabled(False)

        self.lineedit_layout_2.addWidget(self.h_lineedit_editable_2)

        self.h_lineedit_editable_clear_button_2 = HLineEdit(self.h_frame_styled_raised, theme=theme)
        self.h_lineedit_editable_clear_button_2.setObjectName(u"h_lineedit_editable_clear_button_2")
        self.h_lineedit_editable_clear_button_2.setClearButtonEnabled(True)

        self.lineedit_layout_2.addWidget(self.h_lineedit_editable_clear_button_2)

        self.h_lineedit_disabled_2 = HLineEdit(self.h_frame_styled_raised, theme=theme)
        self.h_lineedit_disabled_2.setObjectName(u"h_lineedit_disabled_2")
        self.h_lineedit_disabled_2.setEnabled(False)
        self.h_lineedit_disabled_2.setClearButtonEnabled(True)

        self.lineedit_layout_2.addWidget(self.h_lineedit_disabled_2)

        self.h_lineedit_read_only_2 = HLineEdit(self.h_frame_styled_raised, theme=theme)
        self.h_lineedit_read_only_2.setObjectName(u"h_lineedit_read_only_2")
        self.h_lineedit_read_only_2.setReadOnly(True)
        self.h_lineedit_read_only_2.setClearButtonEnabled(True)

        self.lineedit_layout_2.addWidget(self.h_lineedit_read_only_2)


        self.verticalLayout_9.addLayout(self.lineedit_layout_2)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.h_combobox_rw_2 = HComboBox(self.h_frame_styled_raised, theme=theme)
        self.h_combobox_rw_2.setObjectName(u"h_combobox_rw_2")
        sizePolicy.setHeightForWidth(self.h_combobox_rw_2.sizePolicy().hasHeightForWidth())
        self.h_combobox_rw_2.setSizePolicy(sizePolicy)
        self.h_combobox_rw_2.setMaximumSize(QSize(300, 16777215))
        self.h_combobox_rw_2.setEditable(True)

        self.horizontalLayout_22.addWidget(self.h_combobox_rw_2)

        self.h_combobox_ro_2 = HComboBox(self.h_frame_styled_raised, theme=theme)
        self.h_combobox_ro_2.setObjectName(u"h_combobox_ro_2")
        sizePolicy.setHeightForWidth(self.h_combobox_ro_2.sizePolicy().hasHeightForWidth())
        self.h_combobox_ro_2.setSizePolicy(sizePolicy)
        self.h_combobox_ro_2.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_22.addWidget(self.h_combobox_ro_2)

        self.h_combobox_disabled_2 = HComboBox(self.h_frame_styled_raised, theme=theme)
        self.h_combobox_disabled_2.setObjectName(u"h_combobox_disabled_2")
        self.h_combobox_disabled_2.setEnabled(False)
        self.h_combobox_disabled_2.setEditable(True)

        self.horizontalLayout_22.addWidget(self.h_combobox_disabled_2)


        self.verticalLayout_9.addLayout(self.horizontalLayout_22)

        self.plaintextedit_layout_2 = QHBoxLayout()
        self.plaintextedit_layout_2.setObjectName(u"plaintextedit_layout_2")
        self.h_plaintextedit_editable_2 = HPlainTextEdit(self.h_frame_styled_raised, theme=theme)
        self.h_plaintextedit_editable_2.setObjectName(u"h_plaintextedit_editable_2")
        self.h_plaintextedit_editable_2.setMaximumSize(QSize(100, 150))

        self.plaintextedit_layout_2.addWidget(self.h_plaintextedit_editable_2)

        self.h_plaintextedit_editable_vscrollbar_2 = HPlainTextEdit(self.h_frame_styled_raised, theme=theme)
        self.h_plaintextedit_editable_vscrollbar_2.setObjectName(u"h_plaintextedit_editable_vscrollbar_2")
        self.h_plaintextedit_editable_vscrollbar_2.setMaximumSize(QSize(100, 150))

        self.plaintextedit_layout_2.addWidget(self.h_plaintextedit_editable_vscrollbar_2)

        self.h_plaintextedit_editable_scrollbars_2 = HPlainTextEdit(self.h_frame_styled_raised, theme=theme)
        self.h_plaintextedit_editable_scrollbars_2.setObjectName(u"h_plaintextedit_editable_scrollbars_2")
        self.h_plaintextedit_editable_scrollbars_2.setMaximumSize(QSize(150, 150))
        self.h_plaintextedit_editable_scrollbars_2.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)

        self.plaintextedit_layout_2.addWidget(self.h_plaintextedit_editable_scrollbars_2)

        self.h_plaintextedit_readonly_2 = HPlainTextEdit(self.h_frame_styled_raised, theme=theme)
        self.h_plaintextedit_readonly_2.setObjectName(u"h_plaintextedit_readonly_2")
        self.h_plaintextedit_readonly_2.setMaximumSize(QSize(100, 150))
        self.h_plaintextedit_readonly_2.setReadOnly(True)

        self.plaintextedit_layout_2.addWidget(self.h_plaintextedit_readonly_2)

        self.h_plaintextedit_disabled_2 = HPlainTextEdit(self.h_frame_styled_raised, theme=theme)
        self.h_plaintextedit_disabled_2.setObjectName(u"h_plaintextedit_disabled_2")
        self.h_plaintextedit_disabled_2.setEnabled(False)
        self.h_plaintextedit_disabled_2.setMaximumSize(QSize(100, 150))

        self.plaintextedit_layout_2.addWidget(self.h_plaintextedit_disabled_2)


        self.verticalLayout_9.addLayout(self.plaintextedit_layout_2)

        self.h_spinbox_layout_2 = QHBoxLayout()
        self.h_spinbox_layout_2.setObjectName(u"h_spinbox_layout_2")
        self.h_spinbox_no_button_2 = HSpinBox(self.h_frame_styled_raised, theme=theme)
        self.h_spinbox_no_button_2.setObjectName(u"h_spinbox_no_button_2")
        self.h_spinbox_no_button_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.h_spinbox_no_button_2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.h_spinbox_layout_2.addWidget(self.h_spinbox_no_button_2)

        self.h_spinbox_rw_2 = HSpinBox(self.h_frame_styled_raised, theme=theme)
        self.h_spinbox_rw_2.setObjectName(u"h_spinbox_rw_2")
        self.h_spinbox_rw_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.h_spinbox_rw_2.setMinimum(10)

        self.h_spinbox_layout_2.addWidget(self.h_spinbox_rw_2)

        self.h_spinbox_ro_2 = HSpinBox(self.h_frame_styled_raised, theme=theme)
        self.h_spinbox_ro_2.setObjectName(u"h_spinbox_ro_2")
        self.h_spinbox_ro_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.h_spinbox_ro_2.setReadOnly(True)

        self.h_spinbox_layout_2.addWidget(self.h_spinbox_ro_2)

        self.h_spinbox_disabled_2 = HSpinBox(self.h_frame_styled_raised, theme=theme)
        self.h_spinbox_disabled_2.setObjectName(u"h_spinbox_disabled_2")
        self.h_spinbox_disabled_2.setEnabled(False)
        self.h_spinbox_disabled_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.h_spinbox_layout_2.addWidget(self.h_spinbox_disabled_2)

        self.rlg_spinbox_spacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.h_spinbox_layout_2.addItem(self.rlg_spinbox_spacer_2)

        self.h_doublespinbox_nobutton_2 = HDoubleSpinBox(self.h_frame_styled_raised, theme=theme)
        self.h_doublespinbox_nobutton_2.setObjectName(u"h_doublespinbox_nobutton_2")
        self.h_doublespinbox_nobutton_2.setFrame(True)
        self.h_doublespinbox_nobutton_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.h_doublespinbox_nobutton_2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.h_spinbox_layout_2.addWidget(self.h_doublespinbox_nobutton_2)

        self.h_doublespinbox_rw_2 = HDoubleSpinBox(self.h_frame_styled_raised, theme=theme)
        self.h_doublespinbox_rw_2.setObjectName(u"h_doublespinbox_rw_2")
        self.h_doublespinbox_rw_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.h_doublespinbox_rw_2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.h_doublespinbox_rw_2.setProperty(u"showGroupSeparator", False)
        self.h_doublespinbox_rw_2.setDecimals(1)
        self.h_doublespinbox_rw_2.setMinimum(10.000000000000000)

        self.h_spinbox_layout_2.addWidget(self.h_doublespinbox_rw_2)

        self.h_doublespinbox_ro_2 = HDoubleSpinBox(self.h_frame_styled_raised, theme=theme)
        self.h_doublespinbox_ro_2.setObjectName(u"h_doublespinbox_ro_2")
        self.h_doublespinbox_ro_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.h_doublespinbox_ro_2.setReadOnly(True)

        self.h_spinbox_layout_2.addWidget(self.h_doublespinbox_ro_2)

        self.h_doublespinbox_disabled_2 = HDoubleSpinBox(self.h_frame_styled_raised, theme=theme)
        self.h_doublespinbox_disabled_2.setObjectName(u"h_doublespinbox_disabled_2")
        self.h_doublespinbox_disabled_2.setEnabled(False)
        self.h_doublespinbox_disabled_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.h_spinbox_layout_2.addWidget(self.h_doublespinbox_disabled_2)


        self.verticalLayout_9.addLayout(self.h_spinbox_layout_2)


        self.verticalLayout_3.addWidget(self.h_frame_styled_raised)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.horizontalLayout_10.addLayout(self.verticalLayout_3)


        self.horizontalLayout.addWidget(self.h_frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.h_title.setText(QCoreApplication.translate("MainWindow", u"This is a HTitle widget without icon", None))
        self.h_title_icon.setText("")
        self.h_subtitles.setText(QCoreApplication.translate("MainWindow", u"Subtitle", None))
        self.h_description.setText(QCoreApplication.translate("MainWindow", u"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", None))
        self.h_comment_bold.setText(QCoreApplication.translate("MainWindow", u"Bold comment", None))
        self.h_comment_italic.setText(QCoreApplication.translate("MainWindow", u"Italic comment", None))
        self.h_comment_small_italic.setText(QCoreApplication.translate("MainWindow", u"Small italic comment", None))
        self.h_label.setText(QCoreApplication.translate("MainWindow", u"A Hlabel", None))
        self.h_label_disabled.setText(QCoreApplication.translate("MainWindow", u"A disabled Hlabel", None))
        self.h_checkbox.setText("")
        self.h_checkbox_clicked.setText("")
        self.h_checkbox_disabled.setText("")
        self.h_checkbox_disabled_clicked.setText("")
        self.h_switch.setText("")
        self.h_switch_checked.setText("")
        self.h_switch_disabled.setText("")
        self.h_switch_disabled_checked.setText("")
        self.h_radiobutton_enabled_off.setText("")
        self.h_radiobutton_enabled_on.setText("")
        self.h_radiobutton_disabled_on.setText("")
        self.h_radiobutton_disabled_off.setText("")
        self.h_lineedit_editable.setText(QCoreApplication.translate("MainWindow", u"Editable", None))
        self.h_lineedit_editable_clear_button.setText(QCoreApplication.translate("MainWindow", u"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", None))
        self.h_lineedit_disabled.setText(QCoreApplication.translate("MainWindow", u"Disabled", None))
        self.h_lineedit_read_only.setText(QCoreApplication.translate("MainWindow", u"ReadOnly", None))
        self.h_plaintextedit_editable.setPlainText(QCoreApplication.translate("MainWindow", u"editable\n"
"sdsdc", None))
        self.h_plaintextedit_editable_vscrollbar.setPlainText(QCoreApplication.translate("MainWindow", u"editable\n"
"multiple lines\n"
"for scrollbar\n"
"with test\n"
"", None))
        self.h_plaintextedit_editable_scrollbars.setPlainText(QCoreApplication.translate("MainWindow", u"editable\n"
"multiple lines with very large text for hscrollbar\n"
"for scrollbar \n"
"with test\n"
"and\n"
"a lot\n"
"of vertical text\n"
"", None))
        self.h_plaintextedit_readonly.setPlainText(QCoreApplication.translate("MainWindow", u"read only\n"
"", None))
        self.h_plaintextedit_disabled.setPlainText(QCoreApplication.translate("MainWindow", u"disabled\n"
"", None))
        self.h_strong_button_text.setText(QCoreApplication.translate("MainWindow", u"Strong Button", None))
        self.h_strong_button_text_icon.setText(QCoreApplication.translate("MainWindow", u"Strong Button with icon", None))
        self.h_strong_button_icon.setText("")
        self.h_strong_button_text_icon_2.setText(QCoreApplication.translate("MainWindow", u"Strong Button disabled", None))
        self.h_strong_button_text_icon_4.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.h_text_button.setText(QCoreApplication.translate("MainWindow", u"Button", None))
        self.h_text_button_checked.setText(QCoreApplication.translate("MainWindow", u"Button (checked)", None))
        self.h_text_button_disabled.setText(QCoreApplication.translate("MainWindow", u"Button (disabled)", None))
        self.h_text_button_disabled_checked.setText(QCoreApplication.translate("MainWindow", u"Button (Checked Disabled)", None))
        self.h_text_icon_button.setText(QCoreApplication.translate("MainWindow", u"ibutton", None))
        self.h_text_icon_button_checked.setText(QCoreApplication.translate("MainWindow", u"ibutton (checked)", None))
        self.h_text_icon_button_disabled.setText(QCoreApplication.translate("MainWindow", u"ibutton (disabled)", None))
        self.h_text_icon_button_disabled_checked.setText(QCoreApplication.translate("MainWindow", u"ibutton (Checked Disabled)", None))
        self.h_label_4.setText(QCoreApplication.translate("MainWindow", u"flat", None))
        self.h_button.setText("")
        self.h_button_checked.setText("")
        self.h_button_disabled.setText("")
        self.h_button_disabled_checked.setText("")
        self.h_label_3.setText(QCoreApplication.translate("MainWindow", u"non flat", None))
        self.h_button_checked_2.setText("")
        self.h_button_disabled_2.setText("")
        self.h_button_2.setText("")
        self.h_button_disabled_checked_2.setText("")
        self.h_comment_bold_2.setText(QCoreApplication.translate("MainWindow", u"Bold comment", None))
        self.h_comment_italic_2.setText(QCoreApplication.translate("MainWindow", u"Italic comment", None))
        self.h_description_2.setText(QCoreApplication.translate("MainWindow", u"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", None))
        self.h_label_2.setText(QCoreApplication.translate("MainWindow", u"A Hlabel", None))
        self.h_label_disabled_2.setText(QCoreApplication.translate("MainWindow", u"A disabled Hlabel", None))
        self.h_checkbox_2.setText("")
        self.h_checkbox_clicked_2.setText("")
        self.h_checkbox_disabled_2.setText("")
        self.h_checkbox_disabled_clicked_2.setText("")
        self.h_switch_2.setText("")
        self.h_switch_checked_2.setText("")
        self.h_switch_disabled_2.setText("")
        self.h_switch_disabled_checked_2.setText("")
        self.h_radiobutton_enabled_off_2.setText("")
        self.h_radiobutton_enabled_on_2.setText("")
        self.h_radiobutton_disabled_on_2.setText("")
        self.h_radiobutton_disabled_off_2.setText("")
        self.h_lineedit_editable_2.setText(QCoreApplication.translate("MainWindow", u"Editable", None))
        self.h_lineedit_editable_clear_button_2.setText(QCoreApplication.translate("MainWindow", u"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", None))
        self.h_lineedit_disabled_2.setText(QCoreApplication.translate("MainWindow", u"Disabled", None))
        self.h_lineedit_read_only_2.setText(QCoreApplication.translate("MainWindow", u"ReadOnly", None))
        self.h_plaintextedit_editable_2.setPlainText(QCoreApplication.translate("MainWindow", u"editable\n"
"sdsdc", None))
        self.h_plaintextedit_editable_vscrollbar_2.setPlainText(QCoreApplication.translate("MainWindow", u"editable\n"
"multiple lines\n"
"for scrollbar\n"
"with test\n"
"", None))
        self.h_plaintextedit_editable_scrollbars_2.setPlainText(QCoreApplication.translate("MainWindow", u"editable\n"
"multiple lines with very large text for hscrollbar\n"
"for scrollbar \n"
"with test\n"
"and\n"
"a lot\n"
"of vertical text\n"
"", None))
        self.h_plaintextedit_readonly_2.setPlainText(QCoreApplication.translate("MainWindow", u"read only\n"
"", None))
        self.h_plaintextedit_disabled_2.setPlainText(QCoreApplication.translate("MainWindow", u"disabled\n"
"", None))
    # retranslateUi

