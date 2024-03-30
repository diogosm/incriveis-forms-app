from database import db

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    questionario_id = db.Column(db.Integer, db.ForeignKey('questionario.id'))
    date_created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    ordem = db.Column(db.Integer, nullable=True)

    questoes = db.relationship('Questao', backref='categoria', lazy=True)

    def __init__(self, nome, questionario_id):
        self.nome = nome
        self.questionario_id = questionario_id

    @classmethod
    def categoria_ordem(cls, nome, questionario_id, ordem):
        categoria = cls(nome, questionario_id)
        categoria.ordem = ordem
        return categoria