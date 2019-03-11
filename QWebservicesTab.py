#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtWidgets, QtCore
from SqlConnection import DqConnection


class Webservices(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()