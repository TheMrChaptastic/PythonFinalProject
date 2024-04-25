import uuid


class TeamMember():
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.oid = str(uuid.uuid4())

    def __str__(self):
        return f"{self.name}<{self.email}>"
