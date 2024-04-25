from PyQt5.QtWidgets import QWidget, QListWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QInputDialog, \
    QMessageBox

from Exceptions.duplicate_oid import DuplicateOid
from Models.team import Team
from Widgets.team_editor import TeamEditor


class LeagueEditor(QWidget):
    def __init__(self, league, parent=None):
        super().__init__(parent)
        self.setWindowTitle('League Editor')
        self.league = league
        self.teams = []
        self.current_team_index = -1
        self.team_editor = None

        self.team_list = QListWidget()
        self.add_team_button = QPushButton('Add Team')
        self.edit_team_button = QPushButton('Edit Team')
        self.delete_team_button = QPushButton('Delete Team')
        self.team_list.currentRowChanged.connect(self.set_current_team)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f'Teams in {self.league.name}:'))
        layout.addWidget(self.team_list)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_team_button)
        button_layout.addWidget(self.edit_team_button)
        button_layout.addWidget(self.delete_team_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.add_team_button.clicked.connect(self.add_team)
        self.edit_team_button.clicked.connect(self.edit_team)
        self.delete_team_button.clicked.connect(self.delete_team)

        self.update_team_list()

    def update_team_list(self):
        self.team_list.clear()
        self.teams = []
        for team in self.league.teams:
            self.team_list.addItem(team.name)
            self.teams.append(team)

    def add_team(self):
        team_name, ok = QInputDialog.getText(self, 'Add Team', 'Enter team name:')
        if ok and team_name:
            try:
                new_team = Team(team_name)
                self.league.add_team(new_team)
                self.update_team_list()
            except DuplicateOid:
                QMessageBox.warning(self, 'Error', 'Team with the same ID already exists.')

    def edit_team(self):
        if self.current_team_index != -1:
            selected_league = self.teams[self.current_team_index]
            self.team_editor = TeamEditor(selected_league)
            self.team_editor.show()
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a league to edit.')

    def delete_team(self):
        selected_item = self.team_list.currentItem()
        if selected_item:
            team_name = selected_item.text()
            reply = QMessageBox.question(self, 'Delete Team', f'Are you sure you want to delete team "{team_name}"?',
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                team_index = self.team_list.currentRow()
                team = self.league.teams[team_index]
                self.league.remove_team(team)
                self.update_team_list()
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a team to delete.')

    def set_current_team(self, index):
        self.current_team_index = index
