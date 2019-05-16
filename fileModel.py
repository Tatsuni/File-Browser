from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class FileModel(QAbstractTableModel):
    def __init__(self, data=None, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._data = data
        self.headers = ["", 'Name', 'Type', 'Size']

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        return 4
    
    def data(self, QModelIndex, role=None):
        fileItem = self._data[QModelIndex.row()]
        column = QModelIndex.column()

        if role == Qt.DecorationRole and column == 0:
            return QPixmap(fileItem.IconPath)
        elif role == Qt.DisplayRole:
            if column == 1:
                return fileItem.Name
            elif column == 2:
                return fileItem.Type
            elif column == 3:
                return fileItem.Size

        return QVariant()

    def headerData(self, index, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[index]
