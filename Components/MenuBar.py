from PySide6.QtWidgets import QMenuBar, QFileDialog
from PySide6.QtCore import Signal, Slot

class MenuBar(QMenuBar):
    export_pdf_signal = Signal(str)
    export_word_signal = Signal(str)
    preview_signal = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        previewAction = self.addAction("Preview")
        previewAction.triggered.connect(self.preview)

        exportMenu = self.addMenu("Export")
        exportMenu.addAction("Word").triggered.connect(self.exportWord)
        exportMenu.addAction("PDF").triggered.connect(self.exportPDF)

    @Slot()
    def exportWord(self):
        export_path, _ = QFileDialog.getSaveFileName(filter="Word 文档(*.docx)")
        if export_path:
            self.export_word_signal.emit(export_path)

    @Slot()
    def exportPDF(self):
        export_path, _ = QFileDialog.getSaveFileName(filter="PDF 文档(*.pdf)")
        if export_path:
            self.export_pdf_signal.emit(export_path)

    @Slot()
    def preview(self):
        self.preview_signal.emit()