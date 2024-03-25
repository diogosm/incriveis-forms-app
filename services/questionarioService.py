from models.questionario import Questionario
from models.categoria import Categoria
from models.questao import Questao
from models.alternativa import Alternativa
from models.paciente import Paciente

from database import db

from flask import jsonify
import pandas as pd

'''
    Funcao de teste para criar o questionario do tipo DASS
'''
def cria_questionario_dass():
    ## Cria o questionario DASS
    questionario = Questionario(nome="DASS")
    db.session.add(questionario)
    db.session.commit()

    ## categorias do questionario
    categoria_map = {
        2: 1, 4: 1, 9: 1, 12: 1, 15: 1, 16: 1, 20: 1,
        1: 2, 3: 2, 6: 2, 8: 2, 14: 2, 18: 2, 19: 2,
        0: 3, 5: 3, 7: 3, 10: 3, 11: 3, 13: 3, 17: 3
    }

    questao_texto_map = {
        0: "1. Achei difícil me acalmar.",
        1: "2. Senti minha boca seca.",
        2: "3. Não consegui vivenciar nenhum sentimento positivo.",
        3: "4. Tive dificuldade de respirar em alguns momentos. (ex: respiração ofegante, falta de ar, sem ter feito nenhum esforço físico)",
        4: "5. Achei difícil ter iniciativa pra fazer as coisas.",
        5: "6. Tive a tendência de reagir de forma exagerada às situações.",
        6: "7. Senti tremores (ex: nas mãos)",
        7: "8. Senti que estava sempre nervoso.",
        8: "9. Preocupei-me com situações em que eu pudesse entrar em pânico e parecesse ridículo (a).",
        9: "10. Senti que não tinha nada a desejar.",
        10: "11. Senti-me agitado.",
        11: "12. Achei difícil relaxar.",
        12: "13. Senti-me depressivo (a) e sem ânimo.",
        13: "14. Fui intolerante com as coisas que me impediam de continuar o que eu estava fazendo.",
        14: "15. Senti que ia entrar em pânico.",
        15: "16. Não consegui me entusiasmar com nada.",
        16: "17. Senti que não tinha valor como pessoa.",
        17: "18. Senti que estava um pouco emotivo/sensível demais.",
        18: "19. Sabia que meu coração estava alterado mesmo sem ter feito nenhum esforço físico. (ex: aumento de frequência cardíaca, disritmia cardíaca)",
        19: "20. Senti medo sem motivo.",
        20: "21. Senti que a vida não tinha sentido."
    }

    categorias = []

    ## cria categorias
    for index_i, categoria in enumerate(["Depressao", "Ansiedade", "Estresse"]):
        print(f"Index: {index_i}, Category: {categoria}", flush=True)

        categoria = Categoria(nome=categoria, questionario_id=questionario.id)
        db.session.add(categoria)
        db.session.commit()

        categorias.append(categoria)

    print("Categorias salvas:", categorias, flush=True)

    for questao_index, texto_questao in questao_texto_map.items():
        categoria_id = categoria_map[questao_index]
        categoria_correspondente = next((c for c in categorias if c.id == categoria_id), None)
        if categoria_correspondente:
            print(f"Questão: {texto_questao}, Categoria correspondente: {categoria_correspondente.nome}", flush=True)
            questao = Questao(texto=texto_questao, categoria_id=categoria_correspondente.id, ordem=questao_index)

            db.session.add(questao)
            db.session.commit()

            ## add alternativas
            for k in range(5):
                alternativa = Alternativa(
                    texto=f"Alternativa {k}",
                    valor_numerico=k,
                    questao_id=questao.id
                )
                db.session.add(alternativa)
                db.session.commit()
        else:
            print(f"Questão: {texto_questao}, Categoria não encontrada para o índice {questao_index}", flush=True)

    print(f"Questionario adicionado!", flush=True)


def carga_questionario(questionario_id, pandas_obj):
    questionario = Questionario.query.get(questionario_id)
    df = pandas_obj

    print(df.head(), flush=True)
    print(df, flush=True)

    for index, row in df.iterrows():
        if pd.isnull(row['ID']) or (pd.notnull(row['ID']) and pd.to_numeric(row['ID'], errors='coerce') != row['ID']):
            print("Stopping main loop")
            break
        print(row, flush=True)
        print('#######################', flush=True)

        respostaParticiapnteHash = hash((row['Endereço de e-mail'], row['Carimbo de data/hora']))
        paciente = get_paciente(row['Endereço de e-mail'],
                                row['Nome:'])

        ## @TODO criar uma funcao generica que seja mapeada a chamada de acordo com o tipo quest
        ## pega as questoes desse
        start_q = 5
        end_q   = (5+21) # sao 21 questoes
        index_col = 0
        ## categorias do questionario
        category_mapping = {
            2: 1, 4: 1, 9: 1, 12: 1, 15: 1, 16: 1, 20: 1,
            1: 2, 3: 2, 6: 2, 8: 2, 14: 2, 18: 2, 19: 2,
            0: 3, 5: 3, 7: 3, 10: 3, 11: 3, 13: 3, 17: 3
        }
        for column in df.columns[start_q:end_q]:
            print(f"Coluna : {column}", flush=True)
            question_text = column
            print(f"{column}: {row[column]}", flush=True)

            print(f"Adding questao {index_col}", flush=True)
            category = category_mapping.get(index_col, -1)

            # question = Question(question_text, category)
            # # Add the answer to the question
            # #print(f"Adding answer {row[column]}")
            # question.answers.append(row[column])
            # #print(f"Questao added {question.question_text} e res: {question.answers}")
            # participant.add_question(question)

            index_col+=1


'''
    Funcao que retorna ou cria um novo paciente se nao existir
    @params:
        - email
        - nome: nome é usado caso nao exista ainda o paciente
'''
def get_paciente(email, nome):
    paciente = Paciente.query.filter_by(email=email).first()
    if not paciente:
        paciente = Paciente(nome = nome, email = email)

        db.session.add(paciente)
        db.session.commit()
    return paciente


'''
    Funcao que busca uma questao dado id questionario e texto da questao
'''
def buscar_questao_por_id_texto(id_questionario, texto_questao):
    # Realiza o join entre as tabelas Questao, Categoria e Questionario
    query = db.session.query(Questao).join(Categoria).join(Questionario)

    # Filtra pela ID do questionário e o texto da questão
    query = query.filter(Questionario.id == id_questionario, Questao.texto == texto_questao)

    # Retorna a questão encontrada ou None se não encontrada
    return query.first()

def drop_questionario_cascata(questionario_id):
    # Encontrar o questionário pelo ID
    questionario = Questionario.query.get(questionario_id)
    if not questionario:
        print("Questionário não encontrado.", flush=True)
        return

    # Excluir todas as alternativas associadas às questões do questionário
    for questao in questionario.questoes:
        for alternativa in questao.alternativas:
            db.session.delete(alternativa)

    # Excluir todas as questões associadas ao questionário
    for questao in questionario.questoes:
        db.session.delete(questao)

    # Excluir todas as categorias associadas ao questionário
    for categoria in questionario.categorias:
        db.session.delete(categoria)

    # Excluir o questionário
    db.session.delete(questionario)

    # Commit das alterações no banco de dados
    db.session.commit()

    print("Questionário e todas as suas categorias, questões e alternativas associadas foram excluídas com sucesso.", flush=True)

def drop_questionario_first():
    ans = Questionario.query.all()
    if ans:
        print(f"Excluindo {ans[0].id} - {ans[0].nome}", flush=True)
        drop_questionario_cascata(ans[0].id)


def get_questionarios():
    return Questionario.query.all()