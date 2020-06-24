from flask import Blueprint, url_for, redirect, render_template, request, session
from flask_login import current_user, login_user, logout_user, login_required
from flask import current_app as app

from config import Settings
from src.utils.request import GetWithoutAuth, GetWithKey
from src.utils.user_loader import aluno_loader

from src.aluno.utils.formAluno import AlunoForm
from src.aluno.utils.modelAluno import Aluno, Aluno_Logged

from unidecode import unidecode

aluno_bp = Blueprint('aluno_bp', __name__,
                     template_folder='./templates', static_folder='./static', url_prefix='/aluno')


@aluno_bp.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('aluno_bp.login'))


def getBoletim():
    return Settings().BOLETIM_LINK


app.jinja_env.globals.update(getBoletim=getBoletim)


def imgAluno():
    return Settings().LINK_IMG_ALUNO


app.jinja_env.globals.update(imgAluno=imgAluno)


@aluno_bp.route('/data', methods=['GET', 'POST'])
def login():
    logout_user()
    if current_user.is_authenticated == False:
        form = AlunoForm(request.form)
        if request.method == 'POST' and form.validate():
            matricula = request.form.get('matricula')
            dt = str(request.form.get('dt_nascimento')).split('-')
            dt_nascimento = f"{str(dt[-1])}/{str(dt[1])}/{str(dt[0])}"

            try:
                data = {"matricula": matricula, "dt_nascimento": dt_nascimento}
                req = GetWithoutAuth(f'alunosp/{matricula}', data)
                if 'error' in req:
                    return render_template('aluno.html', form=form, link=Settings().LOGO_LINK, message=req['error'])
                if req['_id'] == matricula and 'error' not in req:
                    login_user(aluno_loader(req))
                    session['ALNAT'] = req
                    return redirect(f'/aluno/data/{matricula}')
            except:
                return render_template('aluno.html', form=form, link=Settings().LOGO_LINK, message='Erro no servidor, verifique as informações')
        else:
            return render_template('aluno.html', form=form, link=Settings().LOGO_LINK)
    else:
        return render_template('aluno.html', form=form, link=Settings().LOGO_LINK)


@aluno_bp.route('/data/<aluno_id>', methods=['GET', 'POST'])
@login_required
def painel(aluno_id):
    dados = Aluno_Logged(session['ALNAT'])
    try:
        matific = GetWithKey(f"alunosp/matific/{dados.matricula}")
    except:
        matific = False

    try:
        inspira = GetWithKey(f"alunosp/inspira/{dados.matricula}")
    except:
        inspira = False

    if 'error' in matific:
        matific = False
    if 'error' in inspira:
        inspira = False
    return render_template('aluno_info.html', data=dados, matific=matific, inspira=inspira, link=Settings().LOGO_LINK)


@aluno_bp.route('/logout')
@login_required
def logout():
    logout_user()
    [session.pop(key) for key in list(session.keys())]
    return redirect('/')
