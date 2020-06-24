from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import *


class CadAlunoForm(FlaskForm):
    nome = TextField('Nome do Aluno', validators=[DataRequired()])
    matricula = TextField('Matricula', validators=[DataRequired()])
    turma = SelectField('Turma', choices=[], validators=[DataRequired()])
    turno = SelectField('Turno', choices=[], validators=[DataRequired()])
    dt_nascimento = DateField('Data de Nascimento', format="%Y-%m-%d" ,validators=[DataRequired()])
    cadastrar = SubmitField('Cadastrar')
