from PyQt5 import QtCore
import operator



class TableModelW(QtCore.QAbstractTableModel):
    def __init__(self, res, parent = None):
        super().__init__(parent)

        self.__data = res
        self.__header = ['AppInstance',' DateCreate',
                                                   'StatusCode', 'RequestAction',' ErrorCode',
                                                    'Content']

    def rowCount( self, parent ):
        return len(self.__data)

    def columnCount( self , parent ):
        return len(self.__data[0])

    def flags(self, index):
        if not index.isValid():
            return None
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data ( self , index , role =  QtCore.Qt.DisplayRole):
        i = index.row()
        j = index.column()
        if role == QtCore.Qt.DisplayRole:
            return '{0}'.format(self.__data[i][j])
        else:
            return QtCore.QVariant()

    def headerData(self , section , orientation , role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.__header[section]
            elif orientation == QtCore.Qt.Vertical:
                return section
        return None

    def sort(self, Ncol, order):
        try:
            self.layoutAboutToBeChanged.emit()
            self.__data = sorted(self.__data, key=operator.itemgetter(Ncol))
            if order == QtCore.Qt.DescendingOrder:
                self.__data.reverse()
            self.layoutChanged.emit()
        except:
            pass



class TableModelF(TableModelW):
    def __init__(self, res, parent = None):
        super(TableModelF, self).__init__(res)
        self.__data = res
        self.__header = ['Partner', 'FileType', 'FileName',
                                                    'DateCreate','Imported','InfoCode',
                                                    'Date AKT/DEZ', 'InternalNumber','Wariant',
                                                    'MSISDN','IMEI','PRODUCENT','MODEL','PESEL',
                                                    'NIP','REGON','Segment','Imie','Nazwisko','Nazwa Firmy'
                                                    ]

        self.rowCount(parent)
        self.columnCount(parent)
        self.flags(QtCore.QModelIndex())



    def data (self , index , role =  QtCore.Qt.DisplayRole):
        i = index.row()
        j = index.column()
        if role == QtCore.Qt.DisplayRole:
            return '{0}'.format(self.__data[i][j])
        else:
            return QtCore.QVariant()

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.__header[section]
            elif orientation == QtCore.Qt.Vertical:
                return section
        return None

    def sort(self, Ncol, order):
        try:
            self.layoutAboutToBeChanged.emit()
            self.__data = sorted(self.__data, key=operator.itemgetter(Ncol))
            if order == QtCore.Qt.DescendingOrder:
                self.__data.reverse()
            self.layoutChanged.emit()
        except:
            pass