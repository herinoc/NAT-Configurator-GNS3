# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QLabel,
    QPushButton, QRadioButton, QSizePolicy, QTextBrowser,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(442, 341)
        self.rdbGns = QRadioButton(Dialog)
        self.rdbGns.setObjectName(u"rdbGns")
        self.rdbGns.setGeometry(QRect(10, 8, 95, 22))
        self.rdbVbox = QRadioButton(Dialog)
        self.rdbVbox.setObjectName(u"rdbVbox")
        self.rdbVbox.setGeometry(QRect(85, 7, 95, 22))
        self.btnActivate = QPushButton(Dialog)
        self.btnActivate.setObjectName(u"btnActivate")
        self.btnActivate.setGeometry(QRect(131, 304, 111, 25))
        self.cbxInterface = QComboBox(Dialog)
        self.cbxInterface.setObjectName(u"cbxInterface")
        self.cbxInterface.setGeometry(QRect(10, 304, 111, 25))
        self.txbDescription = QTextBrowser(Dialog)
        self.txbDescription.setObjectName(u"txbDescription")
        self.txbDescription.setGeometry(QRect(10, 40, 421, 251))
        self.btnRestore = QPushButton(Dialog)
        self.btnRestore.setObjectName(u"btnRestore")
        self.btnRestore.setEnabled(False)
        self.btnRestore.setGeometry(QRect(328, 304, 101, 25))
        self.lbAbout = QLabel(Dialog)
        self.lbAbout.setObjectName(u"lbAbout")
        self.lbAbout.setGeometry(QRect(392, 10, 54, 17))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Nat-SmartConfig", None))
        self.rdbGns.setText(QCoreApplication.translate("Dialog", u"GNS3", None))
        self.rdbVbox.setText(QCoreApplication.translate("Dialog", u"VirtualBox", None))
        self.btnActivate.setText(QCoreApplication.translate("Dialog", u"Activate", None))
#if QT_CONFIG(tooltip)
        self.cbxInterface.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btnRestore.setText(QCoreApplication.translate("Dialog", u"Restore", None))
        self.lbAbout.setText(QCoreApplication.translate("Dialog", u"About", None))
    # retranslateUi

