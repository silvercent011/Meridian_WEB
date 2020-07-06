from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import *


class AlunoEditForm(FlaskForm):
    matricula = TextField('Matrícula')
    nome = TextField('Nome', validators=[DataRequired()])
    email = TextField('E-mail')
    turma = SelectField('Turma', choices=[], validators=[DataRequired()])
    turno = SelectField('Turno', choices=[], validators=[DataRequired()])
    dt_nascimento = DateField('Data de Nascimento', format="%Y-%m-%d" ,validators=[DataRequired()])
    entrar = SubmitField('Concluir Edição')