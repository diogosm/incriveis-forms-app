from database import db

class Questao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    ordem = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    alternativas = db.relationship('Alternativa', backref='questao', lazy=True)

    def __init__(self, texto, categoria_id, ordem):
        self.texto = texto
        self.categoria_id = categoria_id
        self.ordem = ordem

