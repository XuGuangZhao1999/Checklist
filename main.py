import sys
from MainWindow import MainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
import resources_rc


app = QApplication(sys.argv)
icon = QIcon(":/icons/Resources/images/dollar_icon.png")
app.setWindowIcon(icon)
app.setApplicationDisplayName("Checklist")

window = MainWindow()
window.setWindowIcon(icon)
window.show()

sys.exit(app.exec())