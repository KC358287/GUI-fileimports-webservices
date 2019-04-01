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
        ### actions on meenubar
        exitAct = QtWidgets.QAction('&Exit', self, shortcut='Ctrl+Q', statusTip='Exit application')
        exitAct.triggered.connect(self.close)
        moreinfo = QtWidgets.QAction('&Help', self, statusTip='More information')
       # moreinfo.triggered.connect(self.information)

        ### menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        fileMenu = menubar.addMenu('&Help')
        fileMenu.addAction(moreinfo)

    def graph_elements(self):
        ### basic geometry and color
        self.setWindowTitle('Villain')
        self.setWindowIcon(QtGui.QIcon('dc1.png'))
        self.setStyleSheet((qdarkstyle.load_stylesheet_pyqt5()))

    def tab(self, credentials):
        self.tabwidget = QtWidgets.QTabWidget()
        self.tabwidget.addTab(Files(credentials), 'Files Import')
        self.tabwidget.addTab(Webservices(), 'Webservice')
        self.setCentralWidget(self.tabwidget)

    ### center main window
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def information(self):
        QtWidgets.QMessageBox.information(self,'Information','Version: 2.0\n'\
                                            'Please, contact karol.chojnowski@digitalcaregroup.com for comments and suggestions\n\n'\
                                          'Digital Care - Data Processing Team')

  #  def setCredentials(self, credentials):
       # self._credentials = credentials
       # return self._credentials[0][0], self._credentials[0][1]









