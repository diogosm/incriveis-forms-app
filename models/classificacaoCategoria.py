from database import db

class ClassificacaoCategoria(db.Model):
    __tablename__ = 'classificacao_categoria'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classificacao = db.Column(db.String(255), nullable=False)
    escore_inicio = db.Column(db.Integer, nullable=False)
    escore_fim = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    questionario_id = db.Column(db.Integer, db.ForeignKey('questionario.id'), nullable=False)
    date_created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    categoria = db.relationship('Categoria', backref=db.backref('classificacoes', lazy=True))
    questionario = db.relationship('Questionario', backref=db.backref('classificacoes', lazy=True))

    def __init__(self, classificacao, escore_inicio, escore_fim, categoria_id, questionario_id):
        self.classificacao = classificacao
        self.escore_inicio = escore_inicio
        self.escore_fim = escore_fim
        self.categoria_id = categoria_id
        self.questionario_id = questionario_id

    def __repr__(self):
        return f"ClassificacaoCategoria(id={self.id}, classificacao='{self.classificacao}', escore_inicio={self.escore_inicio}, escore_fim={self.escore_fim}, categoria_id={self.categoria_id}, questionario_id={self.questionario_id}, date_created='{self.date_created}', date_updated='{self.date_updated}')"

    def to_dict(self):
        return {
            'id': self.id,
            'classificacao': self.classificacao,
            'escore_inicio': self.escore_inicio,
            'escore_fim': self.escore_fim,
            'categoria_id': self.categoria_id,
            'questionario_id': self.questionario_id,
            'date_created': self.date_created.strftime('%Y-%m-%d %H:%M:%S') if self.date_created else None,
            'date_updated': self.date_updated.strftime('%Y-%m-%d %H:%M:%S') if self.date_updated else None
        }
