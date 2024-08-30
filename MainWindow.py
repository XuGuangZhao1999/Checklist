from PySide6.QtWidgets import QMainWindow, QWidget, QSplitter, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from Components.MenuBar import MenuBar
from Components.Previewer import Previewer

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
        self.leftWidget = QLabel("Left Widget", alignment=Qt.AlignCenter)
        self.leftWidget.setStyleSheet("background-color: lightblue")
        
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