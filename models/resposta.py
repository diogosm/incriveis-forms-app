from database import db
from sqlalchemy import ForeignKey, Index
class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=True)
    questao_id = db.Column(db.Integer, db.ForeignKey('questao.id'), nullable=True)
    alternativa_id = db.Column(db.Integer, db.ForeignKey('alternativa.id'), nullable=True)
    date_created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)
    date_updated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=True)
    questionario_paciente_id = db.Column(db.Integer, db.ForeignKey('questionario_paciente.id'), nullable=False)

    # Relationships
    paciente = db.relationship('Paciente', backref='respostas', lazy=True)
    questao = db.relationship('Questao', backref='respostas', lazy=True)
    alternativa = db.relationship('Alternativa', backref='respostas', lazy=True)
    questionario_paciente = db.relationship('QuestionarioPaciente', backref='respostas', lazy=True)


    def __init__(self, paciente_id=None, questao_id=None, alternativa_id=None, questionario_paciente_id=None):
        self.paciente_id = paciente_id
        self.questao_id = questao_id
        self.alternativa_id = alternativa_id
        self.questionario_paciente_id = questionario_paciente_id

    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'questao_id': self.questao_id,
            'alternativa_id': self.alternativa_id,
            'date_created': self.date_created.strftime('%Y-%m-%d %H:%M:%S') if self.date_created else None,
            'date_updated': self.date_updated.strftime('%Y-%m-%d %H:%M:%S') if self.date_updated else None,
            'questionario_paciente_id': self.questionario_paciente_id
        }