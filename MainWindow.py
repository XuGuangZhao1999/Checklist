from PySide6.QtWidgets import QMainWindow, QWidget, QSplitter, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Slot
from Components.MenuBar import MenuBar
from Components.Previewer import Previewer
from Components.InfosReciver import InfosReciver
from Components.TableViewer import TableViewer

class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.resize(800, 600)

        # Add the menu bar
        self.menuBar = MenuBar(self)
        self.setMenuBar(self.menuBar)

        # Add the central widget
        self.centralWidget = QWidget(self)
            
        # Left Widget
        self.leftWidget = QWidget(self.centralWidget)
        self.infosTableViewer = TableViewer(self.leftWidget)
        self.infosReciver = InfosReciver(self.leftWidget)
        VLayout = QVBoxLayout()
        VLayout.addWidget(self.infosTableViewer)
        VLayout.addWidget(self.infosReciver)
        self.leftWidget.setLayout(VLayout)
        
        # PDF Viewer
        self.previewer = Previewer(self)

        splitter = QSplitter(Qt.Horizontal, self)
        splitter.insertWidget(0, self.leftWidget)
        splitter.insertWidget(1, self.previewer)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)

        hLayout = QHBoxLayout()
        hLayout.addWidget(splitter)

        self.centralWidget.setLayout(hLayout)
        self.setCentralWidget(self.centralWidget)

        # Connect Signal&Slot
        self.menuBar.preview_signal.connect(self.sendInfosToPreviewer)
        self.menuBar.export_pdf_signal.connect(self.previewer.export_to_pdf)
        self.menuBar.export_word_signal.connect(self.previewer.export_to_word)
        self.menuBar.clear_signal.connect(self.infosTableViewer.clear)
        self.infosReciver.addInfoBtn.clicked.connect(self.addInfos)

    @Slot()
    def addInfos(self):
        row = dict()
        row["date"] = self.infosReciver.dateEdit.text()
        row["product"] = self.infosReciver.infosProductEdit.text()
        row["unit"] = self.infosReciver.infosUnitEdit.text()
        row["count"] = self.infosReciver.infosCountEdit.value()
        row["price"] = self.infosReciver.infosPriceEdit.value()
        self.infosTableViewer.addRow(row)

    @Slot()
    def sendInfosToPreviewer(self):
        doc = dict()
        doc["Description"] = self.infosReciver.getDocDescription()
        doc["TableModel"] = self.infosTableViewer.getDocTableModel()
        self.previewer.preview(doc)
