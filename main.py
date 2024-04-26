import sys
from PyQt5.QtWidgets import QApplication

from Repository.league_repository import LeagueRepo
from Widgets.main_window import MainWindow

app = QApplication(sys.argv)
repo = LeagueRepo()
window = MainWindow(repo)
window.setGeometry(100, 100, 600, 400)
window.show()
sys.exit(app.exec_())
