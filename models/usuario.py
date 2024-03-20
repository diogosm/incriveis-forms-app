from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(255), unique=True)
    senha = Column(String(255))
    nome = Column(String(255))
    date_created = Column(DateTime, default=func.now())
    date_updated = Column(DateTime, default=func.now(), onupdate=func.now())
    usuario_created = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=True)
    usuario_updated = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=True)
    authenticated = Column(Boolean, default=False)

    created_by = relationship('Usuario', foreign_keys=[usuario_created], remote_side=[id_usuario],
                              primaryjoin="Usuario.id_usuario == Usuario.usuario_created")
    updated_by = relationship('Usuario', foreign_keys=[usuario_updated], remote_side=[id_usuario],
                              primaryjoin="Usuario.id_usuario == Usuario.usuario_updated")

    def __init__(self):
        #self.login = login
        #self.senha = senha
        #self.nome = nome
        self.date_created = datetime.now()
        self.date_updated = datetime.now()
    def __repr__(self):
        return f"Usuario(id_usuario={self.id_usuario}, " \
               f"login='{self.login}', senha='{self.senha}', " \
               f"nome='{self.nome}', date_created='{self.date_created}', " \
               f"date_updated='{self.date_updated}', " \
               f"usuario_created={self.usuario_created}, " \
               f"usuario_updated={self.usuario_updated})"

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id_usuario

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
