from flask import Blueprint, url_for, redirect, render_template, request
from flask import session
from flask_login import current_user, login_user, logout_user, login_required
from flask import current_app as app

from functools import wraps

from config import Settings
from src.utils.request import req_level1
from src.utils.user_loader import user_load

from src.auth.utils.formUser import AdminLoginForm
from src.auth.utils.modelUser import User, User_Logged
from src.aluno.utils.modelAluno import Aluno_Logged


def returnUser():
    try:
        user = User_Logged(session['USR'], session['TKN'])
    except:
        user = Aluno_Logged(session['ALNAT'])
    return user


def verifica_admin(func):

    @wraps(func)
    def permission():
        userLogado = returnUser()
        if userLogado.type != 'USER':
            return redirect(url_for('aluno_bp.home'))
        return func()

    return permission


def carregaLink():
    """
    Cadastrar Alunos - Cadastrar Alunos, gerenciar dados do inspira e matific
    Gerenciar Alunos
    """
    return {
        'gerenciar_alunos': {'level': '1', 'route': '/manager', 'title': 'Gerenciar Alunos', 'icon':'school'},
        'cadastrar_alunos': {'level': '1', 'route': '/cadalunos', 'title': 'Cadastrar Alunos', 'icon':'person_add'},
        'gerar_codigo': {'level': '5', 'route': '/coduser', 'title': 'Gerar Código de Cadastro', 'icon':'vpn_key'},
        'cad_user': {'level': '5', 'route': '/caduser', 'title': 'Cadastrar Usuário', 'icon':'account_box'},
    }


admin_bp = Blueprint('admin_bp', __name__,
                     template_folder='./templates', static_folder='./static')


@admin_bp.route('/', methods=['GET', 'POST'])
@login_required
@verifica_admin
def main():
    user = returnUser()
    urls = carregaLink()
    return render_template('admin.html', user=user, urls=urls, link=Settings().LOGO_LINK)
