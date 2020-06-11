from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id):
        self.id = id


class User_Logged(UserMixin):
    def __init__(self, object, token=None):
        self.id = object['_id']
        self.level = object['level']
        self.cpf = object['cpf']
        self.email = object['email']
        self.created = object['created']
        self.nome = object['nome']
        self.token = token

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
