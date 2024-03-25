from database import db

class Questionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    categorias = db.relationship('Categoria', backref='questionario', lazy=True)

    def __init__(self, nome):
        self.nome = nome

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'date_created': self.date_created.strftime('%Y-%m-%d %H:%M:%S'),
            'date_updated': self.date_updated.strftime('%Y-%m-%d %H:%M:%S')
        }