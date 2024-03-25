from database import db

class Alternativa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    valor_numerico = db.Column(db.Integer, nullable=False)
    questao_id = db.Column(db.Integer, db.ForeignKey('questao.id'))
    date_created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # questao = db.relationship('Questao', backref='alternativas', lazy=True)
