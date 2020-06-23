from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, SelectField
from wtforms.validators import *


class AlunoFilterForm(FlaskForm):
    nome = TextField('Nome do Aluno')
    matricula = TextField('Matricula')
    turma = SelectField('Turma', choices=[])
    turno = SelectField('Turno', choices=[])
    pesquisar = SubmitField('Pesquisar')
