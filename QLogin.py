# -- coding: utf-8 --

from PyQt5.QtWidgets import QLineEdit,QDialogButtonBox,QFormLayout,QDialog,QMessageBox
from PyQt5 import QtWidgets,QtCore
import qdarkstyle
import pyodbc


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super(LoginDialog,self).__init__(parent)
        self.init_ui()


    def init_ui(self):

        ### delete question mark
        self.setWindowFlags(self.windowFlags()
                            ^ QtCore.Qt.WindowContextHelpButtonHint)

        ### login & password fields
        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)

        loginLayout = QFormLayout()
        loginLayout.addRow('Username', self.username)
        loginLayout.addRow('Password', self.password)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.control)
        self.buttons.rejected.connect(self.reject)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(loginLayout)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

        ### set window title & stylesheet
        self.setWindowTitle('Villain - 10.96.6.14 ')
        #self.setWindowIcon(QtGui.QIcon('dc1.png'))
        self.setStyleSheet((qdarkstyle.load_stylesheet_pyqt5()))
        ###lock resize
        self.setSizeGripEnabled(False)
        self.setFixedSize(self.sizeHint())


    def credentials(self):
        return self.username.text(), self.password.text()


    ###log by usins sql credentials
    def control(self):
        ser = '10.96.6.14'
        base = 'PROD_WAREX2'
        login = self.username.text()
        pwd = self.password.text()

        try:
            self.connection = pyodbc.connect(driver='{SQL Server}', server=ser, database=base,
                         user=login, password=pwd)
            cursor = self.connection.cursor()
            cursor.close()
            self.accept()
        except:
            QMessageBox.warning(self, 'Error', 'Wrong username or password! \n\n'
                                               'Please use the SQL Server credentials ')

