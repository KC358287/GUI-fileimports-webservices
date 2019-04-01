#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtWidgets
from QFilesTab import Files
from QWebservicesTab import Webservices
import qdarkstyle


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.task_bar()
        self.graph_elements()
        self.center()

    def task_bar(self):
        exitAct = QtWidgets.QAction('&Exit', self, shortcut='Ctrl+Q', statusTip='Exit application')
        exitAct.triggered.connect(self.close)
        moreinfo = QtWidgets.QAction('&Help', self, statusTip='More information')
        moreinfo.triggered.connect(self.information)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        fileMenu = menubar.addMenu('&Help')
        fileMenu.addAction(moreinfo)

    def graph_elements(self):
        self.setWindowTitle('Villain')
        self.setWindowIcon(QtGui.QIcon('dc1.png'))
        self.setStyleSheet((qdarkstyle.load_stylesheet_pyqt5()))

    def tab(self, credentials):
        self.tabwidget = QtWidgets.QTabWidget()
        self.tabwidget.addTab(Files(credentials), 'Files Import')
        self.tabwidget.addTab(Webservices(), 'Webservice')
        self.setCentralWidget(self.tabwidget)

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def information(self):
        QtWidgets.QMessageBox.information(self,'Information','Version: 2.0\n'\
                                            'Please, contact karol.chojnowski@digitalcaregroup.com for comments and suggestions\n\n'\
                                          'Digital Care - Data Processing Team')








