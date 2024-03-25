from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db_str = 'mysql+pymysql://' + \
         os.getenv('DB_USERNAME') + \
         ':' + os.getenv('DB_PASS') + '@' + os.getenv('DB_HOST') + \
         ':' + os.getenv('DB_PORT') + '/' + os.getenv('DB_NAME')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_str
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)