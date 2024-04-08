from database import db

class ResultadoQuestionarioPacienteCateg(db.Model):
    __tablename__ = 'resultado_questionario_paciente_categ'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    escore = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    questionario_paciente_id = db.Column(db.Integer, db.ForeignKey('questionario_paciente.id'), nullable=False)
    date_created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    categoria = db.relationship('Categoria', backref=db.backref('resultado_categorias', lazy=True))
    questionario_paciente = db.relationship('QuestionarioPaciente', backref=db.backref('resultado_questionarios', lazy=True))

    def __init__(self, escore, categoria_id, questionario_paciente_id):
        self.escore = escore
        self.categoria_id = categoria_id
        self.questionario_paciente_id = questionario_paciente_id

    def __repr__(self):
        return f"ResultadoQuestionarioPacienteCateg(id={self.id}, escore={self.escore}, categoria_id={self.categoria_id}, questionario_paciente_id={self.questionario_paciente_id}, date_created='{self.date_created}', date_updated='{self.date_updated}')"

    def to_dict(self):
        return {
            'id': self.id,
            'escore': self.escore,
            'categoria_id': self.categoria_id,
            'questionario_paciente_id': self.questionario_paciente_id,
            'date_created': self.date_created.strftime('%Y-%m-%d %H:%M:%S') if self.date_created else None,
            'date_updated': self.date_updated.strftime('%Y-%m-%d %H:%M:%S') if self.date_updated else None
        }