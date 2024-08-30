from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from Components.MenuBar import MenuBar

class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.resize(800, 600)

        # Add the menu bar
        menuBar = MenuBar()
        self.setMenuBar(menuBar)

        # Add the central widget
        centralWidget = QWidget()
        
        hLayout = QHBoxLayout()
        leftWidget = QLabel("Left Widget", alignment=Qt.AlignCenter)
        rightWidget = QLabel("Right Widget", alignment=Qt.AlignCenter)
        leftWidget.setStyleSheet("background-color: lightblue")
        rightWidget.setStyleSheet("background-color: lightgreen")
        hLayout.addWidget(leftWidget, 3)
        hLayout.addWidget(rightWidget, 2)
        centralWidget.setLayout(hLayout)
        
        self.setCentralWidget(centralWidget)