
CREATE TABLE usuario (
  id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nome_completo varchar(255) NOT NULL,
  nome_usuario varchar(255) NOT NULL UNIQUE,
  senha varchar(255) NOT NULL
)

INSERT INTO usuario(nome_completo, nome_usuario, senha) VALUES ('Mucano Cruz', 'mucano', '12345');
INSERT INTO usuario(nome_completo, nome_usuario, senha) VALUES ('João Vela', 'joaov', 'abcde');
INSERT INTO usuario(nome_completo, nome_usuario, senha) VALUES ('Herman José', 'herman', 'abcde');

CREATE TABLE estado (
  id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nome varchar(255) NOT NULL
)

INSERT INTO estado (nome) VALUES ('Em curso'); 
INSERT INTO estado (nome) VALUES ('Concluída')

CREATE TABLE tarefa (
    id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    titulo varchar(255) NOT NULL,
    descricao varchar(255) NOT NULL,
    id_estado INT, 
    id_usuario INT, 
    FOREIGN KEY (id_estado) REFERENCES estado(id) 
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)

INSERT INTO tarefa (titulo, descricao, id_estado, id_usuario) 
VALUES ('Reunião OMATAPALO', "Encontro de acertos com o corpo directivo as 09h00", 1, 1);

INSERT INTO tarefa (titulo, descricao, id_estado, id_usuario) 
VALUES ('Visita à base da SONILS', "Visita e sessões de trocas de experiência", 1, 2);

CREATE TABLE tarefa_usuario (
    id_tarefa INT, 
    id_usuario INT, 
    FOREIGN KEY (id_tarefa) REFERENCES tarefa(id),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) 
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    PRIMARY KEY (id_tarefa, id_usuario)
)

INSERT INTO tarefa_usuario (id_tarefa, id_usuario) VALUES (1,2);
INSERT INTO tarefa_usuario (id_tarefa, id_usuario) VALUES (2,1);
INSERT INTO tarefa_usuario (id_tarefa, id_usuario) VALUES (2,2);


