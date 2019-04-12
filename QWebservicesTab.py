#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
import pyodbc
import threading


'''
#performance qtablewidget
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent = None):
        super(TableModel, self).__init__(parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0]) if self.rowCount() else 0

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            if 0 <= row < self.rowCount():
                column = index.column()
                if 0 <= column < self.columnCount():
                    return self._data[row][column]

'''




class Webservices(QtWidgets.QWidget):
    def __init__(self, credentials, parent = None):
        super(Webservices, self).__init__(parent)
        self.layout_init()
        self._credentials = credentials


    def layout_init(self):
        self.name_f = QtWidgets.QLabel('Enter value:')
        self.textbox = QtWidgets.QLineEdit()

        self.tablewidget = QtWidgets.QTableWidget()
        self.tablewidget.setColumnCount(7)
        self.tablewidget.setHorizontalHeaderLabels(['RequestKey','AppInstance','Content', \
                                                    'StatusCode', 'RequestAction', 'DateCreate', \
                                                    'ErrorCode'])
        self.tablewidget.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.tablewidget.horizontalHeader().setStretchLastSection(True)
        self.tablewidget.resizeColumnsToContents()
        self.tablewidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tablewidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.pb = QtWidgets.QPushButton(self.tr('Run process'))
        self.pb.setDisabled(True)
        self.textbox.textChanged.connect(self.disable_button)
        self.pb.clicked.connect(self.on_clicked_pb)
        self.clearbutton = QtWidgets.QPushButton(self.tr('Clear all'))
        self.clearbutton.setDisabled(True)
        self.clearbutton.clicked.connect(self.on_clicked_clear)

        self.toggle = True
        self.b1 = QtWidgets.QCheckBox('Yes, I know the value', self)
        self.b1.setChecked(self.toggle)
        self.b2 = QtWidgets.QCheckBox('I am not sure about this value...',self)
        self.b2.setChecked(not self.toggle)
        self.b1.clicked.connect(self.toggle_checkbox)
        self.b2.clicked.connect(self.toggle_checkbox)

        searchpanel_f = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom)
        searchpanel_f.addWidget(self.name_f)
        searchpanel_f.addWidget(self.textbox)
        checkbox = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        checkbox.addWidget(self.b1)
        checkbox.addWidget(self.b2)

        wgroupbox = QtWidgets.QGroupBox('Options')
        mainpanel = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        mainpanel.addLayout(searchpanel_f)
        self.topbot = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom)
        self.topbot.addLayout(mainpanel)
        self.topbot.addLayout(checkbox)
        self.topbot.addWidget(self.clearbutton)
        self.topbot.addWidget(self.pb)
        wgroupbox.setLayout(self.topbot)

        grid = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom, self)
        grid.addWidget(wgroupbox)
        grid.addWidget(self.tablewidget)
        self.setLayout(grid)


    @QtCore.pyqtSlot()
    def toggle_checkbox(self):
        self.toggle = not self.toggle
        self.b1.setChecked(self.toggle), self.b2.setChecked(not self.toggle)

    @QtCore.pyqtSlot()
    def disable_button(self):
        val = bool(self.textbox.text())
        self.pb.setDisabled(not val), self.clearbutton.setDisabled(not val)

    @QtCore.pyqtSlot()
    def disable_widgets(self):
        self.textbox.setDisabled(True)
        self.pb.setDisabled(True) ,self.clearbutton.setDisabled(True)
        self.b1.setDisabled(True), self.b2.setDisabled(True)

    @QtCore.pyqtSlot()
    def enable_widgets(self):
        self.textbox.setDisabled(False)
        self.pb.setDisabled(False), self.clearbutton.setDisabled(False)
        self.b1.setDisabled(False), self.b2.setDisabled(False)

    @QtCore.pyqtSlot()
    def on_clicked_clear(self):
        if self.textbox.text():
            self.textbox.clear()
        self.tablewidget.setRowCount(0)
        self.tablewidget.setColumnWidth(3, 200)

    @QtCore.pyqtSlot()
    def on_clicked_pb(self):
        if self.textbox.text():
            threading.Thread(target=self.sql_query, daemon=True).start()

    @QtCore.pyqtSlot()
    def table_performance(self):
        #self.tablewidget.resizeColumnsToContents()
        #self.tablewidget.setColumnWidth(4, 2500)
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
        self.topbot.removeWidget(self.pb)
        self.pb.setParent(None)
        self.topbot.addWidget(self.progressBar)

    @QtCore.pyqtSlot()
    def replace_widgets(self):
        self.topbot.removeWidget(self.progressBar)
        self.progressBar.setParent(None)
        self.topbot.addWidget(self.pb)


    def sql_query(self):
        ser = '10.96.5.17\dqinstance'
        noel = 0
        username, pwd = self._credentials
        value = self.textbox.text()
        self.clear_items()
        try:
            self.disable_widgets()
            connection = pyodbc.connect(driver='{SQL Server}', server=ser,
                                        user=username, password=pwd)
            if self.b1.isChecked() == True:
                cursor = connection.cursor()
                QtCore.QMetaObject.invokeMethod(self, 'make_progressbar', QtCore.Qt.QueuedConnection)
                res = cursor.execute(''' 
                                    SELECT distinct
                                        a.RequestKey,
                                        a.AppInstance,
                                        a.DQContent as Content,
                                        a.StatusCode,
                                        a.RequestAction,
                                        a.DateCreate,
                                        ISNULL(c.InfoCode, '-') as ErrorCode
                                    FROM CleaningRequests.dbo.InsuranceRequests a
                    INNER JOIN CleaningRequests.dbo.InsuranceRequestTokens b ON a.id = b.id
                    LEFT JOIN BIDQ_W2_DB.dbo.InsuranceRequestInfoes c ON a.RequestKey = c.RequestKey
                    WHERE b.TokenValue = ? and a.Appinstance <> 'CoreSaleService'
                    order by a.datecreate
                    ''', (value))
            else:
                cursor = connection.cursor()
                QtCore.QMetaObject.invokeMethod(self, 'make_progressbar',QtCore.Qt.QueuedConnection)
                res = cursor.execute(''' 
                                        SELECT distinct
                                            a.RequestKey,
                                            a.AppInstance,
                                            a.DQContent as Content,
                                            a.StatusCode,
                                            a.RequestAction,
                                                        a.DateCreate,
                                                        ISNULL(c.InfoCode, '-') as ErrorCode
                                                    FROM CleaningRequests.dbo.InsuranceRequests a
                                    INNER JOIN CleaningRequests.dbo.InsuranceRequestTokens b ON a.id = b.id
                                    LEFT JOIN BIDQ_W2_DB.dbo.InsuranceRequestInfoes c ON a.RequestKey = c.RequestKey
                                    WHERE b.TokenValue like ? and a.Appinstance <> 'CoreSaleService'
                                    order by a.datecreate
                                    ''', (value))
            QtCore.QMetaObject.invokeMethod(self, 'replace_widgets', QtCore.Qt.QueuedConnection)
            if not cursor.rowcount:
                QtCore.QMetaObject.invokeMethod(self, 'show_warning',
                                                QtCore.Qt.QueuedConnection,
                                                QtCore.Q_ARG(str, 'IMEI'), QtCore.Q_ARG(str, 'No items found'))
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
                                                QtCore.Q_ARG(str, 'Done'), QtCore.Q_ARG(str, noel))
            cursor.close()
        except:
                QtCore.QMetaObject.invokeMethod(self, 'show_warning',
                                                QtCore.Qt.QueuedConnection,
                                                QtCore.Q_ARG(str, 'Error'), QtCore.Q_ARG(str, 'Something went wrong\n\n' \
                                                                                              'Contact karol.chojnowski@digitalcaregroup.com'))
        self.enable_widgets()










