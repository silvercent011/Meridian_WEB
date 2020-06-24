from flask import Blueprint, url_for, redirect, render_template, request
from flask import session, request
from flask_login import current_user, login_user, logout_user, login_required
from flask import current_app as app

from functools import wraps

from config import Settings
from src.utils.request import GetWithUserToken, PostWithUserToken
from src.utils.user_loader import user_load

from src.auth.utils.formUser import AdminLoginForm
from src.auth.utils.modelUser import User, User_Logged
from src.aluno.utils.modelAluno import Aluno_Logged
from src.admin.utils.AlunoFilterForm import AlunoFilterForm
from src.admin.utils.CadAlunoForm import CadAlunoForm


def returnUser():
    try:
        user = User_Logged(session['USR'], session['TKN'])
        session['USRTYPE'] = user.type
    except:
        user = Aluno_Logged(session['ALNAT'])
        session['USRTYPE'] = user.type
    return user


def verifica_admin(func):

    @wraps(func)
    def permission(*args, **kwargs):
        userLogado = returnUser()
        if userLogado.type != 'USER':
            return redirect(url_for('aluno_bp.home'))
        return func(*args, **kwargs)

    return permission


def verificaPermissao():
    user = returnUser()
    links = carregaLink()
    try:
        link = [links[x]for x in links if user.level >= links[x]['level']]
        return link
    except:
        return []


app.jinja_env.globals.update(verificaPermissao=verificaPermissao)


def carregaLink():
    return {
        'gerenciar_alunos': {'level': '1', 'route': '/admin/alunos', 'title': 'Gerenciar Alunos', 'icon': 'school'},
        'cadastrar_alunos': {'level': '1', 'route': '/admin/cadalunos', 'title': 'Cadastrar Alunos', 'icon': 'person_add'},
        'gerar_codigo': {'level': '5', 'route': '/admin/coduser', 'title': 'Gerar Código de Cadastro', 'icon': 'vpn_key'},
        'cad_user': {'level': '5', 'route': '/admin/caduser', 'title': 'Cadastrar Usuário', 'icon': 'account_box'},
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


@admin_bp.route('/alunos', methods=['GET', 'POST'])
@login_required
@verifica_admin
def manager():
    turmas = [(0, '')] + [(int(x['_id']), x['nome'])
                          for x in GetWithUserToken('resources/turmas')]
    turnos = [('0', '')] + [('MN', 'Manhã'), ('TR', 'Tarde')]
    alunos_getted = GetWithUserToken('alunos')

    form = AlunoFilterForm(request.form)
    form.turma.choices = turmas
    form.turno.choices = turnos

    tam = len(alunos_getted)

    alunos = alunos_getted
    if request.method == 'POST':
        support = []
        nome = request.form.get('nome')
        matricula = request.form.get('matricula')
        try:
            turma = request.form.get('turma')
            turma = [trm[1] for trm in turmas if trm[0] == int(turma)][0]
        except:
            turma = ''

        try:
            turno = request.form.get('turno')
            turno = [trn[1] for trn in turnos if trn[0] == turno][0]
        except:
            turno = ''

        for aluno in alunos:
            if matricula in aluno['matricula'] and matricula != '':
                support.append(aluno)
            else:
                if nome.upper() in aluno['nome'] and nome != '':
                    support.append(aluno)
                else:
                    if turma in aluno['turma'] and turma != '':
                        support.append(aluno)
                    else:
                        if turno in aluno['turno'] and turno != '':
                            support.append(aluno)
        if len(support) != 0:
            alunos = support
        #42
    return render_template('manager.html', alunos=alunos, link=Settings().LOGO_LINK, form=form)


@admin_bp.route('/alunos/<matricula>', methods=['GET', 'POST'])
@login_required
@verifica_admin
def viewAluno(matricula):
    session['ALNAT'] = GetWithUserToken(f'alunos/{matricula}')
    return redirect(f'/aluno/data/{matricula}')


@admin_bp.route('/cadalunos', methods=['GET', 'POST'])
@login_required
@verifica_admin
def cadAlunos():
    turmas = [(int(x['_id']), x['nome'])
              for x in GetWithUserToken('resources/turmas')]
    turnos = [('MN', 'Manhã'), ('TR', 'Tarde')]

    form = CadAlunoForm(request.form)
    form.turma.choices = turmas
    form.turno.choices = turnos

    message = None
    color = None

    if request.method == 'POST':
        nome = request.form.get('nome')
        matricula = request.form.get('matricula')
        turma = request.form.get('turma')
        req_turma = GetWithUserToken(f'resources/turmas/{turma}')
        turma = req_turma['nome']
        nivel = req_turma['nivel']
        turno = [trn[1]
                 for trn in turnos if trn[0] == request.form.get('turno')][0]
        dt = request.form.get('dt_nascimento').split('-')
        dt_nascimento = f"{str(dt[-1])}/{str(dt[1])}/{str(dt[0])}"
        query = {
            '_id': matricula,
            'matricula': matricula,
            'nome': nome.upper(),
            'turma': turma,
            'nivel': nivel,
            'dt_nascimento': dt_nascimento,
            'turno': turno
        }

        req = PostWithUserToken('alunos/', query)
        if 'error' in req:
            message = req['error']
            color = 'red'
        else:
            message = f'{nome.upper()} cadastrado com sucesso'
            color = 'green'

    return render_template('cadaluno.html', form=form, link=Settings().LOGO_LINK, message=message, color=color)
