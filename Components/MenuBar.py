from PySide6.QtWidgets import QMenuBar, QFileDialog
from PySide6.QtCore import Signal, Slot

class MenuBar(QMenuBar):
    export_pdf_signal = Signal(str)
    export_word_signal = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        previewMenu = self.addMenu("Preview")

        exportMenu = self.addMenu("Export")
        exportMenu.addAction("Word").triggered.connect(self.exportWord)
        exportMenu.addAction("PDF").triggered.connect(self.exportPDF)

    @Slot()
    def exportWord(self):
        export_path = QFileDialog.getSaveFileName(filter="Word 文档(*.docx)")[0]
        self.export_word_signal.emit(export_path)

    @Slot()
    def exportPDF(self):
        export_path = QFileDialog.getSaveFileName(filter="PDF 文档(*.pdf)")[0]
        self.export_pdf_signal.emit(export_path)