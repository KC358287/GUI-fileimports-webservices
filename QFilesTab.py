#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from PyQt5 import QtGui, QtWidgets, QtCore
import pyodbc



class Files(QtWidgets.QWidget):
    def __init__(self,credentials):
        super().__init__()
        self.layout_init()
        self._credentials = credentials
        self.ser = '10.96.5.17\dqinstance'
        self.username, pwd = self._credentials

    def layout_init(self):
        operator = ['Orange','Play', 'PLK', 'TMobile']
        variant = ['Select variant', 'Numer usługi/polisy', 'IMEI', 'PESEL', 'NIP',
                    'REGON', 'Nazwisko', 'Nazwa firmy']
        ###partners
        self.pvbox = QtWidgets.QVBoxLayout()
        self.buttongroup = QtWidgets.QButtonGroup(self)
        for elements, forms in enumerate(operator):
            element = str(forms)
            self.partners = QtWidgets.QRadioButton(element)
            self.buttongroup.addButton(self.partners, )
            self.pvbox.addWidget(self.partners,)
        self.buttongroup.buttonClicked.connect(self.on_itemSelected)
        self.buttongroup.buttonClicked['int'].connect(self.on_itemSelected)


        ###variants
        self.variants = QtWidgets.QComboBox()
        for elements, forms in enumerate(variant):
            element = str(forms)
            self.variants.addItem(element)
        self.variants.model().item(0).setEnabled(False)
        self.variants.activated.connect(self.update_textbox)

        self.textbox = QtWidgets.QLineEdit()

        self.tablewidget = QtWidgets.QTableWidget()
        self.tablewidget.setColumnCount(5)
        self.tablewidget.setHorizontalHeaderLabels(['FileNameOriginal', 'OrderItemCode', 'Imported','InfoCode', 'Row'])
        self.tablewidget.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.tablewidget.horizontalHeader().setStretchLastSection(True)
        self.tablewidget.resizeColumnsToContents()
        self.tablewidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tablewidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.pb = QtWidgets.QPushButton(self.tr('Run process'))
        self.pb.setDisabled(True)
        self.textbox.textChanged.connect(self.disableButton)
        self.pb.clicked.connect(self.on_clicked_pb)
        self.clearbutton = QtWidgets.QPushButton(self.tr('Clear all'))
        self.clearbutton.setDisabled(True)
        self.clearbutton.clicked.connect(self.on_clicked_clear)

        vgroupbox = QtWidgets.QGroupBox('Options')
        pgroupbox = QtWidgets.QGroupBox('Partner')

        mainpanel = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        variantpanel = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom)
        variantpanel.addWidget(self.variants)
        variantpanel.addWidget(self.textbox)
        variantpanel.addWidget(self.clearbutton)
        variantpanel.addWidget(self.pb)
        mainpanel.addWidget(pgroupbox)
        mainpanel.addWidget(vgroupbox)
        vgroupbox.setLayout(variantpanel)
        test = QtWidgets.QVBoxLayout(self)
        test.addLayout(self.pvbox)
        pgroupbox.setLayout(test)

        grid = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom, self)
        grid.addLayout(self.create_layout_label())
        grid.addLayout(mainpanel)
        grid.addWidget(self.tablewidget)
        self.setLayout(grid)

    def create_layout_label(self):
        label1 = QtWidgets.QLabel()
        label2 = QtWidgets.QLabel()
        label3 = QtWidgets.QLabel()
        label4 = QtWidgets.QLabel()
        label1.setText('Orange:')
        label2.setText('Play:')
        label3.setText('PLK:')
        label4.setText('TMobile:')
        self.panel = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        self.panel.addWidget(label1),self.panel.addWidget(label2),\
        self.panel.addWidget(label3),self.panel.addWidget(label4)
        return self.panel

    '''
    def actually_date(self):
        connection = pyodbc.connect(driver='{SQL Server}', server=self.ser,
                                    user=self.username, password=self.pwd)'''




    def update_textbox(self, text):
        self.textbox.clear()
        textline = self.variants.itemText(text)
        self.textbox.setPlaceholderText(textline)
        if textline == 'IMEI':
            regexp = QtCore.QRegExp('^(?=.{0,16}$)(0\d+|[1-9][0-9]+)$')
        elif textline == 'PESEL':
            regexp = QtCore.QRegExp('^(?=.{0,11}$)(0\d+|[1-9][0-9]+)$')
        elif textline == 'NIP':
            regexp = QtCore.QRegExp('^(?=.{0,10}$)(0\d+|[1-9][0-9]+)$')
        elif textline == 'REGON':
            regexp = QtCore.QRegExp('^(?=.{0,9}$)(0\d+|[1-9][0-9]+)$')
        elif textline == 'Nazwisko':
            regexp = QtCore.QRegExp('[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]*')
        else:
            regexp = None
        self.textbox.setValidator(QtGui.QRegExpValidator(regexp))

    @QtCore.pyqtSlot(QtWidgets.QAbstractButton)
    @QtCore.pyqtSlot(int)
    def on_itemSelected(self, index):
        if isinstance(index, QtWidgets.QAbstractButton):
            self.base = None
            element = '{}'.format(index.text())
            if element == 'Play':
                self.base = 'W2_FileImportWorkerP4'
            elif element == 'TMobile':
                self.base= 'W2_FileImportWorkerTmobileFIX'
            elif element == 'Orange':
                self.base = 'W2_FileImportWorkerOCP'
            elif element == 'PLK':
                self.base = 'W2_FileImportWorkerPLK'
            return self.base
        elif isinstance(index, int):
            pass

    @QtCore.pyqtSlot()
    def disableButton(self):
        val = bool(self.textbox.text())
        self.pb.setDisabled(not val)
        self.clearbutton.setDisabled(not val)

    @QtCore.pyqtSlot()
    def disablesql(self):
        self.textbox.setDisabled(True)
        self.pb.setDisabled(True)
        self.clearbutton.setDisabled(True)

    @QtCore.pyqtSlot()
    def enablesql(self):
        self.textbox.setDisabled(False)
        self.pb.setDisabled(False)
        self.clearbutton.setDisabled(False)


    ### run process button
    @QtCore.pyqtSlot()
    def on_clicked_pb(self):
        if self.textbox.text():
            threading.Thread(target=self.sql_query, daemon=True).start()

    ### clear all
    @QtCore.pyqtSlot()
    def on_clicked_clear(self):
        if self.textbox.text():
            self.textbox.clear()
        self.tablewidget.setRowCount(0)
        self.tablewidget.setColumnWidth(3, 200)

    def table_performance(self):
        self.tablewidget.resizeColumnsToContents()
        self.tablewidget.setColumnWidth(4, 2500)
        self.tablewidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

    @QtCore.pyqtSlot(str, str)
    def show_warning(self, title, msg):
        QtWidgets.QMessageBox.information(self, title, msg)

    @QtCore.pyqtSlot(str, str)
    def show_ok(self, title, msg):
        QtWidgets.QMessageBox.information(self, title ,msg)

    @QtCore.pyqtSlot()
    def clear_items(self):
        self.tablewidget.setRowCount(0)

    @QtCore.pyqtSlot(int, int, str)
    def add_item(self, row, column, val):
        if row >= self.tablewidget.rowCount():
            self.tablewidget.insertRow(self.tablewidget.rowCount())
        newitem = QtWidgets.QTableWidgetItem(val)
        self.tablewidget.setItem(row, column, newitem)

    @QtCore.pyqtSlot()
    def sort_items(self):
        self.tablewidget.sortItems(0, order=QtCore.Qt.DescendingOrder)

    def sql_query(self):
        imei = '%' + self.textbox.text() + '%'
        self.clear_items()
        try:
            self.disablesql()
            connection = pyodbc.connect(driver='{SQL Server}', server=self.ser,
                                        user=self.username, password=self.pwd)
            if self.base == 'W2_FileImportWorkerTmobileFIX':
                cursor = connection.cursor()
                res = cursor.execute(''' 
                                                    SELECT FI.FileNameOriginal,
                                                    FI.OrderItemCode,
                                                    FIR.Imported,
                                                    FIRI.InfoCode,
                                                    FR.Row
                                                    FROM BIDQ_W2_DB.dbo.[FileImports] AS FI
                                        JOIN BIDQ_W2_DB.dbo.[FileImportRows] AS FIR ON FI.Id = FIR.FileImportId
                                        JOIN BIDQ_W2_DB.dbo.[FileRows] AS FR ON FIR.RowId = FR.RowId 
                                        LEFT JOIN BIDQ_W2_DB.dbo.FileImportRowInfoes AS FIRI ON FR.RowId = FIRI.RowId
                                                    WHERE (FI.WorkerCode = ? or FI.WorkerCode = ?) and FR.Row LIKE ? ''',
                                     (self.base, self.base, imei))

            elif self.base == 'All':
                cursor = connection.cursor()
                res = cursor.execute(''' SELECT FI.FileNameOriginal,
                                        FI.OrderItemCode,
                                        FIR.Imported,
                                        FIRI.InfoCode,
                                        FR.Row
                                        FROM BIDQ_W2_DB.dbo.[FileImports] AS FI
                                        JOIN BIDQ_W2_DB.dbo.[FileImportRows] AS FIR ON FI.Id = FIR.FileImportId
                                        JOIN BIDQ_W2_DB.dbo.[FileRows] AS FR ON FIR.RowId = FR.RowId 
                                        LEFT JOIN BIDQ_W2_DB.dbo.FileImportRowInfoes AS FIRI ON FR.RowId = FIRI.RowId
                                        WHERE FR.Row LIKE ? ''',(imei))
            else:
                cursor = connection.cursor()
                res = cursor.execute('''
                                        SELECT FI.FileNameOriginal,
                                        FI.OrderItemCode,
                                        FIR.Imported,
                                        FIRI.InfoCode,
                                        FR.Row
                                        FROM BIDQ_W2_DB.dbo.[FileImports] AS FI
                                        JOIN BIDQ_W2_DB.dbo.[FileImportRows] AS FIR ON FI.Id = FIR.FileImportId
                                        JOIN BIDQ_W2_DB.dbo.[FileRows] AS FR ON FIR.RowId = FR.RowId 
                                        LEFT JOIN BIDQ_W2_DB.dbo.FileImportRowInfoes AS FIRI ON FR.RowId = FIRI.RowId
                                        WHERE FI.WorkerCode =  ? and FR.Row LIKE ? ''', (self.base, imei))

            if not cursor.rowcount:
                QtCore.QMetaObject.invokeMethod(self, 'show_warning',
                                                QtCore.Qt.QueuedConnection,
                                                QtCore.Q_ARG(str, 'IMEI'), QtCore.Q_ARG(str, 'No items found'))
            else:
                QtCore.QMetaObject.invokeMethod(self, 'clear_items', QtCore.Qt.QueuedConnection)
                QtCore.QThread.msleep(10)
                for row, form in enumerate(res):
                    for column, item in enumerate(form):
                        QtCore.QMetaObject.invokeMethod(self, 'add_item',
                                                        QtCore.Qt.QueuedConnection,
                                                        QtCore.Q_ARG(int, row), QtCore.Q_ARG(int, column),
                                                        QtCore.Q_ARG(str, str(item)))
                        QtCore.QThread.msleep(10)
                QtCore.QMetaObject.invokeMethod(self, 'sort_items', QtCore.Qt.QueuedConnection)
                self.table_performance()
                QtCore.QMetaObject.invokeMethod(self, 'show_ok',
                                                QtCore.Qt.QueuedConnection,
                                                QtCore.Q_ARG(str, 'Done'), QtCore.Q_ARG(str, 'Items found'))
            cursor.close()

        except:
                QtCore.QMetaObject.invokeMethod(self, 'show_warning',
                                                QtCore.Qt.QueuedConnection,
                                                QtCore.Q_ARG(str, 'Error'), QtCore.Q_ARG(str, 'Something went wrong\n\n' \
                                                                                              'Contact karol.chojnowski@digitalcaregroup.com'))
        self.enablesql()

