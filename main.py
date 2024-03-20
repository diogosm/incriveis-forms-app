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
import json

## importa os models
from models.usuario import Usuario

app = Flask(__name__)
compress = Compress(app)
app.config['JSON_AS_ASCII'] = False
app.secret_key = '281hnf19bfu1nf'
app.config['SQLALCHEMY_DATABASE_URI'] = dao.db_str
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

@app.route('/')
def get_landpage():
    return render_template('index.html')

@app.route('/admin/login2')
def route_default():
    return redirect(url_for('login'))

@app.route('/admin/login', methods=['GET', 'POST'])
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
        user = dao.find_by_username(user_id)

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


@app.route('/admin/logout')
@login_required
def logout():
    dao.desautentica_usuario(current_user)
    logout_user() # Log out the user
    return redirect(url_for('route_default'))

@app.route('/admin/home')
@login_required
def admin_home():
    print('User autenticado', flush=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
