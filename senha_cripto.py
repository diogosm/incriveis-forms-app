from flask_bcrypt import Bcrypt

from flask import Flask

app = Flask(__name__)

bcrpyt = Bcrypt(app)
