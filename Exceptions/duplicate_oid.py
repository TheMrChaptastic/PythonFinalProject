class DuplicateOid(Exception):
    def __init__(self, oid):
        self.oid = oid

    def __str__(self):
        return repr(self.oid)