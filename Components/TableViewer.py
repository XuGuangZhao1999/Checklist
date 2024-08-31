from PySide6.QtWidgets import QWidget, QMenu, QTableWidget, QTableWidgetItem, QVBoxLayout
from PySide6.QtCore import Qt, QPoint
import cn2an

headerLabels = ["日期", "品名", "单位", "数量", "单价（元）", "金额（元）"]
class TableViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.productUnit = ""
        self.productCount = 0
        self.productPrice = 0
        self.totalPrice = 0
        self.infosTableWidget = QTableWidget(0, 6, self)
        self.infosTableWidget.setHorizontalHeaderLabels(headerLabels)

        layout = QVBoxLayout()
        layout.addWidget(self.infosTableWidget)
        self.setLayout(layout)

        self.infosTableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.infosTableWidget.customContextMenuRequested.connect(self.showContextMenu)

    def addRow(self, row):
        row_index = self.infosTableWidget.rowCount()
        if row_index != 0:
            row_index -= 1
        self.infosTableWidget.insertRow(row_index)

        items = [
            QTableWidgetItem(row["date"]),
            QTableWidgetItem(row["product"]),
            QTableWidgetItem(row["unit"]),
            QTableWidgetItem(str(row["count"])),
            QTableWidgetItem(str(row["price"])),
            QTableWidgetItem(str(row["count"] * row["price"]))
        ]

        for col, item in enumerate(items):
            item.setTextAlignment(Qt.AlignCenter)
            self.infosTableWidget.setItem(row_index, col, item)

        self.totalPrice += row["count"] * row["price"]
        if row_index == 0:
            self.infosTableWidget.insertRow(row_index + 1)
            self.productUnit = row["unit"]
            self.productCount = row["count"]
            self.productPrice = row["price"]
        
        self.updateLastRow()


    def showContextMenu(self, pos: QPoint):
        context_menu = QMenu(self)
        context_menu.addAction("Delete").triggered.connect(self.deleteSelectedRow)
        
        context_menu.exec(self.infosTableWidget.mapToGlobal(pos))

    def deleteSelectedRow(self):
        selected_items = self.infosTableWidget.selectedItems()
        if selected_items:
            row_index = selected_items[0].row()
            self.totalPrice -= float(self.infosTableWidget.item(row_index, 5).text())
            self.infosTableWidget.removeRow(row_index)
            self.updateLastRow()

    def updateLastRow(self):
        lastRowIndex = self.infosTableWidget.rowCount() - 1
        if lastRowIndex != 0:
            items = [
                QTableWidgetItem("总计: " + cn2an.an2cn(str(self.totalPrice), "rmb")),
                QTableWidgetItem(self.productUnit),
                QTableWidgetItem(str(self.productCount)),
                QTableWidgetItem(str(self.productPrice)),
                QTableWidgetItem(str(self.totalPrice))
            ]

            for item in items:
                item.setTextAlignment(Qt.AlignCenter)

            self.infosTableWidget.setSpan(lastRowIndex, 0, 1, 2)
            self.infosTableWidget.setItem(lastRowIndex, 0, items[0])
            self.infosTableWidget.setItem(lastRowIndex, 2, items[1])
            self.infosTableWidget.setItem(lastRowIndex, 3, items[2])
            self.infosTableWidget.setItem(lastRowIndex, 4, items[3])
            self.infosTableWidget.setItem(lastRowIndex, 5, items[4])
        else:
            self.infosTableWidget.removeRow(lastRowIndex)

    def getDocTableModel(self):
        model = self.infosTableWidget.model()
        docTableModel = []
        docTableModel.append(headerLabels)

        for row in range(model.rowCount()):
            rowData = []
            for column in range(model.columnCount()):
                index = model.index(row, column)
                value = model.data(index)
                rowData.append(value)
            docTableModel.append(rowData)

        return docTableModel