from models.paciente import Paciente


def get_pacient():
    print('buscando pacientes...', flush=True)
    return Paciente.query.all()