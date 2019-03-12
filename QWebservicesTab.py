#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtWidgets, QtCore
from SqlConnection import DqConnection


class Webservices(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(Webservices, self).__init__(parent)
        self.layout_init()

    def layout_init(self):
        self.name = QtWidgets.QLabel('Enter value:')
        self.textbox = QtWidgets.QLineEdit()


        wgroupbox = QtWidgets.QGroupBox('Option')
        searchpanel = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom)
        searchpanel.addWidget(self.name)
        searchpanel.addWidget(self.textbox)
        wgroupbox.setLayout(searchpanel)


        grid = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom, self)
        grid.addWidget(wgroupbox)
        self.setLayout(grid)



