from flask import current_app
from flask_login import LoginManager
from src.auth.utils.modelUser import User
from src.aluno.utils.modelAluno import Aluno

login_manager = LoginManager()
login_manager.init_app(current_app)

@login_manager.user_loader
def user_load(obj):
    try:
        user = User(obj['_id'])
        return user
    except:
        user = User(obj)
        return user

def aluno_loader(obj):
    try:
        user = Aluno(obj['_id'])
        return user
    except:
        user = Aluno(obj)
        return user