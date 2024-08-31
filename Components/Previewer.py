from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QStandardPaths, QUrl, QPoint, Slot
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtGui import QIcon
from pdf2docx import Converter
import resources_rc
import sys
import math
import pymupdf


ZOOM_MULTIPLIER = math.sqrt(2.0)

class Previewer(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.m_fileDialog = None
        self.pdfView = QPdfView(self)
        self.m_pdf = QPdfDocument()
        self.m_pdf_path = ""

        self.pdf_toolbar = QWidget(self)
        self.doc_open_btn = QPushButton(QIcon(":/icons/Resources/images/document-open.svgz"), "", self)
        self.zoom_in_btn = QPushButton(QIcon(":/icons/Resources/images/zoom-in.svgz"), "", self)
        self.zoom_out_btn = QPushButton(QIcon(":/icons/Resources/images/zoom-out.svgz"), "", self)
        self.zoom_fit_best_btn = QPushButton(QIcon(":/icons/Resources/images/zoom-fit-best.svgz"), "", self)
        self.zoom_fit_width_btn = QPushButton(QIcon(":/icons/Resources/images/zoom-fit-width.svgz"),"", self)
        self.go_next_btn = QPushButton(QIcon(":/icons/Resources/images/go-next-view.svgz"),"", self)
        self.go_prev_btn = QPushButton(QIcon(":/icons/Resources/images/go-previous-view.svgz"),"", self)

        self.initUI()
        self.initActions()

    def initUI(self):
        HLayout = QHBoxLayout()
        VLayout = QVBoxLayout()

        HLayout.addWidget(self.doc_open_btn)
        HLayout.addWidget(self.zoom_in_btn)
        HLayout.addWidget(self.zoom_out_btn)
        HLayout.addWidget(self.zoom_fit_best_btn)
        HLayout.addWidget(self.zoom_fit_width_btn)
        HLayout.addWidget(self.go_prev_btn)
        HLayout.addWidget(self.go_next_btn)
        self.pdf_toolbar.setLayout(HLayout)

        VLayout.addWidget(self.pdf_toolbar)
        VLayout.addWidget(self.pdfView)
        self.setLayout(VLayout)

    def initActions(self):
        self.doc_open_btn.clicked.connect(self.open)
        self.zoom_in_btn.clicked.connect(self.on_actionZoom_In_triggered)
        self.zoom_out_btn.clicked.connect(self.on_actionZoom_Out_triggered)
        self.go_next_btn.clicked.connect(self.on_actionNext_Page_triggered)
        self.go_prev_btn.clicked.connect(self.on_actionPrevious_Page_triggered)
        self.zoom_fit_best_btn.clicked.connect(self.on_actionZoom_Fit_Best_triggered)
        self.zoom_fit_width_btn.clicked.connect(self.on_actionZoom_Fit_Width_triggered)

    def update_zoom_factor(self):
        view_size = self.pdfView.size()
        page_size = self.m_pdf.pagePointSize(self.pdfView.pageNavigator().currentPage())

        if self.pdfView.zoomMode() == QPdfView.ZoomMode.FitInView:
            factor = min(view_size.width() / page_size.width(), view_size.height() / page_size.height())
        elif self.pdfView.zoomMode() == QPdfView.ZoomMode.FitToWidth:
            factor = view_size.width() / page_size.width()
        else:
            factor = self.pdfView.zoomFactor()

        self.pdfView.setZoomFactor(factor)

    def preview(self, doc):
        print("Doc: ", doc)

    @Slot()
    def open(self):
        if not self.m_fileDialog:
            directory = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
            self.m_fileDialog = QFileDialog(self, "Choose a PDF", directory)
            self.m_fileDialog.setAcceptMode(QFileDialog.AcceptOpen)
            self.m_fileDialog.setMimeTypeFilters(["application/pdf"])
        if self.m_fileDialog.exec() == QDialog.Accepted:
            to_open = self.m_fileDialog.selectedUrls()[0]
            if to_open.isValid():
                if to_open.isLocalFile():
                    self.m_pdf_path = to_open.toLocalFile()
                    if self.m_pdf.status() == QPdfDocument.Status.Ready:
                        self.m_pdf.close()
                    self.m_pdf.load(self.m_pdf_path)
                    self.pdfView.setDocument(self.m_pdf)
                    self.page_selected(0)
                else:
                    message = f"{to_open} is not a valid local file"
                    print(message, file=sys.stderr)
                    QMessageBox.critical(self, "Failed to open", message)
    
    @Slot(int)
    def page_selected(self, page):
        nav = self.pdfView.pageNavigator()
        nav.jump(page, QPoint(), nav.currentZoom())

    @Slot()
    def on_actionZoom_In_triggered(self):
        factor = self.pdfView.zoomFactor() * ZOOM_MULTIPLIER
        self.pdfView.setZoomFactor(factor)
        self.pdfView.setZoomMode(QPdfView.ZoomMode.Custom)

    @Slot()
    def on_actionZoom_Out_triggered(self):
        factor = self.pdfView.zoomFactor() / ZOOM_MULTIPLIER
        self.pdfView.setZoomFactor(factor)
        self.pdfView.setZoomMode(QPdfView.ZoomMode.Custom)

    @Slot()
    def on_actionPrevious_Page_triggered(self):
        nav = self.pdfView.pageNavigator()
        pre_page = nav.currentPage()
        if pre_page != 0:
            pre_page -= 1
            nav.jump(pre_page, QPoint(), nav.currentZoom())

    @Slot()
    def on_actionNext_Page_triggered(self):
        nav = self.pdfView.pageNavigator()
        next_page = nav.currentPage()
        if next_page + 1 < self.m_pdf.pageCount():
            next_page += 1
            nav.jump(next_page, QPoint(), nav.currentZoom())

    @Slot()
    def on_actionZoom_Fit_Best_triggered(self):
        self.pdfView.setZoomMode(QPdfView.ZoomMode.FitInView)
        self.update_zoom_factor()

    @Slot()
    def on_actionZoom_Fit_Width_triggered(self):
        self.pdfView.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.update_zoom_factor()

    @Slot(str)
    def export_to_pdf(self, out_path):
        if len(self.m_pdf_path) != 0:
            document = pymupdf.open(self.m_pdf_path)
            document.save(out_path)
            document.close()

    @Slot(str)
    def export_to_word(self, out_path):
        if len(self.m_pdf_path) != 0:
            document = Converter(self.m_pdf_path)
            document.convert(out_path, start=0, end=None)
