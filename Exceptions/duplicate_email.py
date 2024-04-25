class DuplicateEmail(Exception):
    def __init__(self, email):
        self.email = email

    def __str__(self):
        return repr(self.email)
