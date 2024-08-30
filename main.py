import sys
from MainWindow import MainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("./Resources/dollar_icon.png"))
app.setApplicationDisplayName("Checklist")

window = MainWindow()
window.show()

sys.exit(app.exec())