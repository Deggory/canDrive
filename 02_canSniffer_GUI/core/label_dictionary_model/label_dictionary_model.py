from typing import Any

from PyQt6.QtCore import QModelIndex, QAbstractTableModel, Qt

from core.project_data import ProjectData


class LabelDictionaryModel(QAbstractTableModel):

    def __init__(self, project_data: ProjectData, parent=None):
        super().__init__(parent=parent)
        self.__data = project_data.label_dict
        self.__horizontal_headers = [
            "ID (hex)",
            "Label"
        ]

    def rowCount(self, parent=None):
        return len(self.__data)

    def columnCount(self, parent=None):
        return len(self.__horizontal_headers)

    def data(self, index: QModelIndex, role: int = ...):
        if role in [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]:
            key = [d for d in self.__data.keys()][index.row()]
            if index.column() == 0:
                return key
            elif index.column() == 1:
                return self.__data[key]
            else:
                print("index is not 0 or 1")

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter

    def headerData(self, section: int, orientation: Any, role: int = ...) -> Any:
        if orientation == Qt.Orientation.Horizontal and section < len(self.__horizontal_headers):
            if role == Qt.ItemDataRole.DisplayRole:
                return self.__horizontal_headers[section]

    def add_data(self, key, value):
        self.beginInsertRows(QModelIndex(), 0, 0)
        if key not in self.__data:
            self.__data[key] = value

        sorted_dict = dict(sorted(self.__data.items()))
        self.__data = sorted_dict

        self.endInsertRows()

    def flags(self, index):
        if index.column() == 1:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable
        else:
            return Qt.ItemFlag.ItemIsEnabled

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            key = [d for d in self.__data.keys()][index.row()]
            self.__data[key] = value
            self.dataChanged.emit(index, index)
            return True
