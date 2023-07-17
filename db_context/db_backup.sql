CREATE SCHEMA calendario;

USE calendario;

CREATE TABLE IF NOT EXISTS importancias (
	id_importancia TINYINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    nombre VARCHAR(30) NOT NULL,
    CONSTRAINT pk_importancia PRIMARY KEY (id_importancia)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS eventos (
	id_evento INT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    titulo VARCHAR(50) NOT NULL,
    fecha_hora DATETIME NOT NULL,
    descripcion VARCHAR(200),
    duracion SMALLINT NOT NULL,
    recordatorio DATETIME,
    id_importancia TINYINT UNSIGNED,
    CONSTRAINT pk_eventos PRIMARY KEY (id_evento),
    CONSTRAINT fk_importancia FOREIGN KEY (id_importancia)
    REFERENCES importancias (id_importancia) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS etiquetas (
	id_etiqueta TINYINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    nombre VARCHAR(45) NOT NULL,
    CONSTRAINT pk_etiquetas PRIMARY KEY (id_etiqueta)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS eventos_etiquetas (
	id_evento_etiqueta TINYINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
    id_evento INT UNSIGNED,
    id_etiqueta TINYINT UNSIGNED,
    CONSTRAINT pk_eventos_etiquetas PRIMARY KEY (id_evento_etiqueta),
    CONSTRAINT fk_eventos FOREIGN KEY (id_evento)
    REFERENCES eventos (id_evento) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_etiquetas FOREIGN KEY (id_etiqueta)
    REFERENCES etiquetas (id_etiqueta) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;
