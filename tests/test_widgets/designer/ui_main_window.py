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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPlainTextEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from hwidgets import (
    HButton,
    HCheckBox,
    HComboBox,
    HGroupBox,
    HLabel,
    HLineEdit,
    HPlainTextEdit,
    HRadioButton,
    HStyle,
)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, hstyle: HStyle):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1358, 723)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.q_frame = QFrame(self.centralwidget)
        self.q_frame.setObjectName(u"q_frame")
        self.q_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.q_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.q_frame)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(18, 18, 18, 18)
        self.q_combobox_layout = QVBoxLayout()
        self.q_combobox_layout.setObjectName(u"q_combobox_layout")
        self.q_combobox_rw = QComboBox(self.q_frame)
        self.q_combobox_rw.setObjectName(u"q_combobox_rw")

        self.q_combobox_layout.addWidget(self.q_combobox_rw)

        self.q_combobox_read_only = QComboBox(self.q_frame)
        self.q_combobox_read_only.setObjectName(u"q_combobox_read_only")
        self.q_combobox_read_only.setEditable(True)

        self.q_combobox_layout.addWidget(self.q_combobox_read_only)

        self.q_combobox_disabled = QComboBox(self.q_frame)
        self.q_combobox_disabled.setObjectName(u"q_combobox_disabled")
        self.q_combobox_disabled.setEnabled(False)
        self.q_combobox_disabled.setEditable(True)

        self.q_combobox_layout.addWidget(self.q_combobox_disabled)


        self.verticalLayout.addLayout(self.q_combobox_layout)

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


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, -1, -1, 20)
        self.q_label = QLabel(self.q_frame)
        self.q_label.setObjectName(u"q_label")

        self.horizontalLayout_7.addWidget(self.q_label)

        self.q_label_disabled = QLabel(self.q_frame)
        self.q_label_disabled.setObjectName(u"q_label_disabled")
        self.q_label_disabled.setEnabled(False)

        self.horizontalLayout_7.addWidget(self.q_label_disabled)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

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


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.q_button = QPushButton(self.q_frame)
        self.q_button.setObjectName(u"q_button")

        self.horizontalLayout_9.addWidget(self.q_button)

        self.q_button_checked = QPushButton(self.q_frame)
        self.q_button_checked.setObjectName(u"q_button_checked")
        self.q_button_checked.setCheckable(True)
        self.q_button_checked.setChecked(True)

        self.horizontalLayout_9.addWidget(self.q_button_checked)

        self.q_button_disabled = QPushButton(self.q_frame)
        self.q_button_disabled.setObjectName(u"q_button_disabled")
        self.q_button_disabled.setEnabled(False)

        self.horizontalLayout_9.addWidget(self.q_button_disabled)

        self.q_button_checked_disabled = QPushButton(self.q_frame)
        self.q_button_checked_disabled.setObjectName(u"q_button_checked_disabled")
        self.q_button_checked_disabled.setEnabled(False)
        self.q_button_checked_disabled.setCheckable(True)
        self.q_button_checked_disabled.setChecked(True)

        self.horizontalLayout_9.addWidget(self.q_button_checked_disabled)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

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
        self.q_groupbox_disabled.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.verticalLayout_7 = QVBoxLayout(self.q_groupbox_disabled)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.q_label_groupbox_2 = QLabel(self.q_groupbox_disabled)
        self.q_label_groupbox_2.setObjectName(u"q_label_groupbox_2")

        self.verticalLayout_7.addWidget(self.q_label_groupbox_2)


        self.q_groupbox_layout.addWidget(self.q_groupbox_disabled)


        self.verticalLayout.addLayout(self.q_groupbox_layout)

        self.htextedit_layout_2 = QVBoxLayout()
        self.htextedit_layout_2.setObjectName(u"htextedit_layout_2")
        self.q_lineedit_editable = QLineEdit(self.q_frame)
        self.q_lineedit_editable.setObjectName(u"q_lineedit_editable")
        self.q_lineedit_editable.setClearButtonEnabled(False)

        self.htextedit_layout_2.addWidget(self.q_lineedit_editable)

        self.q_lineedit_editable_clear_button = QLineEdit(self.q_frame)
        self.q_lineedit_editable_clear_button.setObjectName(u"q_lineedit_editable_clear_button")
        self.q_lineedit_editable_clear_button.setClearButtonEnabled(True)

        self.htextedit_layout_2.addWidget(self.q_lineedit_editable_clear_button)

        self.q_lineedit_read_only = QLineEdit(self.q_frame)
        self.q_lineedit_read_only.setObjectName(u"q_lineedit_read_only")
        self.q_lineedit_read_only.setReadOnly(True)
        self.q_lineedit_read_only.setClearButtonEnabled(True)

        self.htextedit_layout_2.addWidget(self.q_lineedit_read_only)

        self.q_lineedit_disabled = QLineEdit(self.q_frame)
        self.q_lineedit_disabled.setObjectName(u"q_lineedit_disabled")
        self.q_lineedit_disabled.setEnabled(False)
        self.q_lineedit_disabled.setClearButtonEnabled(True)

        self.htextedit_layout_2.addWidget(self.q_lineedit_disabled)


        self.verticalLayout.addLayout(self.htextedit_layout_2)

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


        self.verticalLayout.addLayout(self.q_plaintextedit_layout)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.q_frame)

        self.h_frame = QFrame(self.centralwidget)
        self.h_frame.setObjectName(u"h_frame")
        self.h_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.h_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.h_frame)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(18, 18, 18, 18)
        self.h_combobox_layout = QVBoxLayout()
        self.h_combobox_layout.setObjectName(u"h_combobox_layout")
        self.h_combobox_rw = HComboBox(self.h_frame, hstyle=hstyle)
        self.h_combobox_rw.setObjectName(u"h_combobox_rw")

        self.h_combobox_layout.addWidget(self.h_combobox_rw)

        self.h_combobox_read_only = HComboBox(self.h_frame, hstyle=hstyle)
        self.h_combobox_read_only.setObjectName(u"h_combobox_read_only")
        self.h_combobox_read_only.setEditable(True)

        self.h_combobox_layout.addWidget(self.h_combobox_read_only)

        self.h_combobox_disabled = HComboBox(self.h_frame, hstyle=hstyle)
        self.h_combobox_disabled.setObjectName(u"h_combobox_disabled")
        self.h_combobox_disabled.setEnabled(False)
        self.h_combobox_disabled.setEditable(True)

        self.h_combobox_layout.addWidget(self.h_combobox_disabled)


        self.verticalLayout_2.addLayout(self.h_combobox_layout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.h_radiobutton_2 = HRadioButton(self.h_frame, hstyle=hstyle)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.h_radiobutton_2)
        self.h_radiobutton_2.setObjectName(u"h_radiobutton_2")
        self.h_radiobutton_2.setChecked(True)

        self.horizontalLayout_2.addWidget(self.h_radiobutton_2)

        self.h_radiobutton_1 = HRadioButton(self.h_frame, hstyle=hstyle)
        self.buttonGroup.addButton(self.h_radiobutton_1)
        self.h_radiobutton_1.setObjectName(u"h_radiobutton_1")

        self.horizontalLayout_2.addWidget(self.h_radiobutton_1)

        self.h_radiobutton_disabled_1 = HRadioButton(self.h_frame, hstyle=hstyle)
        self.buttonGroup_2 = QButtonGroup(MainWindow)
        self.buttonGroup_2.setObjectName(u"buttonGroup_2")
        self.buttonGroup_2.addButton(self.h_radiobutton_disabled_1)
        self.h_radiobutton_disabled_1.setObjectName(u"h_radiobutton_disabled_1")
        self.h_radiobutton_disabled_1.setEnabled(False)
        self.h_radiobutton_disabled_1.setChecked(True)

        self.horizontalLayout_2.addWidget(self.h_radiobutton_disabled_1)

        self.h_radiobutton_disabled_2 = HRadioButton(self.h_frame, hstyle=hstyle)
        self.buttonGroup_2.addButton(self.h_radiobutton_disabled_2)
        self.h_radiobutton_disabled_2.setObjectName(u"h_radiobutton_disabled_2")
        self.h_radiobutton_disabled_2.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.h_radiobutton_disabled_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, -1, -1, 20)
        self.h_label = HLabel(self.h_frame, hstyle=hstyle)
        self.h_label.setObjectName(u"h_label")

        self.horizontalLayout_6.addWidget(self.h_label)

        self.h_label_disabled = HLabel(self.h_frame, hstyle=hstyle)
        self.h_label_disabled.setObjectName(u"h_label_disabled")
        self.h_label_disabled.setEnabled(False)

        self.horizontalLayout_6.addWidget(self.h_label_disabled)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.h_label_checkbox = HLabel(self.h_frame, hstyle=hstyle)
        self.h_label_checkbox.setObjectName(u"h_label_checkbox")

        self.horizontalLayout_4.addWidget(self.h_label_checkbox)

        self.h_checkbox = HCheckBox(self.h_frame, hstyle=hstyle)
        self.h_checkbox.setObjectName(u"h_checkbox")

        self.horizontalLayout_4.addWidget(self.h_checkbox)

        self.h_checkbox_clicked = HCheckBox(self.h_frame, hstyle=hstyle)
        self.h_checkbox_clicked.setObjectName(u"h_checkbox_clicked")
        self.h_checkbox_clicked.setChecked(True)

        self.horizontalLayout_4.addWidget(self.h_checkbox_clicked)

        self.h_checkbox_disabled = HCheckBox(self.h_frame, hstyle=hstyle)
        self.h_checkbox_disabled.setObjectName(u"h_checkbox_disabled")
        self.h_checkbox_disabled.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.h_checkbox_disabled)

        self.h_checkbox_disabled_clicked = HCheckBox(self.h_frame, hstyle=hstyle)
        self.h_checkbox_disabled_clicked.setObjectName(u"h_checkbox_disabled_clicked")
        self.h_checkbox_disabled_clicked.setEnabled(False)
        self.h_checkbox_disabled_clicked.setChecked(True)

        self.horizontalLayout_4.addWidget(self.h_checkbox_disabled_clicked)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.h_button = HButton(self.h_frame, hstyle=hstyle)
        self.h_button.setObjectName(u"h_button")

        self.horizontalLayout_8.addWidget(self.h_button)

        self.h_button_checked = HButton(self.h_frame, hstyle=hstyle)
        self.h_button_checked.setObjectName(u"h_button_checked")
        self.h_button_checked.setCheckable(True)
        self.h_button_checked.setChecked(True)

        self.horizontalLayout_8.addWidget(self.h_button_checked)

        self.h_button_disabled = HButton(self.h_frame, hstyle=hstyle)
        self.h_button_disabled.setObjectName(u"h_button_disabled")
        self.h_button_disabled.setEnabled(False)

        self.horizontalLayout_8.addWidget(self.h_button_disabled)

        self.h_button_checked_disabled = HButton(self.h_frame, hstyle=hstyle)
        self.h_button_checked_disabled.setObjectName(u"h_button_checked_disabled")
        self.h_button_checked_disabled.setEnabled(False)
        self.h_button_checked_disabled.setCheckable(True)
        self.h_button_checked_disabled.setChecked(True)

        self.horizontalLayout_8.addWidget(self.h_button_checked_disabled)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.h_groupbox_layout = QHBoxLayout()
        self.h_groupbox_layout.setObjectName(u"h_groupbox_layout")
        self.h_groupbox = HGroupBox(self.h_frame, hstyle=hstyle)
        self.h_groupbox.setObjectName(u"h_groupbox")
        self.verticalLayout_5 = QVBoxLayout(self.h_groupbox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.h_label_groupbox_1 = HLabel(self.h_groupbox, hstyle=hstyle)
        self.h_label_groupbox_1.setObjectName(u"h_label_groupbox_1")

        self.verticalLayout_5.addWidget(self.h_label_groupbox_1)


        self.h_groupbox_layout.addWidget(self.h_groupbox)

        self.h_groupbox_disabled = HGroupBox(self.h_frame, hstyle=hstyle)
        self.h_groupbox_disabled.setObjectName(u"h_groupbox_disabled")
        self.verticalLayout_4 = QVBoxLayout(self.h_groupbox_disabled)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.h_label_groupbox_2 = HLabel(self.h_groupbox_disabled, hstyle=hstyle)
        self.h_label_groupbox_2.setObjectName(u"h_label_groupbox_2")

        self.verticalLayout_4.addWidget(self.h_label_groupbox_2)


        self.h_groupbox_layout.addWidget(self.h_groupbox_disabled)


        self.verticalLayout_2.addLayout(self.h_groupbox_layout)

        self.htextedit_layout = QVBoxLayout()
        self.htextedit_layout.setObjectName(u"htextedit_layout")
        self.h_lineedit_editable = HLineEdit(self.h_frame, hstyle=hstyle)
        self.h_lineedit_editable.setObjectName(u"h_lineedit_editable")
        self.h_lineedit_editable.setClearButtonEnabled(False)

        self.htextedit_layout.addWidget(self.h_lineedit_editable)

        self.h_lineedit_editable_clear_button = HLineEdit(self.h_frame, hstyle=hstyle)
        self.h_lineedit_editable_clear_button.setObjectName(u"h_lineedit_editable_clear_button")
        self.h_lineedit_editable_clear_button.setClearButtonEnabled(True)

        self.htextedit_layout.addWidget(self.h_lineedit_editable_clear_button)

        self.h_lineedit_read_only = HLineEdit(self.h_frame, hstyle=hstyle)
        self.h_lineedit_read_only.setObjectName(u"h_lineedit_read_only")
        self.h_lineedit_read_only.setReadOnly(True)
        self.h_lineedit_read_only.setClearButtonEnabled(True)

        self.htextedit_layout.addWidget(self.h_lineedit_read_only)

        self.h_lineedit_disabled = HLineEdit(self.h_frame, hstyle=hstyle)
        self.h_lineedit_disabled.setObjectName(u"h_lineedit_disabled")
        self.h_lineedit_disabled.setEnabled(False)
        self.h_lineedit_disabled.setClearButtonEnabled(True)

        self.htextedit_layout.addWidget(self.h_lineedit_disabled)


        self.verticalLayout_2.addLayout(self.htextedit_layout)

        self.h_plaintextedit_layout = QHBoxLayout()
        self.h_plaintextedit_layout.setObjectName(u"h_plaintextedit_layout")
        self.h_plaintextedit_editable = HPlainTextEdit(self.h_frame, hstyle=hstyle)
        self.h_plaintextedit_editable.setObjectName(u"h_plaintextedit_editable")
        self.h_plaintextedit_editable.setMaximumSize(QSize(100, 150))

        self.h_plaintextedit_layout.addWidget(self.h_plaintextedit_editable)

        self.h_plaintextedit_editable_vscrollbar = HPlainTextEdit(self.h_frame, hstyle=hstyle)
        self.h_plaintextedit_editable_vscrollbar.setObjectName(u"h_plaintextedit_editable_vscrollbar")
        self.h_plaintextedit_editable_vscrollbar.setMaximumSize(QSize(100, 150))

        self.h_plaintextedit_layout.addWidget(self.h_plaintextedit_editable_vscrollbar)

        self.h_plaintextedit_editable_scrollbars = HPlainTextEdit(self.h_frame, hstyle=hstyle)
        self.h_plaintextedit_editable_scrollbars.setObjectName(u"h_plaintextedit_editable_scrollbars")
        self.h_plaintextedit_editable_scrollbars.setMaximumSize(QSize(150, 150))
        self.h_plaintextedit_editable_scrollbars.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.h_plaintextedit_layout.addWidget(self.h_plaintextedit_editable_scrollbars)

        self.h_plaintextedit_readonly = HPlainTextEdit(self.h_frame, hstyle=hstyle)
        self.h_plaintextedit_readonly.setObjectName(u"h_plaintextedit_readonly")
        self.h_plaintextedit_readonly.setMaximumSize(QSize(100, 150))
        self.h_plaintextedit_readonly.setReadOnly(True)

        self.h_plaintextedit_layout.addWidget(self.h_plaintextedit_readonly)

        self.h_plaintextedit_disabled = HPlainTextEdit(self.h_frame, hstyle=hstyle)
        self.h_plaintextedit_disabled.setObjectName(u"h_plaintextedit_disabled")
        self.h_plaintextedit_disabled.setEnabled(False)
        self.h_plaintextedit_disabled.setMaximumSize(QSize(100, 150))

        self.h_plaintextedit_layout.addWidget(self.h_plaintextedit_disabled)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.h_plaintextedit_layout.addItem(self.horizontalSpacer_6)


        self.verticalLayout_2.addLayout(self.h_plaintextedit_layout)

        self.verticalSpacer_2 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addWidget(self.h_frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
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
        self.q_button.setText(QCoreApplication.translate("MainWindow", u"QButton", None))
        self.q_button_checked.setText(QCoreApplication.translate("MainWindow", u"QButton (C)", None))
        self.q_button_disabled.setText(QCoreApplication.translate("MainWindow", u"QButton (D)", None))
        self.q_button_checked_disabled.setText(QCoreApplication.translate("MainWindow", u"QButton (C/D)", None))
        self.q_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"QGroupBox", None))
        self.q_label_groupbox.setText(QCoreApplication.translate("MainWindow", u"A Qlabel", None))
        self.q_groupbox_disabled.setTitle(QCoreApplication.translate("MainWindow", u"QGroupBox (disabled)", None))
        self.q_label_groupbox_2.setText(QCoreApplication.translate("MainWindow", u"A Qlabel", None))
        self.q_lineedit_editable.setText(QCoreApplication.translate("MainWindow", u"Editable", None))
        self.q_lineedit_editable_clear_button.setText(QCoreApplication.translate("MainWindow", u"Editable with clear button", None))
        self.q_lineedit_read_only.setText(QCoreApplication.translate("MainWindow", u"ReadOnly", None))
        self.q_lineedit_disabled.setText(QCoreApplication.translate("MainWindow", u"Disabled", None))
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
        self.h_radiobutton_2.setText("")
        self.h_radiobutton_1.setText("")
        self.h_radiobutton_disabled_1.setText("")
        self.h_radiobutton_disabled_2.setText("")
        self.h_label.setText(QCoreApplication.translate("MainWindow", u"A Hlabel", None))
        self.h_label_disabled.setText(QCoreApplication.translate("MainWindow", u"A disabled Hlabel", None))
        self.h_label_checkbox.setText(QCoreApplication.translate("MainWindow", u"A Hlabel", None))
        self.h_checkbox.setText("")
        self.h_checkbox_clicked.setText("")
        self.h_checkbox_disabled.setText("")
        self.h_checkbox_disabled_clicked.setText("")
        self.h_button.setText(QCoreApplication.translate("MainWindow", u"HButton", None))
        self.h_button_checked.setText(QCoreApplication.translate("MainWindow", u"HButton (C)", None))
        self.h_button_disabled.setText(QCoreApplication.translate("MainWindow", u"HButton (D)", None))
        self.h_button_checked_disabled.setText(QCoreApplication.translate("MainWindow", u"HButton (C/D)", None))
        self.h_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"HGroupBox", None))
        self.h_label_groupbox_1.setText(QCoreApplication.translate("MainWindow", u"A Hlabel", None))
        self.h_groupbox_disabled.setTitle(QCoreApplication.translate("MainWindow", u"HGroupBox (disabled)", None))
        self.h_label_groupbox_2.setText(QCoreApplication.translate("MainWindow", u"A Hlabel", None))
        self.h_lineedit_editable.setText(QCoreApplication.translate("MainWindow", u"Editable", None))
        self.h_lineedit_editable_clear_button.setText(QCoreApplication.translate("MainWindow", u"Editable with clear button", None))
        self.h_lineedit_read_only.setText(QCoreApplication.translate("MainWindow", u"ReadOnly", None))
        self.h_lineedit_disabled.setText(QCoreApplication.translate("MainWindow", u"Disabled", None))
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
    # retranslateUi

