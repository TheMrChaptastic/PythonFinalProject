import re
from PyQt5.QtWidgets import QListWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QLineEdit, QMessageBox

from Exceptions.duplicate_email import DuplicateEmail
from Exceptions.duplicate_oid import DuplicateOid
from Models.team_member import TeamMember


class TeamEditor(QWidget):
    def __init__(self, league, team, repository, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Team Editor')
        self.league = league
        self.team = team
        self.repo = repository
        self.current_member_index = -1

        self.member_list = QListWidget()
        self.add_member_button = QPushButton('Add Member')
        self.delete_member_button = QPushButton('Delete Member')
        self.update_member_button = QPushButton('Update Member')
        self.member_list.currentRowChanged.connect(self.set_current_member)

        self.name_line_edit = QLineEdit()
        self.email_line_edit = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Team Members:'))
        layout.addWidget(self.member_list)

        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel('Name:'))
        input_layout.addWidget(self.name_line_edit)
        input_layout.addWidget(QLabel('Email:'))
        input_layout.addWidget(self.email_line_edit)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_member_button)
        button_layout.addWidget(self.delete_member_button)
        button_layout.addWidget(self.update_member_button)

        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.add_member_button.clicked.connect(self.add_member)
        self.delete_member_button.clicked.connect(self.delete_member)
        self.update_member_button.clicked.connect(self.update_member)

        self.update_members_list()

    def update_members_list(self):
        self.member_list.clear()
        for member in self.repo.get_members(self.league, self.team):
            self.member_list.addItem(f"{member.name} <{member.email}>")

    def add_member(self):
        name = self.name_line_edit.text().strip()
        email = self.email_line_edit.text().strip()
        if name and email:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(pattern, email) is None:
                QMessageBox.warning(self, 'Warning', 'Please enter a valid email address \'_____@____.___\'.')
                return
            try:
                success = self.repo.add_member(self.league, self.team, TeamMember(name, email))
                if success:
                    self.member_list.addItem(f"{name} <{email}>")
                    self.name_line_edit.clear()
                    self.email_line_edit.clear()
                else:
                    QMessageBox.warning(self, 'Warning', 'Error saving changes.')
            except DuplicateOid:
                QMessageBox.warning(self, 'Error', 'Member with the same ID already exists.')
            except DuplicateEmail:
                QMessageBox.warning(self, 'Error', 'Member with the same Email already exists.')
        else:
            QMessageBox.warning(self, 'Warning', 'Please enter both name and email.')

    def delete_member(self):
        selected_item = self.member_list.currentItem()
        if selected_item:
            success = self.repo.delete_member(self.league, self.team, self.team.members[self.current_member_index])
            if success:
                self.member_list.takeItem(self.member_list.row(selected_item))
            else:
                QMessageBox.warning(self, 'Warning', 'Error saving changes.')
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a member to delete.')

    def update_member(self):
        selected_item = self.member_list.currentItem()
        if selected_item:
            name = self.name_line_edit.text().strip()
            email = self.email_line_edit.text().strip()
            if name and email:
                pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if re.match(pattern, email) is None:
                    QMessageBox.warning(self, 'Warning', 'Please enter a valid email address \'_____@____.___\'.')
                    return
                self.team.members[self.current_member_index].name = name
                self.team.members[self.current_member_index].email = email
                try:
                    success = self.repo.edit_member(self.league, self.team, self.team.members[self.current_member_index])
                    if success:
                        selected_item.setText(f"{name} <{email}>")
                        self.name_line_edit.clear()
                        self.email_line_edit.clear()
                    else:
                        QMessageBox.warning(self, 'Warning', 'Error saving changes.')
                except DuplicateEmail:
                    QMessageBox.warning(self, 'Warning', 'Another member with the same Email already exists.')
            else:
                QMessageBox.warning(self, 'Warning', 'Please enter both name and email.')
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a member to update.')

    def set_current_member(self, index):
        self.current_member_index = index
