from database import db

class QuestionarioPaciente(db.Model):
    __tablename__ = 'questionario_paciente'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=True)
    questionario_id = db.Column(db.Integer, db.ForeignKey('questionario.id'), nullable=True)
    busca = db.Column(db.String(255), nullable=False)

    def __init__(self, paciente_id, questionario_id, busca):
        self.paciente_id = paciente_id
        self.questionario_id = questionario_id
        self.busca = busca

    def __repr__(self):
        return f"QuestionarioPaciente(id={self.id}, paciente_id={self.paciente_id}, questionario_id={self.questionario_id}, busca='{self.busca}')"

    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'questionario_id': self.questionario_id,
            'busca': self.busca
        }