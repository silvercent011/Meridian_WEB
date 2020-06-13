from flask import Blueprint, url_for, redirect, render_template, request, session
from flask_login import current_user, login_user, logout_user, login_required
from flask import current_app as app

from config import Settings
from src.utils.request import req_level1
from src.utils.user_loader import user_load

from src.auth.utils.formUser import AdminLoginForm
from src.auth.utils.modelUser import User, User_Logged

admin_bp = Blueprint('admin_bp', __name__,
                     template_folder='./templates', static_folder='./static')


@admin_bp.route('/', methods=['GET', 'POST'])
@login_required
def main():
    user = returnUser()
    urls = carregaLink()
    return render_template('admin.html', user=user, urls=urls ,link=Settings().LOGO_LINK)


def returnUser():
    return User_Logged(session['USR'], session['TKN'])


def verificaPermissao():
    userLogado = User_Logged(session['USR'], session['TKN'])


def carregaLink():
    return {
        'gerenciar_alunos': {'level': '1', 'route': '/manager', 'title': 'Gerenciar Alunos'},
        'cadastro_matific': {'level': '1', 'route': '/cadmatific', 'title': 'Dados Matific'},
        'cadastro_inspira': {'level': '1', 'route': '/cadinspira', 'title': 'Dados Opet Inspira'}, }
