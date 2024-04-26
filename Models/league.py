import uuid

from Exceptions.duplicate_oid import DuplicateOid


class League:
    def __init__(self, name):
        self.name = name
        self.teams = []
        self.oid = str(uuid.uuid4())

    def __str__(self):
        return f"League Name: {self.name}, {len(self.teams)} teams"
