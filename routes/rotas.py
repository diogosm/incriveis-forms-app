from flask import Blueprint, request, jsonify, redirect, url_for, session, render_template
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user, current_user
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
from models import usuarios

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



@bp.route('/pacientes', methods=['GET', 'POST'])
def pacientes():
        return render_template('home/pacientes.html')


@bp.route('/pacientesData', methods=['GET'])
def pacientesData():
    from services import pacienteService
    patients = pacienteService.get_pacient()  # Fetch all patients from the database
    patient_data = [patient.to_dict() for patient in patients]  # Convert to list of dictionaries
    return jsonify(patient_data)  # Return JSON response


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
    print('##################################', flush=True)
    print('trying login page...', flush=True)
    print(db, flush=True)
    print('hashing 123123: ', hash_pass('123123'), flush=True)
    print('##################################', flush=True)

    login_form = LoginForm(request.form)
    if 'login' in request.form:

        user_id  = request.form['username']
        password = request.form['password']

        # Locate user
        print("## Vou testar: ", user_id, flush=True)
        #user = Usuario.find_by_username(user_id)
        # user = dao.find_by_username(user_id)
        user = Usuarios.query.filter_by(login=user_id).first()

        # if user not found
        if not user:
            return render_template( 'accounts/login.html',
                                    msg='Unknown User or Email',
                                    form=login_form)

        # Check the password
        if verify_pass(password, user.senha):
            dao.autentica_usuario(user.id_usuario)
            login_user(user)
            return redirect(url_for('route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('rotas.index2'))


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
    logout_user() # Log out the user
    return redirect(url_for('route_default'))


@bp.route('/admin/login2')
def route_default():
    return redirect(url_for('login'))