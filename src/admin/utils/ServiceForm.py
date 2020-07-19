from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import *


class ServiceEditForm(FlaskForm):
    login = TextField(f'Login:')
    password = TextField(f'Senha:')
    entrar = SubmitField('Concluir Edição')
