import sys
from PyQt5.QtWidgets import QApplication
from Widgets.main_window import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.setGeometry(100, 100, 600, 400)
window.show()
sys.exit(app.exec_())
