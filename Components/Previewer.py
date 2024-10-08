from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QStandardPaths, QUrl, QPoint, Slot
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtGui import QIcon
from pdf2docx import Converter

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

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

        # Previewer toolbar
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
        # Set up the layout
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

        # Global layout
        VLayout.addWidget(self.pdf_toolbar)
        VLayout.addWidget(self.pdfView)
        self.setLayout(VLayout)

    def initActions(self):
        # Connect Signals&Slots
        self.doc_open_btn.clicked.connect(self.open)
        self.zoom_in_btn.clicked.connect(self.on_actionZoom_In_triggered)
        self.zoom_out_btn.clicked.connect(self.on_actionZoom_Out_triggered)
        self.go_next_btn.clicked.connect(self.on_actionNext_Page_triggered)
        self.go_prev_btn.clicked.connect(self.on_actionPrevious_Page_triggered)
        self.zoom_fit_best_btn.clicked.connect(self.on_actionZoom_Fit_Best_triggered)
        self.zoom_fit_width_btn.clicked.connect(self.on_actionZoom_Fit_Width_triggered)

    def update_zoom_factor(self):
        # Update zoom factor
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
        # Preview doc infos as PDF
        pdf_file = "./temp.pdf"
        c = canvas.Canvas(pdf_file, pagesize=A4)
        width, height = A4

        song = "simsun"
        pdfmetrics.registerFont(TTFont(song, f"{song}.ttc"))
        c.setFont(song, 12)

        # Draw the Name and Time
        c.drawCentredString(300, height - 50, doc["Description"]["name"])
        c.drawCentredString(300, height - 70, doc["Description"]["timeFrom"] + "-" + doc["Description"]["timeTo"])

        # Draw the table
        table_data = doc["TableModel"]
        total_rows = len(table_data)

        row_per_page = 35
        # Table style
        style = [
                    ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # 设置表头背景色
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # 设置表头文字颜色
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 设置对齐方式
                    ('FONTNAME', (0, 0), (-1, 0), song),  # 设置表头字体
                    ('FONTNAME', (0, 1), (-1, -1), song), # 设置表格字体
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 4),  # 设置表头底部填充
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # 设置表格背景色
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # 设置表格网格线
                ]
        for start_row in range(0, total_rows, row_per_page):
            end_row = min(start_row + row_per_page, total_rows)
            table_part = Table(table_data[start_row:end_row])

            if end_row == total_rows:
                style.append(('SPAN', (0, -1), (1, -1)))
                
            table_part.setStyle(TableStyle(style))

            table_width, table_height = table_part.wrap(0, 0)
            x_position = (width - table_width) / 2
            y_position = height - table_height - 90

            table_part.drawOn(c, x_position, y_position)

            if end_row < total_rows:
                c.showPage()
                c.setFont(song, 12)
            else:
                c.drawString(width - 270, y_position - 20, "供货方：")
                c.drawString(width - 270, y_position - 40, "收货方：")
                c.drawString(width - 270, y_position - 60, "对账日期：" + doc["Description"]["date"])

        c.save()

        # Show PDF by pdfView
        self.m_pdf_path = pdf_file
        if self.m_pdf.status() == QPdfDocument.Status.Ready:
            self.m_pdf.close()
        self.m_pdf.load(self.m_pdf_path)
        self.pdfView.setDocument(self.m_pdf)
        self.page_selected(0)

    # Slots
    @Slot()
    def open(self):
        # Open PDF
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
        # Page selected
        nav = self.pdfView.pageNavigator()
        nav.jump(page, QPoint(), nav.currentZoom())

    @Slot()
    def on_actionZoom_In_triggered(self):
        # Zoom in
        factor = self.pdfView.zoomFactor() * ZOOM_MULTIPLIER
        self.pdfView.setZoomFactor(factor)
        self.pdfView.setZoomMode(QPdfView.ZoomMode.Custom)

    @Slot()
    def on_actionZoom_Out_triggered(self):
        # Zoom out
        factor = self.pdfView.zoomFactor() / ZOOM_MULTIPLIER
        self.pdfView.setZoomFactor(factor)
        self.pdfView.setZoomMode(QPdfView.ZoomMode.Custom)

    @Slot()
    def on_actionPrevious_Page_triggered(self):
        # Go to the previous page
        nav = self.pdfView.pageNavigator()
        pre_page = nav.currentPage()
        if pre_page != 0:
            pre_page -= 1
            nav.jump(pre_page, QPoint(), nav.currentZoom())

    @Slot()
    def on_actionNext_Page_triggered(self):
        # Go to the next page
        nav = self.pdfView.pageNavigator()
        next_page = nav.currentPage()
        if next_page + 1 < self.m_pdf.pageCount():
            next_page += 1
            nav.jump(next_page, QPoint(), nav.currentZoom())

    @Slot()
    def on_actionZoom_Fit_Best_triggered(self):
        # Zoom fit best
        self.pdfView.setZoomMode(QPdfView.ZoomMode.FitInView)
        self.update_zoom_factor()

    @Slot()
    def on_actionZoom_Fit_Width_triggered(self):
        # Zoom fit width
        self.pdfView.setZoomMode(QPdfView.ZoomMode.FitToWidth)
        self.update_zoom_factor()

    @Slot(str)
    def export_to_pdf(self, out_path):
        # Export to pdf
        if len(self.m_pdf_path) != 0:
            document = pymupdf.open(self.m_pdf_path)
            document.save(out_path)
            document.close()

    @Slot(str)
    def export_to_word(self, out_path):
        # Export to doc
        if len(self.m_pdf_path) != 0:
            document = Converter(self.m_pdf_path)
            document.convert(out_path, start=0, end=None)
