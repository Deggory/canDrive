from PyQt6.QtCore import Qt, QModelIndex

from core.can_message.decoded_can_message import DecodedCanMessage
from core.message_table_model.base_message_table_model import BaseMessageTableModel
from core.project_data import ProjectData


class DecodedMessagesTableModel(BaseMessageTableModel):
    def __init__(self, project_data: ProjectData, parent=None):
        headers = [
            "Name",
            "ID (hex)",
            "RTR (hex)",
            "IDE (hex)",
            "DLC (hex)",
            "D0",
            "D1",
            "D2",
            "D3",
            "D4",
            "D5",
            "D6",
            "D7",
        ]
        self.project_data = project_data
        super().__init__(data=project_data.decoded_messages, headers=headers, parent=parent)

    def data(self, index: QModelIndex, role: int = ...):
        if role in [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]:
            message: DecodedCanMessage = self._data[index.row()]
            value = message.get_value_from_index(index.column())
            if index.column() == 1:
                if value in self.project_data.label_dict:
                    return f"{value} ({self.project_data.label_dict[value]})"
            return value

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter

        if role == Qt.ItemDataRole.UserRole:
            message: DecodedCanMessage = self._data[index.row()]
            return message

        return None

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable  # type: ignore
        else:
            return Qt.ItemFlag.ItemIsEnabled

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self._data[index.row()].name = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def add_data(self, data: DecodedCanMessage):
        for message in self._data:
            if message.can_message == data.can_message:
                return

        self.beginInsertRows(QModelIndex(), 0, 0)
        self._data.insert(0, data)
        self.endInsertRows()
