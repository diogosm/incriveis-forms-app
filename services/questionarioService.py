from models.questionario import Questionario
from models.categoria import Categoria
from models.questao import Questao
from database import db

def cria_questionario_dass():
    ## Cria o questionario DASS
    questionario = Questionario(nome="DASS")
    db.session.add(questionario)
    db.session.commit()

    ## cria categorias
    for index_i, categoria in enumerate(["Depressao", "Ansiedade", "Estresse"]):
        print(f"Index: {index_i}, Category: {categoria}")

        category = Categoria(nome=categoria, questionario_id=questionnaire.id)
        db.session.add(category)
        db.session.commit()
