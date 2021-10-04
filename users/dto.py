import json
from utils.null_object import Null


class UserDto:
    NULL = Null()

    def __init__(self, id, username, email, name, admin, birth_date):
        self.id = id
        self.username = username
        self.email = email
        self.name = name
        self.admin = admin
        self.birth_date = birth_date
        self.is_active = True
        self.is_anonymous = not admin
        self.is_authenticated = True

    def get_id(self):
        return self.id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'id': self.id,
                'username': self.username,
                'email': self.email,
                'name': self.name,
                'admin': self.admin,
                'birth_date': str(self.birth_date.strftime('%Y-%m-%dT%H:%M:%S'))}



