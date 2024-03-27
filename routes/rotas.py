from flask import Blueprint, request, jsonify, redirect, url_for, session, render_template
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user, current_user

import database
from dao import dao
import json
import pandas as pd
import io
from functools import wraps
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from dotenv import load_dotenv

load_dotenv()
from forms.forms import LoginForm
from utils.utils import verify_pass, hash_pass

from flask_dance.contrib.github import github
from flask_login import LoginManager
from flask_login import login_required
from jinja2 import TemplateNotFound

from database import db
from models import usuarios, Usuarios
from senha_cripto import bcrpyt

bp = Blueprint('rotas', __name__)


@bp.route('/admin/uploadCargaQuestionario', methods=['GET', 'POST'])
def upload_carga():
    if request.method == 'POST':
        print("Form Data:", flush=True)
        for key, value in request.form.items():
            print(f"{key}: {value}", flush=True)
        print('##########', flush=True)

        upload = request.files['upload']
        questionario_id = request.form['questionario']

        # ler o csv do forms
        df = pd.read_csv(io.StringIO(upload.read().decode('utf-8')))

        from services import questionarioService
        questionarioService.carga_questionario(questionario_id, df)

        return "File uploaded and processed successfully."
    else:
        from services import questionarioService
        questionarios = questionarioService.get_questionarios()
        return render_template('home/carga_questionario.html',
                               questionarios=questionarios)


@bp.route('/index2', methods=['GET'])
@login_required
def index2():
    print('##################################', flush=True)
    print('ESTOU NA ROTA INDEX2 ###########', flush=True)
    print('##################################', flush=True)
    print('Current user: ', current_user.id_usuario, flush=True)
    print('Current user: ', current_user, flush=True)
    return render_template('home/index.html', segment='index')


@bp.route('/admin/home')
@login_required
def admin_home():
    print('User autenticado', flush=True)


@bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    """For GET requests, display the login form.
    For POSTS, login the current user by processing the form.

    """

    # logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message', level=logging.INFO)
    # logging.info("Admin Logado")
    # print('trying login page...', flush=True)
    # print(db, flush=True)
    # print('hashing 123123: ', hash_pass('123123'), flush=True)
    # print('##################################', flush=True)

    formLogin = LoginForm()
    if formLogin.validate_on_submit():
        usuario = Usuarios.query.filter_by(login=formLogin.username.data).first()
        # if usuario and bcrpyt.check_password_hash(usuario.senha, formLogin.password.data):
        #Ao usar o bcrypt somente quando ja tiver criado o usuario usando o bcrpyt.generate_password_hash
        if usuario and usuario.senha == formLogin.password.data:
            login_user(usuario)
        return redirect(url_for("rotas.index2"))
    return render_template('accounts/login.html', form=formLogin)


@bp.route('/admin/questionario/<int:id>', methods=['GET'])
# @login_required
def get_questionario(id):
    print(f'getting questionario {id}', flush=True)

    from services import questionarioService
    questionarioService.drop_questionario_first()
    questionarioService.cria_questionario_dass()

    return render_template('home/template.html',
                           id=id)


@bp.route('/admin/logout')
@login_required
def logout():
    dao.desautentica_usuario(current_user)
    logout_user()  # Log out the user
    return redirect(url_for('route_default'))


@bp.route('/admin/login2')
def route_default():
    return redirect(url_for('login'))
