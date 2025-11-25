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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout,
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
    HComment,
    HDescription,
    HDivider,
    HHorizontalDivider,
    HIndeterminateCircularProgress,
    HIndeterminateProgress,
    HProgress,
    HRadialProgress,
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
        MainWindow.resize(1000, 860)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
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

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.h_subtitles = HSubtitle(self.h_frame, theme=theme)
        self.h_subtitles.setObjectName(u"h_subtitles")

        self.verticalLayout.addWidget(self.h_subtitles)

        self.h_description = HDescription(self.h_frame, theme=theme)
        self.h_description.setObjectName(u"h_description")
        self.h_description.setWordWrap(True)

        self.verticalLayout.addWidget(self.h_description)

        self.h_comment_bold = HComment(self.h_frame, theme=theme)
        self.h_comment_bold.setObjectName(u"h_comment_bold")
        self.h_comment_bold.setWordWrap(True)

        self.verticalLayout.addWidget(self.h_comment_bold)

        self.h_comment_italic = HComment(self.h_frame, theme=theme)
        self.h_comment_italic.setObjectName(u"h_comment_italic")
        self.h_comment_italic.setWordWrap(True)

        self.verticalLayout.addWidget(self.h_comment_italic)

        self.h_comment_small_italic = HComment(self.h_frame, theme=theme)
        self.h_comment_small_italic.setObjectName(u"h_comment_small_italic")
        self.h_comment_small_italic.setWordWrap(True)

        self.verticalLayout.addWidget(self.h_comment_small_italic)


        self.main_layout.addLayout(self.verticalLayout)

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

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.h_checkbox = HCheckBox(self.h_frame, theme=theme)
        self.h_checkbox.setObjectName(u"h_checkbox")

        self.horizontalLayout_4.addWidget(self.h_checkbox)

        self.h_checkbox_clicked = HCheckBox(self.h_frame, theme=theme)
        self.h_checkbox_clicked.setObjectName(u"h_checkbox_clicked")
        self.h_checkbox_clicked.setChecked(True)

        self.horizontalLayout_4.addWidget(self.h_checkbox_clicked)

        self.h_checkbox_disabled = HCheckBox(self.h_frame, theme=theme)
        self.h_checkbox_disabled.setObjectName(u"h_checkbox_disabled")
        self.h_checkbox_disabled.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.h_checkbox_disabled)

        self.h_checkbox_disabled_clicked = HCheckBox(self.h_frame, theme=theme)
        self.h_checkbox_disabled_clicked.setObjectName(u"h_checkbox_disabled_clicked")
        self.h_checkbox_disabled_clicked.setEnabled(False)
        self.h_checkbox_disabled_clicked.setChecked(True)

        self.horizontalLayout_4.addWidget(self.h_checkbox_disabled_clicked)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.h_switch = HSwitch(self.h_frame, theme=theme)
        self.h_switch.setObjectName(u"h_switch")

        self.horizontalLayout_4.addWidget(self.h_switch)

        self.h_switch_checked = HSwitch(self.h_frame, theme=theme)
        self.h_switch_checked.setObjectName(u"h_switch_checked")
        self.h_switch_checked.setChecked(True)

        self.horizontalLayout_4.addWidget(self.h_switch_checked)

        self.h_switch_disabled = HSwitch(self.h_frame, theme=theme)
        self.h_switch_disabled.setObjectName(u"h_switch_disabled")
        self.h_switch_disabled.setEnabled(False)
        self.h_switch_disabled.setCheckable(True)

        self.horizontalLayout_4.addWidget(self.h_switch_disabled)

        self.h_switch_disabled_checked = HSwitch(self.h_frame, theme=theme)
        self.h_switch_disabled_checked.setObjectName(u"h_switch_disabled_checked")
        self.h_switch_disabled_checked.setEnabled(False)
        self.h_switch_disabled_checked.setChecked(True)

        self.horizontalLayout_4.addWidget(self.h_switch_disabled_checked)


        self.main_layout.addLayout(self.horizontalLayout_4)

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
        self.h_title.setText(QCoreApplication.translate("MainWindow", u"This is a HTitle widget without icon", None))
        self.h_title_icon.setText("")
        self.h_subtitles.setText(QCoreApplication.translate("MainWindow", u"Subtitle", None))
        self.h_description.setText(QCoreApplication.translate("MainWindow", u"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", None))
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
    # retranslateUi

