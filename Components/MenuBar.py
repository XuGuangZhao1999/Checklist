from PySide6.QtWidgets import QMenuBar

def exportWord():
    print("Exporting to Word")

def exportPDF():
    print("Exporting to PDF")

class MenuBar(QMenuBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        previewMenu = self.addMenu("Preview")

        exportMenu = self.addMenu("Export")
        exportMenu.addAction("Word").triggered.connect(exportWord)
        exportMenu.addAction("PDF").triggered.connect(exportPDF)