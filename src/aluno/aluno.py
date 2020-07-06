from flask import Blueprint, url_for, redirect, render_template, request, session
from flask_login import current_user, login_user, logout_user, login_required
from flask import current_app as app

from config import Settings
from src.utils.request import GetWithoutAuth, GetWithKey, GetFree
from src.utils.user_loader import aluno_loader

from src.aluno.utils.formAluno import AlunoForm
from src.aluno.utils.modelAluno import Aluno, Aluno_Logged

from src.admin.admin import returnUser

from unidecode import unidecode

from datetime import datetime

aluno_bp = Blueprint('aluno_bp', __name__,
                     template_folder='./templates', static_folder='./static', url_prefix='/alunos')


# @aluno_bp.route('/', methods=['GET', 'POST'])
# def home():
#     return redirect(url_for('aluno_bp.login'))


def getBoletim():
    return Settings().BOLETIM_LINK


app.jinja_env.globals.update(getBoletim=getBoletim)


def imgAluno():
    return Settings().LINK_IMG_ALUNO


app.jinja_env.globals.update(imgAluno=imgAluno)


def getPosts():
    getted = GetFree(f'posts')[::-1]
    posts = []
    for x in getted:
        x['created'] = x['created'].split('T')[0]
        data = datetime.strptime(x['created'], "%Y-%m-%d").date()
        x['created'] = f'{data.strftime("%d/%m/%Y")}'
        x['dataformat'] = x['expires'].split('T')[0]
        x['dataformat'] = datetime.strptime(x['dataformat'], "%Y-%m-%d").date()
    for x in getted:
        datenow = datetime.now().date()
        if x['dataformat'] >= datenow:
            posts.append(x)
    return posts


def GetAlunoEditForm(data):

    form = AlunoEditForm(data),

    return form


@aluno_bp.route('/', methods=['GET', 'POST'])
def login():
    logout_user()
    posts = getPosts()

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
                    return render_template('aluno.html', form=form, posts=posts, link=Settings().LOGO_LINK, message=req['error'])
                if req['_id'] == matricula and 'error' not in req:
                    login_user(aluno_loader(req))
                    session['ALNAT'] = req
                    return redirect(f'/alunos/{matricula}')
            except:
                return render_template('aluno.html', form=form, posts=posts, link=Settings().LOGO_LINK, message='Erro no servidor, verifique as informações')
        else:
            return render_template('aluno.html', form=form, posts=posts, link=Settings().LOGO_LINK)
    else:
        return render_template('aluno.html', form=form, posts=posts, link=Settings().LOGO_LINK)


@aluno_bp.route('/<aluno_id>', methods=['GET', 'POST'])
@login_required
def painel(aluno_id):
    dados = Aluno_Logged(session['ALNAT'])
    user = returnUser()
    try:
        matific = GetWithKey(f"alunosp/matific/{dados.matricula}")
        if 'error' in matific:
            matific = False
    except:
        matific = False

    try:
        inspira = GetWithKey(f"alunosp/inspira/{dados.matricula}")
        if 'error' in inspira:
            inspira = False
    except:
        inspira = False

    try:
        estuda = GetWithKey(f"alunosp/estuda/{dados.matricula}")
        if 'error' in estuda:
            estuda = False
    except:
        estuda = False

    services = {}
    services['matific'] = matific
    services['inspira'] = inspira
    services['estuda'] = estuda

    return render_template('aluno_info.html', data=dados, services=services, link=Settings().LOGO_LINK)


@aluno_bp.route('/logout')
@login_required
def logout():
    logout_user()
    [session.pop(key) for key in list(session.keys())]
    return redirect('/')


@aluno_bp.route('/<aluno_id>/edit')
@login_required
def edit(aluno_id):
    return redirect(url_for(f'admin_bp.editAluno', matricula=aluno_id))


@aluno_bp.route('/<aluno_id>/delete')
@login_required
def delete(aluno_id):
    return redirect(url_for(f'admin_bp.deleteAluno', matricula=aluno_id))
