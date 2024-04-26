import uuid


class Team:
    def __init__(self, name):
        self.name = name
        self.members = []
        self.oid = str(uuid.uuid4())

    def __str__(self):
        return f"Team Name: {self.name}, {len(self.members)} members"
