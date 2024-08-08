from bson.objectid import ObjectId

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password
        }

    @staticmethod
    def from_dict(data):
        return User(data.get('name'), data.get('email'), data.get('password'))
