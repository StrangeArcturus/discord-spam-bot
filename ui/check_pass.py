# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/check_pass.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 160, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 250, 15))
        self.label_2.setObjectName("label_2")
        self.key_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.key_lineEdit.setGeometry(QtCore.QRect(20, 60, 350, 30))
        self.key_lineEdit.setObjectName("key_lineEdit")
        self.status_label = QtWidgets.QLabel(Dialog)
        self.status_label.setGeometry(QtCore.QRect(20, 190, 350, 30))
        self.status_label.setText("")
        self.status_label.setObjectName("status_label")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Проверка пароля"))
        self.label.setText(_translate("Dialog", "Последняя проверка ^-^"))
        self.label_2.setText(_translate("Dialog", "Введите Ваш уникальный пароль ниже"))
