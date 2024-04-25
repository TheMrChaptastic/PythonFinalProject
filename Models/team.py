import uuid

from Exceptions.duplicate_email import DuplicateEmail
from Exceptions.duplicate_oid import DuplicateOid


class Team():
    def __init__(self, name):
        self.name = name
        self.members = []
        self.oid = str(uuid.uuid4())

    def add_member(self, member):
        for existing in self.members:
            if member.email.lower() == existing.email.lower():
                raise DuplicateEmail(member.email)
            elif member.oid == existing.oid:
                raise DuplicateOid(member.oid)
        self.members.append(member)

    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)

    def __str__(self):
        return f"Team Name: {self.name}, {len(self.members)} members"
