from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.simple import SubmitField
from wtforms.validators import Email, DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username',
                           id='username_login',
                           validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class RegisterForm(FlaskForm):
    login = StringField('Username',
                        id='login',
                        validators=[DataRequired()])
    nome = StringField('Nome do Usuario',
                       validators=[DataRequired()])

    senha = PasswordField('Password',
                          id='senha',
                          validators=[DataRequired()])

    confirmacao_senha = PasswordField("Confirmação de Senha", id='confirmacao_senha',validators=[DataRequired()])

