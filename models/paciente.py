from database import db

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)
    date_updated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=True)
    email = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return f"Paciente(id={self.id}, nome='{self.nome}', email='{self.email}', " \
               f"date_created='{self.date_created}', date_updated='{self.date_updated}')"


    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'date_created': self.date_created.strftime('%Y-%m-%d %H:%M:%S'),
            'date_updated': self.date_updated.strftime('%Y-%m-%d %H:%M:%S'),
            'email': self.email
        }

    def to_dict_paciente(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'date_created': self.date_created.strftime('%d-%m-%Y'),
            'date_updated': self.date_updated.strftime('%d-%m-%Y'),
            'email': self.email
        }