from models.paciente import Paciente


def get_pacient():
    return Paciente.query.all()