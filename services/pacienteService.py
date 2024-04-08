from models.paciente import Paciente


def get_pacient():
    print('buscando pacientes...', flush=True)
    return Paciente.query.all()


def get_pacient_by_id(paciente_id):
    return Paciente.query.filter_by(id=paciente_id).first()
