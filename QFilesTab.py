#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from PyQt5 import QtGui, QtWidgets, QtCore
import pyodbc



class Files(QtWidgets.QWidget):
    operator = ['Orange', 'Play', 'PLK', 'TMobile']
    variant = ['Select variant', 'InternalNnmber','MSISDN',\
               'IMEI', 'PESEL', 'NIP',\
               'REGON', 'NAZWISKO', 'NAZWA_FIRMY']

    def __init__(self,credentials):
        super().__init__()
        self._credentials = credentials
        self.ser = '10.96.5.17\dqinstance'
        self.username, self.pwd = self._credentials

        self.layout_init()
        self.run_refresh()

    def layout_init(self):
        self.pvbox = QtWidgets.QVBoxLayout()
        self.buttongroup = QtWidgets.QButtonGroup(self)
        for elements, forms in enumerate(self.operator):
            element = str(forms)
            self.partners = QtWidgets.QRadioButton(element)
            self.buttongroup.addButton(self.partners, elements)
            self.pvbox.addWidget(self.partners,)
            if elements == 0:
                self.partners.setChecked(True)
                self.element = self.partners.text()
        self.buttongroup.buttonClicked.connect(self.on_itemSelected)
        self.buttongroup.buttonClicked['int'].connect(self.on_itemSelected)


        self.variants = QtWidgets.QComboBox()
        for elements, forms in enumerate(self.variant):
            element = str(forms)
            self.variants.addItem(element)
        self.variants.model().item(0).setEnabled(False)
        self.variants.activated.connect(self.update_textbox)

        self.textbox = QtWidgets.QLineEdit()

        self.tablewidget = QtWidgets.QTableWidget()
        self.tablewidget.setColumnCount(20)
        self.tablewidget.setHorizontalHeaderLabels(['Partner', 'FileType', 'FileName',\
                                                    'DateCreate','Imported','InfoCode',\
                                                    'Date AKT/DEZ', 'InternalNumber','Wariant',\
                                                    'MSISDN','IMEI','PRODUCENT','MODEL','PESEL',\
                                                    'NIP','REGON','Segment','Imie','Nazwisko','Nazwa Firmy'
                                                    ])
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
        self.variantpanel = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom)
        self.variantpanel.addWidget(self.variants)
        self.variantpanel.addWidget(self.textbox)
        self.variantpanel.addWidget(self.clearbutton)
        self.variantpanel.addWidget(self.pb)
        mainpanel.addWidget(pgroupbox)
        mainpanel.addWidget(vgroupbox)
        vgroupbox.setLayout(self.variantpanel)
        test = QtWidgets.QVBoxLayout(self)
        test.addLayout(self.pvbox)
        pgroupbox.setLayout(test)

        grid = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom, self)
        grid.addLayout(self.create_layout_label())
        grid.addLayout(mainpanel)
        grid.addWidget(self.tablewidget)
        self.setLayout(grid)

    def create_layout_label(self):
        self.label0 = QtWidgets.QLabel()
        self.label1 = QtWidgets.QLabel()
        self.label2 = QtWidgets.QLabel()
        self.label3 = QtWidgets.QLabel()
        self.label0.setText('Orange:')
        self.label1.setText('Play:')
        self.label2.setText('PLK:')
        self.label3.setText('TMobile:')
        self.panel = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        self.panel.addWidget(self.label0),self.panel.addWidget(self.label1),\
        self.panel.addWidget(self.label2),self.panel.addWidget(self.label3)
        return self.panel

    def update_textbox(self, text):
        self.textbox.clear()
        self.textline = self.variants.itemText(text)
        self.textbox.setPlaceholderText(self.textline)
        if self.textline == 'IMEI':
            regexp = QtCore.QRegExp('^(?=.{0,16}$)(0\d+|[1-9][0-9]+)$')
        elif self.textline == 'PESEL' or self.textline == 'MSISDN':
            regexp = QtCore.QRegExp('^(?=.{0,11}$)(0\d+|[1-9][0-9]+)$')
        elif self.textline == 'NIP':
            regexp = QtCore.QRegExp('^(?=.{0,10}$)(0\d+|[1-9][0-9]+)$')
        elif self.textline == 'REGON':
            regexp = QtCore.QRegExp('^(?=.{0,9}$)(0\d+|[1-9][0-9]+)$')
        elif self.textline == 'NAZWISKO':
            regexp = QtCore.QRegExp('[A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]*')
        else:
            regexp = None
        self.textbox.setValidator(QtGui.QRegExpValidator(regexp))
        return self.textline

    @QtCore.pyqtSlot(QtWidgets.QAbstractButton)
    @QtCore.pyqtSlot(int)
    def on_itemSelected(self, index):
        if isinstance(index, QtWidgets.QAbstractButton):
            self.element = '{}'.format(index.text())
            return self.element
        elif isinstance(index, int):
            pass

    @QtCore.pyqtSlot()
    def disableButton(self):
        if self.variants.currentIndex() == 0:
            val = False
        else:
            val = bool(self.textbox.text())
        self.pb.setDisabled(not val)
        self.clearbutton.setDisabled(not val)

    @QtCore.pyqtSlot()
    def disable_widgets(self):
        self.textbox.setDisabled(True)
        self.pb.setDisabled(True)
        self.clearbutton.setDisabled(True)

    @QtCore.pyqtSlot()
    def enable_widgets(self):
        self.textbox.setDisabled(False)
        self.pb.setDisabled(False)
        self.clearbutton.setDisabled(False)


    def run_refresh(self):
        threading.Thread(target=self.load_data, daemon=True).start()

    @QtCore.pyqtSlot()
    def on_clicked_pb(self):
        if self.textbox.text():
            threading.Thread(target=self.sql_query, daemon=True).start()

    @QtCore.pyqtSlot()
    def on_clicked_clear(self):
        if self.textbox.text():
            self.textbox.clear()
        self.tablewidget.setRowCount(0)
        self.tablewidget.setColumnWidth(3, 200)

    @QtCore.pyqtSlot()
    def table_performance(self):
        self.tablewidget.resizeColumnsToContents()
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
    def make_progressbar(self):
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setRange(0, 0)
        self.variantpanel.removeWidget(self.pb)
        self.pb.setParent(None)
        self.variantpanel.addWidget(self.progressBar)

    @QtCore.pyqtSlot()
    def replace_widgets(self):
        self.variantpanel.removeWidget(self.progressBar)
        self.progressBar.setParent(None)
        self.variantpanel.addWidget(self.pb)


    def sql_query(self):
        self.clear_items()
        text = self.textbox.text()
        column = self.textline
        noel = 0
        sql = '''
        SELECT 
               [Partner]
              ,[FileType]
              ,[FileNameTransformed]
              ,[FileDateCreate]
              ,[Imported]
              ,ISNULL([InfoCode],'-') as InfoCode
              ,[DateActivation/Deactivation]
              ,[Internalnumber]
              ,[WARIANT]
              ,[MSISDN]
              ,[IMEI]
              ,[PRODUCENT]
              ,[MODEL]
              ,[PESEL]
              ,[NIP]
              ,[REGON]
              ,[SEGMENT]
              ,[IMIE]
              ,[NAZWISKO]
              ,[NAZWA_FIRMY]
          FROM [CleaningFilesRows].[dbo].[SplittedFileRows]  
          WHERE Partner = ?  and [{}] = ?
          ORDER BY FileDateCreate
        '''.format(column)


        try:
            self.disable_widgets()
            QtCore.QMetaObject.invokeMethod(self, 'make_progressbar', QtCore.Qt.QueuedConnection)
            connection = pyodbc.connect(driver='{SQL Server}', server=self.ser,
                                        user=self.username, password=self.pwd)
            cursor = connection.cursor()
            res = cursor.execute(sql, self.element, text)
            QtCore.QMetaObject.invokeMethod(self, 'replace_widgets', QtCore.Qt.QueuedConnection)

            if not cursor.rowcount:
                QtCore.QMetaObject.invokeMethod(self, 'show_warning',
                                                QtCore.Qt.QueuedConnection,
                                                QtCore.Q_ARG(str, 'Files Import'), QtCore.Q_ARG(str, 'No items found'))
            else:
                QtCore.QMetaObject.invokeMethod(self, 'clear_items',
                                                QtCore.Qt.QueuedConnection)
                QtCore.QThread.msleep(10)
                for row, form in enumerate(res):
                    for column, item in enumerate(form):
                        QtCore.QMetaObject.invokeMethod(self, 'add_item',
                                                        QtCore.Qt.QueuedConnection,
                                                        QtCore.Q_ARG(int, row), QtCore.Q_ARG(int, column),
                                                        QtCore.Q_ARG(str, str(item)))
                        QtCore.QThread.msleep(10)
                    noel += 1
                QtCore.QMetaObject.invokeMethod(self, 'table_performance',
                                                QtCore.Qt.QueuedConnection)
                if noel == 1:
                    itemsfound = ' item found'
                else:
                    itemsfound = ' items found'
                noel = str(noel) + itemsfound
                QtCore.QMetaObject.invokeMethod(self, 'show_ok',
                                                QtCore.Qt.QueuedConnection,
                                                QtCore.Q_ARG(str, 'Files Import'), QtCore.Q_ARG(str, noel))
            cursor.close()

        except:
                QtCore.QMetaObject.invokeMethod(self, 'show_warning',
                                                QtCore.Qt.QueuedConnection,
                                                QtCore.Q_ARG(str, 'Files Import'), QtCore.Q_ARG(str, 'Something went wrong\n\n' \
                                                                                              'Contact Data Processing Team'))
        self.enable_widgets()


    def load_data(self):
        Sql = '''     Select CAST(MAX([DateActivation/Deactivation]) as date)
                    FROM [CleaningFilesRows].[dbo].[SplittedFileRows]
                 WHERE Partner = ? and (FileType = 'AKT' or FileType = 'AC')  
                 and [DateActivation/Deactivation] < CONVERT(nvarchar,CONVERT(date,GETDATE()+30,120))
                '''
        SqlP = '''
                Select  MAX(CONVERT(date,[DateActivation/Deactivation],103))
                 FROM [CleaningFilesRows].[dbo].[SplittedFileRows]
                WHERE Partner = 'PLK' and (FileType = 'AKT' or FileType = 'AC') 
                and [DateActivation/Deactivation] < CONVERT(nvarchar,CONVERT(date,GETDATE()+30,120)) 
                '''
        connection = pyodbc.connect(driver='{SQL Server}', server=self.ser,
                                    user=self.username, password=self.pwd)
        cursor = connection.cursor()
        try:
            QtCore.QThread.msleep(10)
            i = 0
            for value in (self.operator):
                label = getattr(self, 'label{}'.format(i))
                if i == 2: #PLK
                    res = cursor.execute(SqlP)
                    for fieldrow in res.fetchall():
                        label.setText(value+': '+fieldrow[0])
                else:
                    res = cursor.execute(Sql, value)
                    for fieldrow in res.fetchall():
                        label.setText(value + ': ' + fieldrow[0])
                i +=1
        except:
            QtCore.QThread.msleep(10)
            for j in range(0, 4):
                label = getattr(self, 'label{}'.format(j))
                label.setText(self.operator[j] + ': ' + 'No data')





