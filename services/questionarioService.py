from models.questionario import Questionario
from models.categoria import Categoria
from models.questao import Questao
from models.alternativa import Alternativa
from models.paciente import Paciente

from models.questionarioPaciente import QuestionarioPaciente
from models.resposta import Resposta

from database import db

from sqlalchemy import exc
from flask import jsonify
import pandas as pd
import hashlib

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
        # print(f"Index: {index_i}, Category: {categoria}", flush=True)

        categoria = Categoria.categoria_ordem(nome=categoria, questionario_id=questionario.id, ordem=index_i)
        db.session.add(categoria)
        db.session.commit()

        categorias.append(categoria)

    print("Categorias salvas:", categorias, flush=True)

    for questao_index, texto_questao in questao_texto_map.items():
        categoria_ordem = categoria_map[questao_index] - 1
        categoria_correspondente = next((c for c in categorias if c.ordem == categoria_ordem
                                         and c.questionario_id == questionario.id), None)
        # print("\tCategoria id: ", categoria_ordem, flush=True)
        # print("\tCategoria correspo: ", categoria_correspondente, flush=True)
        if categoria_correspondente:
            # print(f"Questão: {texto_questao}, Categoria correspondente: {categoria_correspondente.nome}", flush=True)
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

    for index, row in df.iterrows():
        if pd.isnull(row['ID']) or (pd.notnull(row['ID']) and pd.to_numeric(row['ID'], errors='coerce') != row['ID']):
            print("Stopping main loop")
            break
        print('#######################', flush=True)

        encoded_str_key = f"{row['Endereço de e-mail']}{row['Carimbo de data/hora']}"
        resposta_participante_hash = hashlib.md5(encoded_str_key.encode()).hexdigest()# hash((row['Endereço de e-mail'], row['Carimbo de data/hora']))
        paciente = get_paciente(row['Endereço de e-mail'],
                                row['Nome:'])
        questionario_paciente = get_questionario_paciente_by_hash(resposta_participante_hash)

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

        print(f"Adicionando respostas de {paciente.nome}", flush=True)
        if not questionario_paciente:
            questionario_paciente = add_questionario_paciente(paciente, questionario_id, resposta_participante_hash)

        for column in df.columns[start_q:end_q]:
            question_text = column
            category = category_mapping.get(index_col, -1)
            questao = get_questao_by_texto(column)

            if questao:
                print(f"\tQuestao found: ", questao.id, ". Categoria: ", questao.categoria.nome, flush=True)
                ## add resposta
                resposta = Resposta(paciente_id=paciente.id,
                                    questao_id=questao.id,
                                    alternativa_id=get_alternativa_by_questao(questao.id, row[column]).id,
                                    questionario_paciente_id=questionario_paciente.id)
                add_resposta(resposta)
            else:
                print(f"Questao not found!", flush=True)

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

    try:
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
    except Exception as e:
        print("Falha: ", repr(e), flush=True)

def drop_questionario_first():
    ans = Questionario.query.all()
    if ans:
        print(f"Excluindo {ans[0].id} - {ans[0].nome}", flush=True)
        drop_questionario_cascata(ans[0].id)


def get_questionarios():
    return Questionario.query.all()


'''
    Busca categoria pelo id
'''
def get_categoria_by_id(id):
    return Categoria.query.filter_by(id=id).first()


'''
    Busca questao pelo texto
'''
def get_questao_by_texto(texto_questao):
    query = db.session.query(Questao).join(Categoria).join(Questionario)
    query = query.filter(Questao.texto == texto_questao)
    return query.first()


'''
    Busca questionario paciente pela chave de busca:
        (hash((row['Endereço de e-mail'], row['Carimbo de data/hora']))
'''
def get_questionario_paciente_by_hash(resposta_participante_hash):
    return QuestionarioPaciente. \
            query. \
            filter_by(busca=resposta_participante_hash). \
            first()


'''
    Adicionar o questionario paciente para um dado paciente
    e dado questionario_id e a chave de busca
    
'''
def add_questionario_paciente(paciente, questionario_id, resposta_participante_hash):
    questionario_paciente = QuestionarioPaciente(paciente_id=paciente.id, questionario_id=questionario_id, busca=resposta_participante_hash)
    db.session.add(questionario_paciente)
    try:
        db.session.commit()
        return questionario_paciente
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(f"Falha no commit: {e}", flush=True)
    return None


'''
    Retorna a alternativa selecionada da questao dado o valor numerico
    e o id da questao
'''
def get_alternativa_by_questao(questao_id, valor_numerico):
    return Alternativa.query.filter_by(questao_id=questao_id, valor_numerico=valor_numerico).first()


def add_resposta(resposta):
    db.session.add(resposta)
    try:
        db.session.commit()
        return resposta
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(f"Falha no commit: {e}", flush=True)
    return None


def get_questionarios_paciente_respostas(paciente_id, busca):
    ans = {}
    questionarios_pacientes = QuestionarioPaciente.query.filter_by(paciente_id=paciente_id, busca=busca).all()

    for qp in questionarios_pacientes:
        questionario = Questionario.query.get(qp.questionario_id)
        respostas = Resposta.query.filter_by(questionario_paciente_id=qp.id).all()

        # Adiciona o Questionario e suas Respostas ao dicionário de resultados
        ans[questionario] = {
            'questionario_paciente': qp.to_dict(),
            'respostas': [resposta.to_dict() for resposta in respostas]
        }

    ## debug
    for questionario, detalhes in ans.items():
        print(f"Questionario: {questionario.nome}", flush=True)
        print(f"QuestionarioPaciente: {detalhes['questionario_paciente']}", flush=True)
        print("Respostas:", flush=True)
        for resposta in detalhes['respostas']:
            print(resposta, flush=True)
        print("\n", flush=True)

    return ans


def cria_questionario(nomeQuestionario, params):
    print(f"Nome do Questionário: {nomeQuestionario}", flush=True)

    for categoria, questoes in params.items():
        print(f"Categoria: {categoria}", flush=True)

        for questao, alternativas in questoes:
            print(f"Questão: {questao}", flush=True)
            for alternativa, _ in alternativas:
                print(f"Alternativa: {alternativa}", flush=True)

        print("\n", flush=True)