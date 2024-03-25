from flask import Flask, request, jsonify, render_template, url_for, session, redirect
from flask_compress import Compress
from dotenv import load_dotenv
load_dotenv()
from routes import rotas
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user, current_user
from dao import dao
from flask_sqlalchemy import SQLAlchemy
from forms.forms import LoginForm
from utils.utils import verify_pass, hash_pass
from database import db
import json
from datetime import timedelta


## importa os models
# from models.usuario import Usuario

app = Flask(__name__)
compress = Compress(app)

app.config['JSON_AS_ASCII'] = False
app.secret_key = '281hnf19bfu1nf'
app.config['SECRET_KEY'] = app.secret_key

app.config['SQLALCHEMY_DATABASE_URI'] = dao.db_str
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

db.init_app(app)

## inicializa login
login_manager = LoginManager(app)
login_manager.login_view = 'rotas.login'

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

from models import *

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/admin/login'
@login_manager.user_loader
def load_user(user_id):
    return dao.get_user(user_id)

# Register the routes
app.register_blueprint(rotas.bp)

@app.route('/rotas')
def get_rotas():
    route_data = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            methods = ','.join(rule.methods)
            url = url_for(rule.endpoint)
            doc = app.view_functions[rule.endpoint].__doc__
            route_data.append((url, methods, doc))
    return render_template('routes.html', route_data=route_data)

# @app.route('/')
# def get_landpage():
#     return render_template('index.html')
#
# @app.route('/admin/login2')
# def route_default():
#     return redirect(url_for('login'))

# @app.route('/admin/logout')
# @login_required
# def logout():
#     dao.desautentica_usuario(current_user)
#     logout_user() # Log out the user
#     return redirect(url_for('route_default'))
#

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
