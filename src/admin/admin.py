from flask import Blueprint, url_for, redirect, render_template, request
from flask import session, request
from flask_login import current_user, login_user, logout_user, login_required
from flask import current_app as app

from functools import wraps

from config import Settings
from src.utils.request import req_level3
from src.utils.user_loader import user_load

from src.auth.utils.formUser import AdminLoginForm
from src.auth.utils.modelUser import User, User_Logged
from src.aluno.utils.modelAluno import Aluno_Logged
from src.admin.utils.AlunoFilterForm import AlunoFilterForm


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
        'gerenciar_alunos': {'level': '1', 'route': '/admin/alunos', 'title': 'Gerenciar Alunos', 'icon': 'school'},
        'cadastrar_alunos': {'level': '1', 'route': '/cadalunos', 'title': 'Cadastrar Alunos', 'icon': 'person_add'},
        'gerar_codigo': {'level': '5', 'route': '/coduser', 'title': 'Gerar Código de Cadastro', 'icon': 'vpn_key'},
        'cad_user': {'level': '5', 'route': '/caduser', 'title': 'Cadastrar Usuário', 'icon': 'account_box'},
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
    turmas = [(0, '')]
    turmas = turmas + [(int(x['_id']), x['nome'])
                     for x in req_level3('resources/turmas')]
    turnos= [('0', '')]
    turnos = turnos + [('MN', 'Manhã'), ('TR', 'Tarde')]
    alunos_getted = req_level3('alunos')

    form = AlunoFilterForm(request.form)
    form.turma.choices = turmas
    form.turno.choices = turnos

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
        alunos = support
        form = AlunoFilterForm()
    return render_template('manager.html', alunos=alunos, link=Settings().LOGO_LINK, form=form)
