#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtWidgets, QtCore
from QFilesTab import Files
from QWebservicesTab import Webservices
import qdarkstyle


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow,self).__init__(parent)

        self.task_bar()
        self.tab_layout()
        self.graph_elements()
        self.center()

    def task_bar(self):
        ### actions on meenubar
        exitAct = QtWidgets.QAction('&Exit', self, shortcut='Ctrl+Q', statusTip='Exit application')
        exitAct.triggered.connect(self.close)
        moreinfo = QtWidgets.QAction('&Help', self, statusTip='More information')
        moreinfo.triggered.connect(self.information)

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

    def tab_layout(self):
        self.tabwidget = QtWidgets.QTabWidget()
        self.tabwidget.addTab(Files(), 'Files Import')
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





