from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt


class ComPortListModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__com_ports = []

    @property
    def com_ports(self):
        return self.__com_ports

    def rowCount(self, parent=QModelIndex()):
        return len(self.__com_ports)

    def flags(self, index):
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def data(self, index, role):
        """return value or edit value"""
        com_port = self.__com_ports[index.row()]
        if role == Qt.ItemDataRole.ToolTipRole:
            return com_port

        if role == Qt.ItemDataRole.DisplayRole:
            return com_port

        return None

    def update_data(self, list_of_com_ports):
        self.beginInsertRows(
            QModelIndex(), len(self.__com_ports), len(self.__com_ports)
        )
        for item in list_of_com_ports:
            if item not in self.__com_ports:
                self.__com_ports.append(item)
        self.endInsertRows()

        for index, value in enumerate(self.__com_ports):
            if value not in list_of_com_ports:
                self.beginRemoveRows(QModelIndex(), index, index)
                self.__com_ports.pop(index)
                self.endRemoveRows()
