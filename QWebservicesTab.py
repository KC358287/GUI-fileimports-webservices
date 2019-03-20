#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from QFilesTab import Files
import pyodbc
import threading


class Webservices(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(Webservices, self).__init__(parent)
        self.files = Files()
        self.layout_init()


    def layout_init(self):
        self.name_f = QtWidgets.QLabel('Enter fully known value:')
        self.name_nf = QtWidgets.QLabel('Enter value like%:')
        self.textbox_f = QtWidgets.QLineEdit()
        self.textbox_nf = QtWidgets.QLineEdit()

        ###table output
        self.tablewidget = QtWidgets.QTableWidget()
        self.tablewidget.setColumnCount(5)
        self.tablewidget.setHorizontalHeaderLabels(['FileNameOriginal', 'OrderItemCode', 'Imported', 'InfoCode', 'Row'])
        self.tablewidget.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.tablewidget.horizontalHeader().setStretchLastSection(True)
        self.tablewidget.resizeColumnsToContents()
        self.tablewidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tablewidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        ### buttons
        self.pb = QtWidgets.QPushButton(self.tr('Run process'))
        self.pb.setDisabled(True)
        #self.textbox_f.textChanged.connect(self.disableButton)
        #self.textbox_nf.textChanged.connect(self.disableButton)
        #self.pb.clicked.connect(self.on_clicked_pb)
        self.clearbutton = QtWidgets.QPushButton(self.tr('Clear all'))
        self.clearbutton.setDisabled(True)
        #self.clearbutton.clicked.connect(self.on_clicked_clear)


        searchpanel_f = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom)
        searchpanel_f.addWidget(self.name_f)
        searchpanel_f.addWidget(self.textbox_f)

        searchpanel_nf = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom)
        searchpanel_nf.addWidget(self.name_nf)
        searchpanel_nf.addWidget(self.textbox_nf)

        wgroupbox = QtWidgets.QGroupBox('Options')
        mainpanel = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        mainpanel.addLayout(searchpanel_f)
        mainpanel.addLayout(searchpanel_nf)
        topbot = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom)
        topbot.addLayout(mainpanel)
        topbot.addWidget(self.pb)
        topbot.addWidget(self.clearbutton)
        wgroupbox.setLayout(topbot)

        grid = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom, self)
        grid.addWidget(wgroupbox)
        grid.addWidget(self.tablewidget)
        self.setLayout(grid)




