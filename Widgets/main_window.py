from PyQt5.QtWidgets import QMainWindow, QListWidget, QAction, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QFileDialog, \
    QMessageBox, QInputDialog, QPushButton

from Exceptions.duplicate_name import DuplicateName
from Exceptions.duplicate_oid import DuplicateOid
from Models.league import League
from Widgets.league_editor import LeagueEditor


class MainWindow(QMainWindow):
    def __init__(self, repository):
        super().__init__()
        self.setWindowTitle('Chappy\'s Curling League Manager')
        self.repo = repository
        self.current_league_index = -1

        self.league_list = QListWidget()
        self.load_action = QAction('Load', self)
        self.save_action = QAction('Save', self)
        self.league_editor = None

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('Leagues:'))
        main_layout.addWidget(self.league_list)

        button_layout = QHBoxLayout()
        button = QPushButton('Add League')
        button.clicked.connect(self.add_league)
        button_layout.addWidget(button)
        button = QPushButton('Edit League')
        button.clicked.connect(self.edit_league)
        button_layout.addWidget(button)
        button = QPushButton('Delete League')
        button.clicked.connect(self.delete_league)
        button_layout.addWidget(button)

        main_layout.addLayout(button_layout)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.create_menus()
        self.create_connections()

    def create_menus(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.load_action)
        file_menu.addAction(self.save_action)

    def create_connections(self):
        self.load_action.triggered.connect(self.load_file)
        self.save_action.triggered.connect(self.save_file)
        self.league_list.currentRowChanged.connect(self.set_current_league)

    def load_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter('Text files (*.txt)')
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            success = self.repo.load_repo(file_path)
            if success:
                if self.league_editor:
                    self.league_editor.close()
                QMessageBox.information(self, 'Message', f'Loaded file: {file_path}')
                self.update_league()
            else:
                QMessageBox.information(self, 'Message', f'Failed to load file: {file_path}')

    def save_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter('Text files (*.txt)')
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            success = self.repo.save_repo(file_path)
            if success:
                QMessageBox.information(self, 'Message', f'Saved file: {file_path}')
            else:
                QMessageBox.information(self, 'Message', f'Failed to save file.')

    def update_league(self):
        self.league_list.clear()
        for leg in self.repo.leagues:
            self.league_list.addItem(leg.name)

    def add_league(self):
        league_name, ok = QInputDialog.getText(self, 'Add League', 'Enter league name:')
        if ok and league_name:
            new_league = League(league_name)
            try:
                success = self.repo.add_league(new_league)
                if success:
                    self.league_list.addItem(new_league.name)
                else:
                    QMessageBox.warning(self, 'Warning', 'Error saving changes.')
            except DuplicateOid:
                QMessageBox.warning(self, 'Error', 'League with the same ID already exists.')
            except DuplicateName:
                QMessageBox.warning(self, 'Error', 'League with the same Name already exists.')

    def edit_league(self):
        if self.current_league_index != -1:
            selected_league = self.repo.leagues[self.current_league_index]
            self.league_editor = LeagueEditor(selected_league, self.repo)
            self.league_editor.show()
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a league to edit.')

    def delete_league(self):
        if self.current_league_index != -1:
            reply = QMessageBox.question(self, 'Delete League', 'Are you sure you want to delete this league?',
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                success = self.repo.delete_league(self.repo.leagues[self.current_league_index])
                if success:
                    self.league_list.takeItem(self.current_league_index)
                    self.current_league_index = -1
                    self.update_league_list()
                else:
                    QMessageBox.warning(self, 'Warning', 'Error saving changes.')
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a league to delete.')

    def update_league_list(self):
        self.league_list.clear()
        for league in self.repo.leagues:
            self.league_list.addItem(league.name)

    def set_current_league(self, index):
        self.current_league_index = index

    def closeEvent(self, event):
        if self.league_editor:
            self.league_editor.close()
        event.accept()
