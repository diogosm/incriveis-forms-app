import bcrypt
from flask import Blueprint, request, jsonify, redirect, url_for, session, render_template, flash, abort, session
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
from forms.forms import *
from utils.utils import verify_pass, hash_pass

from flask_dance.contrib.github import github
from flask_login import LoginManager
from flask_login import login_required
from jinja2 import TemplateNotFound

from database import db
from models import usuarios, Usuarios
from senha_cripto import bcrpyt

from services import questionarioService
from services import pacienteService

bp = Blueprint('rotas', __name__)


@bp.route('/admin/uploadCargaQuestionario', methods=['GET', 'POST'])
def upload_carga():
    questionarios = questionarioService.get_questionarios()

    if request.method == 'POST':
        for key, value in request.form.items():
            print(f"{key}: {value}", flush=True)

        upload = request.files['upload']
        questionario_id = request.form['questionario']

        # ler o csv do forms
        df = pd.read_csv(io.StringIO(upload.read().decode('utf-8')))

        questionarioService.carga_questionario(questionario_id, df)

        return render_template('home/carga_questionario.html',
                               questionarios=questionarios,
                               flash_message="Carga feita com sucesso!")
    else:
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
        # Ao usar o bcrypt somente quando ja tiver criado o usuario usando o bcrpyt.generate_password_hash
        if usuario and usuario.senha == formLogin.password.data:
            login_user(usuario)
            print("Login sucessful", flush=True)
        return redirect(url_for("rotas.index2"))
    return render_template('accounts/login.html', form=formLogin)


@bp.route('/admin/cadastro', methods=['GET', 'POST'])
@login_required
def criar_usuario():
    formCriarUsuario = RegisterForm()
    if formCriarUsuario.validate_on_submit():
        login_existente = Usuarios.query.filter_by(login=formCriarUsuario.login.data).first()

        if formCriarUsuario.senha.data == formCriarUsuario.confirmacao_senha.data and not login_existente:
            try:
                usuario = Usuarios()
                usuario.nome = formCriarUsuario.nome.data
                usuario.senha = formCriarUsuario.senha.data
                usuario.login = formCriarUsuario.login.data
                db.session.add(usuario)
                db.session.commit()
                print('Usuário criado com sucesso', flush=True)
            except Exception as e:
                print(f"Erro ao criar usuário: {str(e)}", flush=True)
                formCriarUsuario.login.errors.append("Usuário ja existente")
                db.session.rollback()
                flash('Ocorreu um erro ao criar o usuário. Por favor, tente novamente.', 'error')
        elif login_existente:
            flash('O login já está em uso. Por favor, escolha outro.', 'error')
        else:
            formCriarUsuario.confirmacao_senha.errors.append('As senhas não coincidem')

    return render_template('home/cadastro_usuario.html', form=formCriarUsuario)



@bp.route('/admin/questionario/<int:id>', methods=['GET'])
# @login_required
def get_questionario(id):
    print(f'getting questionario {id}', flush=True)

    # questionarioService.drop_questionario_first()
    questionarioService.cria_questionario_dass()

    return render_template('home/template.html',
                           id=id)


@bp.route('/pacientes/<int:paciente_id>', methods=['GET'])
# @login_required
def get_paciente(paciente_id):
    paciente = pacienteService.get_pacient_by_id(paciente_id)
    if not paciente:
        # Handle the case where the paciente is not found
        return "Paciente not found", 404
    paciente = paciente.to_dict_paciente() # Ajust hour
    # Pass the paciente data to the template for rendering
    return render_template('home/paciente.html', paciente=paciente)


@bp.route('/admin/logout')
@login_required
def logout():
    dao.desautentica_usuario(current_user)
    logout_user()  # Log out the user
    return redirect(url_for('rotas.login'))


@bp.route('/admin/login2')
def route_default():
    return redirect(url_for('login'))


@bp.route('/pacientes', methods=['GET', 'POST'])
def pacientes():
    return render_template('home/pacientes.html')


@bp.route('/pacientesData', methods=['GET'])
def pacientesData():
    patients = pacienteService.get_pacient()  # Fetch all patients from the database
    patient_data = [patient.to_dict() for patient in patients]  # Convert to list of dictionaries
    return jsonify(patient_data)  # Return JSON response


@bp.route('/pacienteQuestionario', methods=['GET'])
# def paciente_questionario(paciente_id):
def paciente_questionario():
    if 'paciente_id' not in request.args or 'busca' not in request.args:
        return jsonify({"error": "Erro na passagem de parâmetros"}), 400

    paciente_id = request.args.get('paciente_id', default='', type=int)
    busca = request.args.get('busca', default='', type=str)

    ans = questionarioService.get_questionarios_paciente_respostas(paciente_id, busca)

    primeira_chave = next(iter(ans))
    primeiro_questionario = ans[primeira_chave]
    categorias = questionarioService.get_categoria_by_questionario(
        primeiro_questionario['questionario_paciente']['questionario_id'])
    escores = questionarioService.get_escore_by_questionario_paciente(busca)
    paciente = pacienteService.get_pacient_by_id(paciente_id)

    # questionarioService.get_questionarios_paciente_respostas(paciente_id)
    print("#################", flush=True)
    return render_template('home/questionario_paciente.html',
                           ans=ans,
                           categorias=categorias,
                           escores=escores,
                           paciente=paciente)


@bp.route('/teste/criaQuestionario', methods=['GET'])
def cria_questionario():
    questionarioService.cria_questionario(
        'Nome questionario',
        {
            'categoria 1': [
                ('questao 1',
                 [
                     ('alternativa 1', 0),
                     ('alternativa 2', 1),
                     ('alternativa 3', 2),
                     ('alternativa 4', 3)
                 ]),
                ('questao 2',
                 [
                     ('alternativa 1', 0),
                     ('alternativa 2', 1),
                     ('alternativa 3', 2),
                     ('alternativa 4', 3)
                 ])
            ],
            'categoria 2': [
                ('questao 3',
                 [
                     ('alternativa 1', 0),
                     ('alternativa 2', 1),
                     ('alternativa 3', 2),
                     ('alternativa 4', 3)
                 ])
            ]
        }
    )
    return 'questionario criado'
