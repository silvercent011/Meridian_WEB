from flask_login import UserMixin


class Aluno(UserMixin):
    def __init__(self, id):
        self.id = id


class Aluno_Logged(UserMixin):
    def __init__(self, object):
        self.id = object['_id']
        self.dt_nascimento = object['dt_nascimento']
        self.matricula = object['matricula']
        self.turma = object['turma']
        self.turno = object['turno']
        self.nivel = object['nivel']
        self.created = object['created']
        self.nome = object['nome']
