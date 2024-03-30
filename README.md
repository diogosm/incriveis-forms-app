# incriveis-forms-app

App web em python + flask

## Como rodar:

### Database settings

O container roda com um volume, se for preciso resetar tudo, use:

- docker rm incriveis_forms_app //remove o container
- docker volume rm incriveis_forms_db_data //remove o volume do banco
- docker inspect --format='{{json .Mounts}}' incriveis_forms_db //verifica o volume

### Para gerar backup do banco

Para gerar backup do banco, rode um comando docker, como esse:

- docker exec incriveis_forms_db mariadb-dump -uadmin -p123123 incriveis_forms > incriveis_forms.sql

### Build settings

- docker-compose up --build -d

# Como testar o ws

Rotas: `http://localhost:5000/`


## Regras de negócio

1. Regras de negócio de controle de acesso
   - RN1: Como usuário gostaria de logar   
2. Regras de negócio do questionário

## Modelagem do software

## Modelagem do banco

## Algoritmos principais
