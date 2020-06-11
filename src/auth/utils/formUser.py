from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

class AdminLoginForm(FlaskForm):
    cpf = TextField('CPF', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    entrar = SubmitField('Entrar')