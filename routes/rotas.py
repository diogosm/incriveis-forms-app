from flask import Blueprint, request, jsonify, redirect, url_for, session
from dao import dao
import json
import pandas as pd
import io
from functools import wraps

bp = Blueprint('rotas', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

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


