import uuid

from Exceptions.duplicate_oid import DuplicateOid


class League():
    def __init__(self, name):
        self.name = name
        self.teams = []
        self.oid = str(uuid.uuid4())

    def add_team(self, team):
        for existing in self.teams:
            if team.oid == existing.oid:
                raise DuplicateOid(team.oid)
        self.teams.append(team)

    def remove_team(self, team):
        if team in self.teams:
            self.teams.remove(team)

    def __str__(self):
        return f"League Name: {self.name}, {len(self.teams)} teams"
