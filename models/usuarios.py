from datetime import datetime

from flask_login import UserMixin

from database import db


class Usuarios(db.Model, UserMixin):
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(255), unique=True)
    senha = db.Column(db.String, nullable=False)
    nome = db.Column(db.String(255))
    date_created = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    date_updated = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario_created = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True)
    usuario_updated = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=True)
    # authenticated = db.Column(db.Boolean, default=False)

    # created_by = db.relationship('Usuarios', backref='usuarios_created_by', remote_side=[id_usuario])
    # updated_by = db.relationship('Usuarios', backref='usuarios_updated_by', remote_side=[id_usuario])
    created_by = db.relationship('Usuarios', foreign_keys=[usuario_created], backref='usuarios_created_by', remote_side=[id_usuario])
    updated_by = db.relationship('Usuarios', foreign_keys=[usuario_updated], backref='usuarios_updated_by', remote_side=[id_usuario])


    def __init__(self):
        self.login = Usuarios.login
        self.senha = Usuarios.senha
        self.nome = Usuarios.nome
        self.date_created = datetime.now()
        self.date_updated = datetime.now()
    def __repr__(self):
        return f"Usuario(id_usuario={self.id_usuario}, " \
               f"login='{self.login}', senha='{self.senha}', " \
               f"nome='{self.nome}', date_created='{self.date_created}', " \
               f"date_updated='{self.date_updated}', " \
               f"usuario_created={self.usuario_created}, " \
               f"usuario_updated={self.usuario_updated})"


    def get_id(self):
        return self.id_usuario