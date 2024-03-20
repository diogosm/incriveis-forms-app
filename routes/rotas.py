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

from flask_dance.contrib.github import github
from flask_login import LoginManager
from flask_login import login_required
from jinja2 import TemplateNotFound

bp = Blueprint('rotas', __name__)

@bp.route('/uploadCarga', methods=['POST'])
def upload_carga():
    if request.method == 'POST':
        file = request.files['file']
        option = request.form['option']

        # ler o csv do forms
        df = pd.read_csv(io.StringIO(file.read().decode('utf-8')), sep=';')

        # Process the CSV data based on the selected option
        # This is a placeholder for your processing logic
        print(f"Tipo questionario: {option}",flush=True)
        ##print(df.head(),flush=True)

        for index, row in df.iterrows():
            print(f"Paciente: {row['usuario']}",flush=True)
            print(flush=True)

            cat1 = row['q1']-1
            cat2 = row['q2']-1
            cat3 = row['q3']-1

            print(f"\tPontuacoes por categoria:", flush=True)
            print(f"\t\tCategoria 1: {cat1}", flush=True)
            print(f"\t\tCategoria 2: {cat2}", flush=True)
            print(f"\t\tCategoria 3: {cat3}", flush=True)

        return "File uploaded and processed successfully."


@bp.route('/index2', methods=['GET'])
@login_required
def index2():
    print('##################################', flush=True)
    print('ESTOU NA ROTA INDEX2 ###########', flush=True)
    print('##################################', flush=True)
    print('Current user: ', current_user.id_usuario, flush=True)
    print('Current user: ', current_user, flush=True)
    return render_template('home/index.html', segment='index')


