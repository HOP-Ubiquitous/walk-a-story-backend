from utils.null_object import Null


class User:
    NULL = Null()

    def __init__(self, id, password, username, email, name, admin, birth_date):
        self.id = id
        self.password = password
        self.username = username
        self.email = email
        self.name = name
        self.admin = admin
        self.birth_date = birth_date
