from models.classificacaoCategoria import ClassificacaoCategoria

from database import db

'''
    Funcao que trás a classificacao de um escore
'''
def get_classificacao(escore, categoria_id):
    session = db.Session(db.engine)
    print(f"Testando {escore} - {categoria_id} - ", flush=True)
    try:
        # Consulta a tabela classificacao_categoria para encontrar a classificação
        classificacao = session.query(ClassificacaoCategoria).filter(
            ClassificacaoCategoria.escore_inicio <= escore,
            ClassificacaoCategoria.escore_fim >= escore,
            ClassificacaoCategoria.categoria_id == categoria_id
        ).first()

        if classificacao:
            return classificacao.classificacao
        else:
            return "Classificação não encontrada para o escore e critérios especificados."
    finally:
        session.close()