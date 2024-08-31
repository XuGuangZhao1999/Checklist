from PySide6.QtWidgets import QWidget, QMenu, QTableWidget, QTableWidgetItem, QVBoxLayout
from PySide6.QtCore import Qt, QPoint
class TableViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.infosTableWidget = QTableWidget(0, 6, self)
        self.infosTableWidget.setHorizontalHeaderLabels(["日期", "品名", "单位", "数量", "单价（元）", "金额（元）"])

        layout = QVBoxLayout()
        layout.addWidget(self.infosTableWidget)
        self.setLayout(layout)

        self.infosTableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.infosTableWidget.customContextMenuRequested.connect(self.showContextMenu)

    def addRow(self, row):
        row_index = self.infosTableWidget.rowCount()
        self.infosTableWidget.insertRow(row_index)
        self.infosTableWidget.setItem(row_index, 0, QTableWidgetItem(row["date"]))
        self.infosTableWidget.setItem(row_index, 1, QTableWidgetItem(row["product"]))
        self.infosTableWidget.setItem(row_index, 2, QTableWidgetItem(row["unit"]))
        self.infosTableWidget.setItem(row_index, 3, QTableWidgetItem(str(row["count"])))
        self.infosTableWidget.setItem(row_index, 4, QTableWidgetItem(str(row["price"])))
        self.infosTableWidget.setItem(row_index, 5, QTableWidgetItem(str(row["count"] * row["price"])))

    def showContextMenu(self, pos: QPoint):
        context_menu = QMenu(self)
        context_menu.addAction("Delete").triggered.connect(self.deleteSelectedRow)
        
        context_menu.exec(self.infosTableWidget.mapToGlobal(pos))

    def deleteSelectedRow(self):
        selected_items = self.infosTableWidget.selectedItems()
        if selected_items:
            row_index = selected_items[0].row()
            self.infosTableWidget.removeRow(row_index)