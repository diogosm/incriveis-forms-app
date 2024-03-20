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

SELECT 'Tabelas criadas!!';
