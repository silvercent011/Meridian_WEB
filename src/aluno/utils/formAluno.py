from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import *


class AlunoForm(FlaskForm):
    matricula = TextField('Matrícula', validators=[DataRequired()])
    dt_nascimento = DateField('Data de Nascimento', format="%Y-%m-%d" ,validators=[DataRequired()])
    entrar = SubmitField('Entrar')
