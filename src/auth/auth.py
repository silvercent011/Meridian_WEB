from flask import Blueprint, url_for, redirect, render_template, request
from flask_login import current_user, login_user, logout_user, login_required
from flask import current_app as app

from config import Settings
from src.utils.request import req_level1
from src.utils.user_loader import user_load

from src.auth.utils.formUser import AdminLoginForm
from src.auth.utils.modelUser import User

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
            data = {"cpf": cpf, "password": senha}
            requi = req_level1('users/auth', data)['data']
            login_user(user_load(requi), remember=True)
            print(current_user)
            return redirect(url_for('auth_bp.painel'))
        else:
            return render_template('login.html', form=form, link=Settings().LOGO_LINK)
    else:
        return redirect(url_for('auth_bp.painel'))


@auth_bp.route('/home', methods=['GET', 'POST'])
@login_required
def painel():
    return f"<h1>{current_user.id}</h1>"

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return f"<h1>Deslogado</h1>"