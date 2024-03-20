from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_, cast, String
from sqlalchemy.engine.row import Row
import os, json
from datetime import datetime

'''
    Aqui importe os models definidos em models, ou seja, os modelos do banco
'''
from models.usuario import Usuario

db_str = 'mysql+pymysql://' + \
         os.getenv('DB_USERNAME') + \
         ':' + os.getenv('DB_PASS') + '@' + os.getenv('DB_HOST') + \
         ':' + os.getenv('DB_PORT') + '/' + os.getenv('DB_NAME')
# Create the engine
engine = create_engine(db_str,
                       connect_args={'charset':'utf8'})
# Create a session factory
Session = sessionmaker(bind=engine)


def find_by_username(user_id):
    session = Session()

    try:
        query = session.query(Usuario).filter(Usuario.login == user_id)
        result_size = query.count()
        user = query.first()

        if result_size == 0:
            return None

        return user
    except Exception as e:
        session.rollback()
        print(f"Error validating login: {str(e)}", flush=True)
        return None
    finally:
        session.close()

def get_user(user_id):
    session = Session()

    try:
        query = session.query(Usuario).filter(Usuario.id_usuario == user_id)
        result_size = query.count()
        user = query.first()

        if result_size == 0:
            return None

        return user
    except Exception as e:
        session.rollback()
        print(f"Error validating login: {str(e)}", flush=True)
        return None
    finally:
        session.close()

def autentica_usuario(usuario):
    session = Session()

    try:
        session.add(usuario)
        session.commit()
        usuario.authenticated = True
        session.commit()

        return usuario
    except Exception as e:
        session.rollback()
        print(f"Error validating login: {str(e)}", flush=True)
        return None
    finally:
        session.close()

def desautentica_usuario(usuario):
    session = Session()

    try:
        session.add(usuario)
        session.commit()
        usuario.authenticated = False
        session.commit()

        return usuario
    except Exception as e:
        session.rollback()
        print(f"Error validating login: {str(e)}", flush=True)
        return None
    finally:
        session.close()