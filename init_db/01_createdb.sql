SELECT 'Dropando tudo. Descomente qndo for para a producao';
DROP DATABASE IF EXISTS incriveis_forms;

-----------------------------------------------------------------------
-----------------------------------------------------------------------
-------------------- Cria o banco e tabelas ---------------------------
-----------------------------------------------------------------------
-----------------------------------------------------------------------

SET foreign_key_checks = 0;
SELECT 'Criando o banco';
CREATE DATABASE IF NOT EXISTS incriveis_forms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE incriveis_forms;

SELECT 'Criando as tabelas';

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(255) UNIQUE,
    senha VARCHAR(255),
    nome VARCHAR(255),
    date_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_created INT,
    usuario_updated INT,
    FOREIGN KEY (usuario_created) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (usuario_updated) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS perfil (
    id_perfil INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    date_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_created INT NOT NULL,
    usuario_updated INT NOT NULL,
    FOREIGN KEY (usuario_created) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (usuario_updated) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS usuario_perfil (
    id_usuario_perfil INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    date_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_created INT NOT NULL,
    usuario_updated INT NOT NULL,
    FOREIGN KEY (usuario_created) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (usuario_updated) REFERENCES usuarios(id_usuario)
    ) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS aplicacao (
    id_aplicacao INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    caminho VARCHAR(255) NOT NULL,
    date_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_created INT NOT NULL,
    usuario_updated INT NOT NULL,
    FOREIGN KEY (usuario_created) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (usuario_updated) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS aplicacaoPerfil (
    id_aplicacao_perfil INT AUTO_INCREMENT PRIMARY KEY,
    id_aplicacao INT NOT NULL,
    id_perfil INT NOT NULL,
    date_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_created INT NOT NULL,
    usuario_updated INT NOT NULL,
    FOREIGN KEY (usuario_created) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (usuario_updated) REFERENCES usuarios(id_usuario),
    PRIMARY KEY (id_aplicacao, id_perfil),
    FOREIGN KEY (id_aplicacao) REFERENCES aplicacao(id_aplicacao),
    FOREIGN KEY (id_perfil) REFERENCES perfil(id_perfil)
) ENGINE=InnoDB;

SELECT 'Tabelas de controle de acesso criadas!!';

SELECT 'Criando tabelas dos questionarios...';

CREATE TABLE Questionario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    questionario_id INT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (questionario_id) REFERENCES Questionario(id)
);

CREATE TABLE Questao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    texto TEXT NOT NULL,
    categoria_id INT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES Categoria(id)
);

CREATE TABLE Alternativa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    texto TEXT NOT NULL,
    valor_numerico INT NOT NULL,
    questao_id INT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (questao_id) REFERENCES Questao(id)
);

CREATE TABLE Paciente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Questionario_Paciente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT,
    questionario_id INT,
    busca VARCHAR(255) NOT NULL,
    FOREIGN KEY (paciente_id) REFERENCES Paciente(id),
    FOREIGN KEY (questionario_id) REFERENCES Questionario(id)
);

CREATE TABLE Resposta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT,
    questao_id INT,
    alternativa_id INT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (paciente_id) REFERENCES Paciente(id),
    FOREIGN KEY (questao_id) REFERENCES Questao(id),
    FOREIGN KEY (alternativa_id) REFERENCES Alternativa(id)
);

alter table Resposta
    add questionario_paciente_id int not null;

alter table Resposta
    add constraint Resposta_Questionario_Paciente_id_fk
        foreign key (questionario_paciente_id) references Questionario_Paciente (id);

alter table Questao
    add ordem int not null;


rename table Alternativa to alternativa;
rename table Categoria to categoria;
rename table Paciente to paciente;
rename table Questao to questao;
rename table Questionario to questionario;
rename table Questionario_Paciente to questionario_paciente;
rename table Resposta to resposta;

alter table paciente
    add email varchar(255) not null;

alter table paciente
    add constraint paciente_pk
        unique (email);


SELECT 'Tabelas dos questionarios criadas!!';

# DELIMITER //
# CREATE TRIGGER populate_busca_questionario_paciente BEFORE INSERT ON Questionario_Paciente
#     FOR EACH ROW
# BEGIN
#     SET NEW.busca = MD5(CONCAT(NEW.paciente_id, NEW.questionario_id, RAND()));
# END;
# //
# DELIMITER ;

# DELIMITER //
# CREATE FUNCTION calcular_pontuacao_paciente_questionario(paciente_id INT, questionario_id INT) RETURNS INT
# BEGIN
#     DECLARE pontuacao INT;
#     SELECT SUM(a.valor_numerico)
#     INTO pontuacao
#     FROM Resposta r
#          JOIN Alternativa a ON r.alternativa_id = a.id
#          JOIN Questao q ON r.questao_id = q.id
#          JOIN Categoria c ON q.categoria_id = c.id
#     WHERE r.paciente_id = paciente_id AND q.questionario_id = questionario_id
#     GROUP BY c.id;
#     RETURN pontuacao;
# END;
# //
# DELIMITER ;