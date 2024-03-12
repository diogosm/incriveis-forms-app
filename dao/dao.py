from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_, cast, String
from sqlalchemy.engine.row import Row
import os, json
from datetime import datetime

'''
    Aqui importe os models definidos em models, ou seja, os modelos do banco
'''
###from models.usuarios import Usuarios

db_str = 'mysql+pymysql://' + \
         os.getenv('DB_USER') + \
         ':' + os.getenv('DB_PASSWORD') + '@' + os.getenv('DB_HOST') + \
         ':' + os.getenv('DB_PORT') + '/' + os.getenv('DB_NAME')
# Create the engine
engine = create_engine(db_str,
                       connect_args={'charset':'utf8'})
# Create a session factory
Session = sessionmaker(bind=engine)
