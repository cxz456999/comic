# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Spider.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from CatchHtml import CatchHtml

class Ui_MainWindow(object):
    def checkC(self):
        if len(self.beginIndex.text()) == 0 or len(self.endIndex.text()) == 0 or int(self.beginIndex.text()) > int(self.endIndex.text()):
            self.showStatus.setText('頁數出錯')
            return
        self.GoButton.setEnabled(False)
        #self.Keyword.setText('44444')
        self.catcher.start(self.Keyword.text(), int(self.beginIndex.text()), int(self.endIndex.text()))
        #self.textEdit.append('發生Error')
        #print(self.beginIndex.text())
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(518, 377)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 12, 501, 321))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Keyword = QtWidgets.QLineEdit(self.widget)
        self.Keyword.setObjectName("Keyword")
        self.horizontalLayout_2.addWidget(self.Keyword)
        self.GoButton = QtWidgets.QPushButton(self.widget)
        self.GoButton.setObjectName("GoButton")
        ############## GoButton Event #########################
        self.GoButton.clicked.connect(self.checkC)
        ##############################################################
        self.horizontalLayout_2.addWidget(self.GoButton)
        self.showStatus = QtWidgets.QLabel(self.widget)
        self.showStatus.setMinimumSize(QtCore.QSize(250, 0))
        self.showStatus.setObjectName("showStatus")
        self.horizontalLayout_2.addWidget(self.showStatus)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.beginIndex = QtWidgets.QLineEdit(self.widget)
        self.beginIndex.setMaximumSize(QtCore.QSize(50, 16777215))
        self.beginIndex.setObjectName("beginIndex")
        ###### add
        self.beginIndex.setValidator(QtGui.QIntValidator(1, 999))
        ######
        self.horizontalLayout_3.addWidget(self.beginIndex)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.endIndex = QtWidgets.QLineEdit(self.widget)
        self.endIndex.setMaximumSize(QtCore.QSize(50, 16777215))
        self.endIndex.setObjectName("endIndex")
        ###### add
        self.endIndex.setValidator(QtGui.QIntValidator(1, 999))
        ######
        self.horizontalLayout_3.addWidget(self.endIndex)
        self.downloadImg = QtWidgets.QCheckBox(self.widget)
        self.downloadImg.setObjectName("downloadImg")
        self.horizontalLayout_3.addWidget(self.downloadImg)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.GoButton.raise_()
        self.Keyword.raise_()
        self.beginIndex.raise_()
        self.endIndex.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.textEdit.raise_()
        self.GoButton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 518, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.catcher = CatchHtml(self)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BIDO_Spider"))
        self.GoButton.setText(_translate("MainWindow", "Go"))
        self.showStatus.setText(_translate("MainWindow", "尚未開始"))
        self.label.setText(_translate("MainWindow", "起始頁數"))
        self.label_2.setText(_translate("MainWindow", "結束頁數"))
        self.downloadImg.setText(_translate("MainWindow", "下載圖片"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

