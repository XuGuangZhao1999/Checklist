from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QDateTimeEdit, QDoubleSpinBox, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
from PySide6.QtGui import QIcon
from PySide6.QtCore import QDate
import resources_rc
class InfosReciver(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        # Name widget
        self.nameWidget = QWidget(self)
        self.nameLabel = QLabel("Name:", self.nameWidget)
        self.nameLineEdit = QLineEdit(self.nameWidget)

        # Time widget
        self.timeWidget = QWidget(self)
        self.timeFromLabel = QLabel("From:", self.timeWidget)
        self.timeFromDateEdit = QDateTimeEdit(QDate.currentDate(), self.timeWidget)
        self.timeFromDateEdit.setMinimumDate(QDate.currentDate().addDays(-730))
        self.timeFromDateEdit.setMaximumDate(QDate.currentDate().addDays(365))
        self.timeFromDateEdit.setDisplayFormat("yyyy.MM.dd")
        self.timeToLabel = QLabel("To:", self.timeWidget)
        self.timeToDateEdit = QDateTimeEdit(QDate.currentDate(), self.timeWidget)
        self.timeToDateEdit.setMinimumDate(QDate.currentDate().addDays(-730))
        self.timeToDateEdit.setMaximumDate(QDate.currentDate().addDays(365))
        self.timeToDateEdit.setDisplayFormat("yyyy.MM.dd")

        # Date widget
        self.dateWidget = QWidget(self)
        self.dateLabel = QLabel("Date:", self.dateWidget)
        self.dateEdit = QDateTimeEdit(QDate.currentDate(), self.dateWidget)
        self.dateEdit.setMinimumDate(QDate.currentDate().addDays(-730))
        self.dateEdit.setMaximumDate(QDate.currentDate().addDays(365))
        self.dateEdit.setDisplayFormat("yyyy.MM.dd")
        
        # Infos widget
        self.infosWidget = QWidget(self)
        self.infosLabel = QLabel("Infos:", self.infosWidget)
        self.infosDateEdit = QDateTimeEdit(QDate.currentDate(), self.infosWidget)
        self.infosDateEdit.setMinimumDate(QDate.currentDate().addDays(-730))
        self.infosDateEdit.setMaximumDate(QDate.currentDate().addDays(365))
        self.infosDateEdit.setDisplayFormat("yyyy.MM.dd")
        self.infosProductEdit = QLineEdit("Product_name" ,self.infosWidget)
        self.infosUnitEdit = QLineEdit("Unit", self.infosWidget)
        self.infosCountEdit = QDoubleSpinBox(self.infosWidget)
        self.infosPriceEdit = QDoubleSpinBox(self.infosWidget)
        self.infosCountEdit.setRange(-1000, +1000)
        self.infosPriceEdit.setRange(0, 10000)
        
        # Add info button
        self.addInfoBtn = QPushButton(QIcon(":/icons/Resources/images/row_insert_icon.png"), "", self)

        self.initUI()

    def initUI(self):
        # Set up the layout
        nameLayout = QHBoxLayout()
        nameLayout.addWidget(self.nameLabel)
        nameLayout.addWidget(self.nameLineEdit)
        nameLayout.setSpacing(2)
        self.nameWidget.setLayout(nameLayout)
        self.nameWidget.adjustSize()

        timeLayout = QHBoxLayout()
        timeLayout.addWidget(self.timeFromLabel)
        timeLayout.addWidget(self.timeFromDateEdit)
        timeLayout.addWidget(self.timeToLabel)
        timeLayout.addWidget(self.timeToDateEdit)
        timeLayout.setSpacing(2)
        self.timeWidget.setLayout(timeLayout)
        self.timeWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.timeWidget.adjustSize()

        dateLayout = QHBoxLayout()
        dateLayout.addWidget(self.dateLabel)
        dateLayout.addWidget(self.dateEdit)
        dateLayout.setSpacing(2)
        self.dateWidget.setLayout(dateLayout)
        self.dateWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.dateWidget.adjustSize()

        infosLayout = QHBoxLayout()
        infosLayout.addWidget(self.infosLabel)
        infosLayout.addWidget(self.infosDateEdit)
        infosLayout.addWidget(self.infosProductEdit)
        infosLayout.addWidget(self.infosUnitEdit)
        infosLayout.addWidget(self.infosCountEdit)
        infosLayout.addWidget(self.infosPriceEdit)
        infosLayout.setSpacing(2)
        self.infosWidget.setLayout(infosLayout)
        self.infosWidget.adjustSize()

        # Global layout
        VLayout = QVBoxLayout()
        VLayout.addWidget(self.nameWidget)
        VLayout.addWidget(self.timeWidget)
        VLayout.addWidget(self.dateWidget)
        VLayout.addWidget(self.infosWidget)
        VLayout.addWidget(self.addInfoBtn)
        VLayout.setSpacing(2)

        self.setLayout(VLayout)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.adjustSize()

    def getDocDescription(self):
        # Get the document description
        docDescription = dict()
        docDescription["name"] = self.nameLineEdit.text()
        docDescription["timeFrom"] = self.timeFromDateEdit.text()
        docDescription["timeTo"] = self.timeToDateEdit.text()
        docDescription["date"] = self.dateEdit.text()

        return docDescription
