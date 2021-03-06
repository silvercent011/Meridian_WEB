from flask import Blueprint, url_for, redirect, render_template, request, session
from flask_login import current_user, login_user, logout_user, login_required
from flask import current_app as app

from config import Settings
from src.utils.request import PostWithoutAuth
from src.utils.user_loader import user_load

from src.auth.utils.formUser import AdminLoginForm
from src.auth.utils.modelUser import User, User_Logged

auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='./templates', static_folder='./static')


@auth_bp.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == False:
        form = AdminLoginForm(request.form)
        if request.method == 'POST' and form.validate():
            cpf = request.form.get('cpf')
            senha = request.form.get('senha')
            try:
                data = {"cpf": cpf, "password": senha}
                req = PostWithoutAuth('users/auth', data)
                if 'error' in req:
                    return render_template('login.html', form=form, link=Settings(
                    ).LOGO_LINK, message='Erro ao fazer login. Verifique os dados e tente novamente')
                if req['userData']['_id'] == cpf and 'error' not in req:
                    req1 = req['userData']
                    login_user(user_load(req1), remember=True)
                    session['USR'] = req1
                    session['TKN'] = req['token']
                    return redirect(url_for('auth_bp.painel'))
            except:
                return render_template('login.html', form=form, link=Settings(
                ).LOGO_LINK, message='Não foi possível fazer login, verifique os dados e tente novamente')
        else:
            return render_template('login.html', form=form, link=Settings().LOGO_LINK)
    else:
        return redirect(url_for('auth_bp.painel'))


@auth_bp.route('/home', methods=['GET', 'POST'])
@login_required
def painel():
    return redirect('/admin')


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    [session.pop(key) for key in list(session.keys())]
    logout_user()
    return f"<h1>Deslogado</h1>"


@auth_bp.route('/cadastre', methods=['GET', 'POST'])
@login_required
def cadastre():
    return render_template('cadastre.html')
