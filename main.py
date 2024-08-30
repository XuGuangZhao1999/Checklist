import sys
from MainWindow import MainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
import resources_rc

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(":/icons/Resources/images/dollar_icon.png"))
app.setApplicationDisplayName("Checklist")

window = MainWindow()
window.show()

sys.exit(app.exec())