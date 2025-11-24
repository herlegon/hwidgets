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
    QComboBox, QDoubleSpinBox, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPlainTextEdit, QProgressBar, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

from typing import Type
from hwidgets import (
    HButton,
    HCheckBox,
    HComboBox,
    HDoubleSpinBox,
    HGroupBox,
    HLabel,
    HLineEdit,
    HPlainTextEdit,
    HRadioButton,
    HScrollBar,
    HSpinBox,
    HButtonGroup,
    HDivider,
    HHorizontalDivider,
    HIndeterminateCircularProgress,
    HIndeterminateProgress,
    HProgress,
    HRadialProgress,
    HSwitch,
    HTitle,
    HVerticalDivider,
    Theme,
)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, theme: Type[Theme]):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 860)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.q_frame = QFrame(self.centralwidget)
        self.q_frame.setObjectName(u"q_frame")
        self.q_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.q_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.q_widgets_main_layout = QHBoxLayout(self.q_frame)
        self.q_widgets_main_layout.setSpacing(9)
        self.q_widgets_main_layout.setObjectName(u"q_widgets_main_layout")
        self.q_widgets_main_layout.setContentsMargins(12, 18, 18, 18)
        self.q_line = QFrame(self.q_frame)
        self.q_line.setObjectName(u"q_line")
        self.q_line.setFrameShape(QFrame.Shape.HLine)
        self.q_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.q_widgets_main_layout.addWidget(self.q_line)

        self.q_widgets_sub_layout = QVBoxLayout()
        self.q_widgets_sub_layout.setObjectName(u"q_widgets_sub_layout")
        self.q_combobox_layout = QVBoxLayout()
        self.q_combobox_layout.setObjectName(u"q_combobox_layout")
        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.q_combobox_read_only = QComboBox(self.q_frame)
        self.q_combobox_read_only.setObjectName(u"q_combobox_read_only")
        self.q_combobox_read_only.setMaximumSize(QSize(300, 16777215))
        self.q_combobox_read_only.setEditable(True)

        self.horizontalLayout_20.addWidget(self.q_combobox_read_only)

        self.q_combobox_rw = QComboBox(self.q_frame)
        self.q_combobox_rw.setObjectName(u"q_combobox_rw")
        self.q_combobox_rw.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_20.addWidget(self.q_combobox_rw)


        self.q_combobox_layout.addLayout(self.horizontalLayout_20)

        self.q_combobox_disabled = QComboBox(self.q_frame)
        self.q_combobox_disabled.setObjectName(u"q_combobox_disabled")
        self.q_combobox_disabled.setEnabled(False)
        self.q_combobox_disabled.setEditable(True)

        self.q_combobox_layout.addWidget(self.q_combobox_disabled)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.q_lineedit_editable_3 = QLineEdit(self.q_frame)
        self.q_lineedit_editable_3.setObjectName(u"q_lineedit_editable_3")
        self.q_lineedit_editable_3.setClearButtonEnabled(False)

        self.horizontalLayout_23.addWidget(self.q_lineedit_editable_3)

        self.q_combobox_read_only_3 = QComboBox(self.q_frame)
        self.q_combobox_read_only_3.setObjectName(u"q_combobox_read_only_3")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.q_combobox_read_only_3.sizePolicy().hasHeightForWidth())
        self.q_combobox_read_only_3.setSizePolicy(sizePolicy)
        self.q_combobox_read_only_3.setMaximumSize(QSize(300, 16777215))

        self.horizontalLayout_23.addWidget(self.q_combobox_read_only_3)

        self.q_spinbox_rw_3 = QSpinBox(self.q_frame)
        self.q_spinbox_rw_3.setObjectName(u"q_spinbox_rw_3")
        self.q_spinbox_rw_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.q_spinbox_rw_3.setMinimum(10)

        self.horizontalLayout_23.addWidget(self.q_spinbox_rw_3)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_11)


        self.q_combobox_layout.addLayout(self.horizontalLayout_23)


        self.q_widgets_sub_layout.addLayout(self.q_combobox_layout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.q_radiobutton_1 = QRadioButton(self.q_frame)
        self.buttonGroup_3 = QButtonGroup(MainWindow)
        self.buttonGroup_3.setObjectName(u"buttonGroup_3")
        self.buttonGroup_3.addButton(self.q_radiobutton_1)
        self.q_radiobutton_1.setObjectName(u"q_radiobutton_1")
        self.q_radiobutton_1.setChecked(True)

        self.horizontalLayout_3.addWidget(self.q_radiobutton_1)

        self.q_radiobutton_2 = QRadioButton(self.q_frame)
        self.buttonGroup_3.addButton(self.q_radiobutton_2)
        self.q_radiobutton_2.setObjectName(u"q_radiobutton_2")

        self.horizontalLayout_3.addWidget(self.q_radiobutton_2)

        self.q_radiobutton_disabled_1 = QRadioButton(self.q_frame)
        self.buttonGroup_4 = QButtonGroup(MainWindow)
        self.buttonGroup_4.setObjectName(u"buttonGroup_4")
        self.buttonGroup_4.addButton(self.q_radiobutton_disabled_1)
        self.q_radiobutton_disabled_1.setObjectName(u"q_radiobutton_disabled_1")
        self.q_radiobutton_disabled_1.setEnabled(False)
        self.q_radiobutton_disabled_1.setChecked(True)

        self.horizontalLayout_3.addWidget(self.q_radiobutton_disabled_1)

        self.q_radiobutton_disabled_2 = QRadioButton(self.q_frame)
        self.buttonGroup_4.addButton(self.q_radiobutton_disabled_2)
        self.q_radiobutton_disabled_2.setObjectName(u"q_radiobutton_disabled_2")
        self.q_radiobutton_disabled_2.setEnabled(False)

        self.horizontalLayout_3.addWidget(self.q_radiobutton_disabled_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.q_widgets_sub_layout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.q_label = QLabel(self.q_frame)
        self.q_label.setObjectName(u"q_label")

        self.horizontalLayout_7.addWidget(self.q_label)

        self.q_label_disabled = QLabel(self.q_frame)
        self.q_label_disabled.setObjectName(u"q_label_disabled")
        self.q_label_disabled.setEnabled(False)

        self.horizontalLayout_7.addWidget(self.q_label_disabled)


        self.q_widgets_sub_layout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.q_label_checkbox = QLabel(self.q_frame)
        self.q_label_checkbox.setObjectName(u"q_label_checkbox")

        self.horizontalLayout_5.addWidget(self.q_label_checkbox)

        self.q_checkbox = QCheckBox(self.q_frame)
        self.q_checkbox.setObjectName(u"q_checkbox")

        self.horizontalLayout_5.addWidget(self.q_checkbox)

        self.q_checkbox_clicked = QCheckBox(self.q_frame)
        self.q_checkbox_clicked.setObjectName(u"q_checkbox_clicked")
        self.q_checkbox_clicked.setChecked(True)

        self.horizontalLayout_5.addWidget(self.q_checkbox_clicked)

        self.q_checkbox_disabled = QCheckBox(self.q_frame)
        self.q_checkbox_disabled.setObjectName(u"q_checkbox_disabled")
        self.q_checkbox_disabled.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.q_checkbox_disabled)

        self.q_checkbox_disabled_clicked = QCheckBox(self.q_frame)
        self.q_checkbox_disabled_clicked.setObjectName(u"q_checkbox_disabled_clicked")
        self.q_checkbox_disabled_clicked.setEnabled(False)
        self.q_checkbox_disabled_clicked.setChecked(True)

        self.horizontalLayout_5.addWidget(self.q_checkbox_disabled_clicked)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.q_widgets_sub_layout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.q_text_button = QPushButton(self.q_frame)
        self.q_text_button.setObjectName(u"q_text_button")

        self.horizontalLayout_9.addWidget(self.q_text_button)

        self.q_text_button_checked = QPushButton(self.q_frame)
        self.q_text_button_checked.setObjectName(u"q_text_button_checked")
        self.q_text_button_checked.setCheckable(True)
        self.q_text_button_checked.setChecked(True)

        self.horizontalLayout_9.addWidget(self.q_text_button_checked)

        self.q_text_button_disabled = QPushButton(self.q_frame)
        self.q_text_button_disabled.setObjectName(u"q_text_button_disabled")
        self.q_text_button_disabled.setEnabled(False)

        self.horizontalLayout_9.addWidget(self.q_text_button_disabled)

        self.q_text_button_checked_disabled = QPushButton(self.q_frame)
        self.q_text_button_checked_disabled.setObjectName(u"q_text_button_checked_disabled")
        self.q_text_button_checked_disabled.setEnabled(False)
        self.q_text_button_checked_disabled.setCheckable(True)
        self.q_text_button_checked_disabled.setChecked(True)

        self.horizontalLayout_9.addWidget(self.q_text_button_checked_disabled)


        self.q_widgets_sub_layout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.q_text_icon_button = QPushButton(self.q_frame)
        self.q_text_icon_button.setObjectName(u"q_text_icon_button")
        icon = QIcon()
        icon.addFile(u"../../hwidgets/icons/gpu.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.q_text_icon_button.setIcon(icon)

        self.horizontalLayout_19.addWidget(self.q_text_icon_button)

        self.q_text_icon_button_checked = QPushButton(self.q_frame)
        self.q_text_icon_button_checked.setObjectName(u"q_text_icon_button_checked")
        self.q_text_icon_button_checked.setIcon(icon)
        self.q_text_icon_button_checked.setCheckable(True)
        self.q_text_icon_button_checked.setChecked(True)
        self.q_text_icon_button_checked.setFlat(False)

        self.horizontalLayout_19.addWidget(self.q_text_icon_button_checked)

        self.q_text_icon_button_disabled = QPushButton(self.q_frame)
        self.q_text_icon_button_disabled.setObjectName(u"q_text_icon_button_disabled")
        self.q_text_icon_button_disabled.setEnabled(False)
        self.q_text_icon_button_disabled.setIcon(icon)

        self.horizontalLayout_19.addWidget(self.q_text_icon_button_disabled)

        self.q_text_icon_button_disabled_checked = QPushButton(self.q_frame)
        self.q_text_icon_button_disabled_checked.setObjectName(u"q_text_icon_button_disabled_checked")
        self.q_text_icon_button_disabled_checked.setEnabled(False)
        self.q_text_icon_button_disabled_checked.setIcon(icon)
        self.q_text_icon_button_disabled_checked.setCheckable(True)
        self.q_text_icon_button_disabled_checked.setChecked(True)

        self.horizontalLayout_19.addWidget(self.q_text_icon_button_disabled_checked)


        self.q_widgets_sub_layout.addLayout(self.horizontalLayout_19)

        self.q_button_layout = QHBoxLayout()
        self.q_button_layout.setObjectName(u"q_button_layout")
        self.q_button = QPushButton(self.q_frame)
        self.q_button.setObjectName(u"q_button")
        sizePolicy.setHeightForWidth(self.q_button.sizePolicy().hasHeightForWidth())
        self.q_button.setSizePolicy(sizePolicy)
        self.q_button.setMaximumSize(QSize(24, 24))
        icon1 = QIcon()
        icon1.addFile(u"../../hwidgets/icons/settings_FILL0_wght400_GRAD0_opsz24.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.q_button.setIcon(icon1)
        self.q_button.setIconSize(QSize(24, 24))
        self.q_button.setFlat(True)

        self.q_button_layout.addWidget(self.q_button)

        self.q_button_checked = QPushButton(self.q_frame)
        self.q_button_checked.setObjectName(u"q_button_checked")
        self.q_button_checked.setMaximumSize(QSize(24, 24))
        self.q_button_checked.setIcon(icon1)
        self.q_button_checked.setIconSize(QSize(24, 24))
        self.q_button_checked.setCheckable(True)
        self.q_button_checked.setChecked(True)
        self.q_button_checked.setFlat(True)

        self.q_button_layout.addWidget(self.q_button_checked)

        self.q_button_disabled = QPushButton(self.q_frame)
        self.q_button_disabled.setObjectName(u"q_button_disabled")
        self.q_button_disabled.setEnabled(False)
        self.q_button_disabled.setMaximumSize(QSize(24, 24))
        self.q_button_disabled.setIcon(icon1)
        self.q_button_disabled.setIconSize(QSize(24, 24))
        self.q_button_disabled.setFlat(True)

        self.q_button_layout.addWidget(self.q_button_disabled)

        self.q_button_disabled_checked = QPushButton(self.q_frame)
        self.q_button_disabled_checked.setObjectName(u"q_button_disabled_checked")
        self.q_button_disabled_checked.setEnabled(False)
        self.q_button_disabled_checked.setMaximumSize(QSize(24, 24))
        self.q_button_disabled_checked.setIcon(icon1)
        self.q_button_disabled_checked.setIconSize(QSize(24, 24))
        self.q_button_disabled_checked.setCheckable(True)
        self.q_button_disabled_checked.setChecked(True)
        self.q_button_disabled_checked.setFlat(True)

        self.q_button_layout.addWidget(self.q_button_disabled_checked)

        self.q_button_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.q_button_layout.addItem(self.q_button_spacer)


        self.q_widgets_sub_layout.addLayout(self.q_button_layout)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(-1, -1, -1, 60)

        self.q_widgets_sub_layout.addLayout(self.horizontalLayout_22)

        self.q_frame_layout = QHBoxLayout()
        self.q_frame_layout.setObjectName(u"q_frame_layout")
        self.q_frame_noframe = QFrame(self.q_frame)
        self.q_frame_noframe.setObjectName(u"q_frame_noframe")
        self.q_frame_noframe.setFrameShape(QFrame.Shape.NoFrame)
        self.q_frame_noframe.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayout_8 = QVBoxLayout(self.q_frame_noframe)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.q_label_1 = QLabel(self.q_frame_noframe)
        self.q_label_1.setObjectName(u"q_label_1")

        self.verticalLayout_8.addWidget(self.q_label_1)


        self.q_frame_layout.addWidget(self.q_frame_noframe)

        self.q_frame_styled_raised = QFrame(self.q_frame)
        self.q_frame_styled_raised.setObjectName(u"q_frame_styled_raised")
        self.q_frame_styled_raised.setFrameShape(QFrame.Shape.StyledPanel)
        self.q_frame_styled_raised.setFrameShadow(QFrame.Shadow.Plain)
        self.verticalLayout_9 = QVBoxLayout(self.q_frame_styled_raised)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.q_label_0 = QLabel(self.q_frame_styled_raised)
        self.q_label_0.setObjectName(u"q_label_0")
        self.q_label_0.setFrameShape(QFrame.Shape.StyledPanel)

        self.verticalLayout_9.addWidget(self.q_label_0)


        self.q_frame_layout.addWidget(self.q_frame_styled_raised)


        self.q_widgets_sub_layout.addLayout(self.q_frame_layout)

        self.q_groupbox_layout = QHBoxLayout()
        self.q_groupbox_layout.setObjectName(u"q_groupbox_layout")
        self.q_groupbox = QGroupBox(self.q_frame)
        self.q_groupbox.setObjectName(u"q_groupbox")
        self.verticalLayout_6 = QVBoxLayout(self.q_groupbox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.q_label_groupbox = QLabel(self.q_groupbox)
        self.q_label_groupbox.setObjectName(u"q_label_groupbox")

        self.verticalLayout_6.addWidget(self.q_label_groupbox)


        self.q_groupbox_layout.addWidget(self.q_groupbox)

        self.q_groupbox_disabled = QGroupBox(self.q_frame)
        self.q_groupbox_disabled.setObjectName(u"q_groupbox_disabled")
        self.q_groupbox_disabled.setEnabled(False)
        self.q_groupbox_disabled.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.verticalLayout_7 = QVBoxLayout(self.q_groupbox_disabled)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.q_label_groupbox_2 = QLabel(self.q_groupbox_disabled)
        self.q_label_groupbox_2.setObjectName(u"q_label_groupbox_2")

        self.verticalLayout_7.addWidget(self.q_label_groupbox_2)


        self.q_groupbox_layout.addWidget(self.q_groupbox_disabled)


        self.q_widgets_sub_layout.addLayout(self.q_groupbox_layout)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.q_lineedit_editable = QLineEdit(self.q_frame)
        self.q_lineedit_editable.setObjectName(u"q_lineedit_editable")
        self.q_lineedit_editable.setClearButtonEnabled(False)

        self.horizontalLayout_16.addWidget(self.q_lineedit_editable)

        self.q_lineedit_editable_clear_button = QLineEdit(self.q_frame)
        self.q_lineedit_editable_clear_button.setObjectName(u"q_lineedit_editable_clear_button")
        self.q_lineedit_editable_clear_button.setClearButtonEnabled(True)

        self.horizontalLayout_16.addWidget(self.q_lineedit_editable_clear_button)

        self.q_lineedit_disabled = QLineEdit(self.q_frame)
        self.q_lineedit_disabled.setObjectName(u"q_lineedit_disabled")
        self.q_lineedit_disabled.setEnabled(False)
        self.q_lineedit_disabled.setClearButtonEnabled(True)

        self.horizontalLayout_16.addWidget(self.q_lineedit_disabled)

        self.q_lineedit_read_only = QLineEdit(self.q_frame)
        self.q_lineedit_read_only.setObjectName(u"q_lineedit_read_only")
        self.q_lineedit_read_only.setReadOnly(True)
        self.q_lineedit_read_only.setClearButtonEnabled(True)

        self.horizontalLayout_16.addWidget(self.q_lineedit_read_only)


        self.q_widgets_sub_layout.addLayout(self.horizontalLayout_16)

        self.q_plaintextedit_layout = QHBoxLayout()
        self.q_plaintextedit_layout.setObjectName(u"q_plaintextedit_layout")
        self.q_plaintextedit_editable = QPlainTextEdit(self.q_frame)
        self.q_plaintextedit_editable.setObjectName(u"q_plaintextedit_editable")
        self.q_plaintextedit_editable.setMaximumSize(QSize(100, 150))

        self.q_plaintextedit_layout.addWidget(self.q_plaintextedit_editable)

        self.q_plaintextedit_editable_vscrollbar = QPlainTextEdit(self.q_frame)
        self.q_plaintextedit_editable_vscrollbar.setObjectName(u"q_plaintextedit_editable_vscrollbar")
        self.q_plaintextedit_editable_vscrollbar.setMaximumSize(QSize(100, 150))

        self.q_plaintextedit_layout.addWidget(self.q_plaintextedit_editable_vscrollbar)

        self.q_plaintextedit_editable_scrollbars = QPlainTextEdit(self.q_frame)
        self.q_plaintextedit_editable_scrollbars.setObjectName(u"q_plaintextedit_editable_scrollbars")
        self.q_plaintextedit_editable_scrollbars.setMaximumSize(QSize(150, 150))
        self.q_plaintextedit_editable_scrollbars.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.q_plaintextedit_layout.addWidget(self.q_plaintextedit_editable_scrollbars)

        self.q_plaintextedit_readonly = QPlainTextEdit(self.q_frame)
        self.q_plaintextedit_readonly.setObjectName(u"q_plaintextedit_readonly")
        self.q_plaintextedit_readonly.setMaximumSize(QSize(100, 150))
        self.q_plaintextedit_readonly.setReadOnly(True)

        self.q_plaintextedit_layout.addWidget(self.q_plaintextedit_readonly)

        self.q_plaintextedit_disabled = QPlainTextEdit(self.q_frame)
        self.q_plaintextedit_disabled.setObjectName(u"q_plaintextedit_disabled")
        self.q_plaintextedit_disabled.setEnabled(False)
        self.q_plaintextedit_disabled.setMaximumSize(QSize(100, 150))

        self.q_plaintextedit_layout.addWidget(self.q_plaintextedit_disabled)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.q_plaintextedit_layout.addItem(self.horizontalSpacer_5)


        self.q_widgets_sub_layout.addLayout(self.q_plaintextedit_layout)

        self.q_spinbox_layout = QHBoxLayout()
        self.q_spinbox_layout.setObjectName(u"q_spinbox_layout")
        self.q_spinbox_no_button = QSpinBox(self.q_frame)
        self.q_spinbox_no_button.setObjectName(u"q_spinbox_no_button")
        self.q_spinbox_no_button.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.q_spinbox_no_button.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.q_spinbox_layout.addWidget(self.q_spinbox_no_button)

        self.q_spinbox_rw = QSpinBox(self.q_frame)
        self.q_spinbox_rw.setObjectName(u"q_spinbox_rw")
        self.q_spinbox_rw.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.q_spinbox_rw.setMinimum(10)

        self.q_spinbox_layout.addWidget(self.q_spinbox_rw)

        self.q_spinbox_ro = QSpinBox(self.q_frame)
        self.q_spinbox_ro.setObjectName(u"q_spinbox_ro")
        self.q_spinbox_ro.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.q_spinbox_ro.setReadOnly(True)

        self.q_spinbox_layout.addWidget(self.q_spinbox_ro)

        self.q_spinbox_disabled = QSpinBox(self.q_frame)
        self.q_spinbox_disabled.setObjectName(u"q_spinbox_disabled")
        self.q_spinbox_disabled.setEnabled(False)
        self.q_spinbox_disabled.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.q_spinbox_layout.addWidget(self.q_spinbox_disabled)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.q_spinbox_layout.addItem(self.horizontalSpacer_7)

        self.q_doublespinbox_nobutton = QDoubleSpinBox(self.q_frame)
        self.q_doublespinbox_nobutton.setObjectName(u"q_doublespinbox_nobutton")
        self.q_doublespinbox_nobutton.setFrame(True)
        self.q_doublespinbox_nobutton.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.q_doublespinbox_nobutton.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.q_spinbox_layout.addWidget(self.q_doublespinbox_nobutton)

        self.q_doublespinbox_rw = QDoubleSpinBox(self.q_frame)
        self.q_doublespinbox_rw.setObjectName(u"q_doublespinbox_rw")
        self.q_doublespinbox_rw.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.q_doublespinbox_rw.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.q_doublespinbox_rw.setProperty(u"showGroupSeparator", False)
        self.q_doublespinbox_rw.setDecimals(1)
        self.q_doublespinbox_rw.setMinimum(10.000000000000000)

        self.q_spinbox_layout.addWidget(self.q_doublespinbox_rw)

        self.q_doublespinbox_ro = QDoubleSpinBox(self.q_frame)
        self.q_doublespinbox_ro.setObjectName(u"q_doublespinbox_ro")
        self.q_doublespinbox_ro.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.q_doublespinbox_ro.setReadOnly(True)

        self.q_spinbox_layout.addWidget(self.q_doublespinbox_ro)

        self.q_doublespinbox_disabled = QDoubleSpinBox(self.q_frame)
        self.q_doublespinbox_disabled.setObjectName(u"q_doublespinbox_disabled")
        self.q_doublespinbox_disabled.setEnabled(False)
        self.q_doublespinbox_disabled.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.q_spinbox_layout.addWidget(self.q_doublespinbox_disabled)


        self.q_widgets_sub_layout.addLayout(self.q_spinbox_layout)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(-1, -1, -1, 60)
        self.q_indeterminate_progress = QProgressBar(self.q_frame)
        self.q_indeterminate_progress.setObjectName(u"q_indeterminate_progress")
        self.q_indeterminate_progress.setMaximum(0)
        self.q_indeterminate_progress.setValue(0)

        self.horizontalLayout_11.addWidget(self.q_indeterminate_progress)


        self.q_widgets_sub_layout.addLayout(self.horizontalLayout_11)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.q_widgets_sub_layout.addItem(self.verticalSpacer)


        self.q_widgets_main_layout.addLayout(self.q_widgets_sub_layout)


        self.horizontalLayout.addWidget(self.q_frame)

        self.h_frame = QFrame(self.centralwidget)
        self.h_frame.setObjectName(u"h_frame")
        self.h_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.h_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.h_frame)
        self.horizontalLayout_10.setSpacing(12)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(18, 18, 18, 18)
        self.main_layout = QVBoxLayout()
        self.main_layout.setObjectName(u"main_layout")
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

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.h_subtitles = HLabel(self.h_frame, theme=theme)
        self.h_subtitles.setObjectName(u"h_subtitles")

        self.verticalLayout.addWidget(self.h_subtitles)

        self.h_comment = HLabel(self.h_frame, theme=theme)
        self.h_comment.setObjectName(u"h_comment")
        self.h_comment.setWordWrap(True)

        self.verticalLayout.addWidget(self.h_comment)


        self.main_layout.addLayout(self.verticalLayout)

        self.h_divider = HDivider(self.h_frame, theme=theme)
        self.h_divider.setObjectName(u"h_divider")
        self.h_divider.setFrameShape(QFrame.Shape.HLine)
        self.h_divider.setFrameShadow(QFrame.Shadow.Sunken)

        self.main_layout.addWidget(self.h_divider)

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

        self.verticalSpacer_2 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.main_layout.addItem(self.verticalSpacer_2)


        self.horizontalLayout_10.addLayout(self.main_layout)


        self.horizontalLayout.addWidget(self.h_frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.q_lineedit_editable_3.setText(QCoreApplication.translate("MainWindow", u"Editable", None))
        self.q_radiobutton_1.setText("")
        self.q_radiobutton_2.setText("")
        self.q_radiobutton_disabled_1.setText("")
        self.q_radiobutton_disabled_2.setText("")
        self.q_label.setText(QCoreApplication.translate("MainWindow", u"A Qlabel", None))
        self.q_label_disabled.setText(QCoreApplication.translate("MainWindow", u"A disabled Qlabel", None))
        self.q_label_checkbox.setText(QCoreApplication.translate("MainWindow", u"A Qlabel", None))
        self.q_checkbox.setText("")
        self.q_checkbox_clicked.setText("")
        self.q_checkbox_disabled.setText("")
        self.q_checkbox_disabled_clicked.setText("")
        self.q_text_button.setText(QCoreApplication.translate("MainWindow", u"QButton", None))
        self.q_text_button_checked.setText(QCoreApplication.translate("MainWindow", u"QButton (C)", None))
        self.q_text_button_disabled.setText(QCoreApplication.translate("MainWindow", u"QButton (D)", None))
        self.q_text_button_checked_disabled.setText(QCoreApplication.translate("MainWindow", u"QButton (C/D)", None))
        self.q_text_icon_button.setText(QCoreApplication.translate("MainWindow", u"qi_button", None))
        self.q_text_icon_button_checked.setText(QCoreApplication.translate("MainWindow", u"qi_button (checked)", None))
        self.q_text_icon_button_disabled.setText(QCoreApplication.translate("MainWindow", u"qi_button (disabled)", None))
        self.q_text_icon_button_disabled_checked.setText(QCoreApplication.translate("MainWindow", u"qi_button (Checked Disabled)", None))
        self.q_button.setText("")
        self.q_button_checked.setText("")
        self.q_button_disabled.setText("")
        self.q_button_disabled_checked.setText("")
        self.q_label_1.setText(QCoreApplication.translate("MainWindow", u"no frame, plain", None))
        self.q_label_0.setText(QCoreApplication.translate("MainWindow", u"no frame, styled", None))
        self.q_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"QGroupBox", None))
        self.q_label_groupbox.setText(QCoreApplication.translate("MainWindow", u"A Qlabel", None))
        self.q_groupbox_disabled.setTitle(QCoreApplication.translate("MainWindow", u"QGroupBox (disabled)", None))
        self.q_label_groupbox_2.setText(QCoreApplication.translate("MainWindow", u"A Qlabel", None))
        self.q_lineedit_editable.setText(QCoreApplication.translate("MainWindow", u"Editable", None))
        self.q_lineedit_editable_clear_button.setText(QCoreApplication.translate("MainWindow", u"Editable with clear button", None))
        self.q_lineedit_disabled.setText(QCoreApplication.translate("MainWindow", u"Disabled", None))
        self.q_lineedit_read_only.setText(QCoreApplication.translate("MainWindow", u"ReadOnly", None))
        self.q_plaintextedit_editable.setPlainText(QCoreApplication.translate("MainWindow", u"editable\n"
"sdsdc", None))
        self.q_plaintextedit_editable_vscrollbar.setPlainText(QCoreApplication.translate("MainWindow", u"editable\n"
"multiple lines\n"
"for scrollbar\n"
"with test\n"
"", None))
        self.q_plaintextedit_editable_scrollbars.setPlainText(QCoreApplication.translate("MainWindow", u"editable\n"
"multiple lines with very large text for hscrollbar\n"
"for scrollbar \n"
"with test\n"
"and\n"
"a lot\n"
"of vertical text\n"
"", None))
        self.q_plaintextedit_readonly.setPlainText(QCoreApplication.translate("MainWindow", u"read only\n"
"", None))
        self.q_plaintextedit_disabled.setPlainText(QCoreApplication.translate("MainWindow", u"disabled\n"
"", None))
        self.h_label.setText(QCoreApplication.translate("MainWindow", u"A Hlabel", None))
        self.h_label_disabled.setText(QCoreApplication.translate("MainWindow", u"A disabled Hlabel", None))
        self.h_subtitles.setText(QCoreApplication.translate("MainWindow", u"Subtitle", None))
        self.h_comment.setText(QCoreApplication.translate("MainWindow", u"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", None))
        self.h_title.setText(QCoreApplication.translate("MainWindow", u"This is a HTitle widget without icon", None))
        self.h_title_icon.setText("")
    # retranslateUi

