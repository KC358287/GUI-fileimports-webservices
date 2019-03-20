# -- coding: utf-8 --

import sys
from PyQt5 import QtWidgets,QtGui
from QLogin import LoginDialog
from QApp import MainWindow
from QFilesTab import Files
import os


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    login = LoginDialog()
    login.setWindowIcon(QtGui.QIcon(resource_path('dc1.png')))

    if login.exec_() != QtWidgets.QDialog.Accepted:
        sys.exit(-1)

    files = Files()
    window = MainWindow()
    window.setWindowIcon(QtGui.QIcon(resource_path('dc1.png')))
    window.setGeometry(500, 150, 800, 500)
    files.setCredentials(login.credentials())
    window.show()
    sys.exit(app.exec_())



