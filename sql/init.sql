-- Crear tablas auxiliares

CREATE TABLE rol_usuario (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE ciudad (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    departamento TEXT NOT NULL
);

CREATE TABLE lugar (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    direccion TEXT NOT NULL,
    id_ciudad INT REFERENCES ciudad(id),
    capacidad INT CHECK (capacidad > 0)
);

CREATE TABLE categoria_evento (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE tipo_evento (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE tema_evento (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE tipo_entrada (
    id SERIAL PRIMARY KEY,
    descripcion TEXT NOT NULL,
    precio_base NUMERIC(10, 2) NOT NULL
);

CREATE TABLE medio_pago (
    id SERIAL PRIMARY KEY,
    metodo TEXT NOT NULL
);

-- Entidades principales

CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    id_rol INT REFERENCES rol_usuario(id)
);

CREATE TABLE asistente (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT UNIQUE NOT NULL,
    fecha_nacimiento DATE NOT NULL
);

CREATE TABLE evento (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    descripcion TEXT,
    id_lugar INT REFERENCES lugar(id),
    id_categoria_evento INT REFERENCES categoria_evento(id),
    id_tipo_evento INT REFERENCES tipo_evento(id),
    id_tema_evento INT REFERENCES tema_evento(id),
    id_usuario INT REFERENCES usuario(id)
);

CREATE TABLE entrada (
    id SERIAL PRIMARY KEY,
    id_evento INT REFERENCES evento(id),
    id_asistente INT REFERENCES asistente(id),
    id_tipo_entrada INT REFERENCES tipo_entrada(id),
    id_medio_pago INT REFERENCES medio_pago(id),
    fecha_compra DATE NOT NULL,
    precio_final NUMERIC(10, 2) NOT NULL
);

CREATE TABLE registro_asistencia (
    id SERIAL PRIMARY KEY,
    id_evento INT REFERENCES evento(id),
    id_asistente INT REFERENCES asistente(id),
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relaciones N:M

CREATE TABLE artista (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL
);

CREATE TABLE evento_artista (
    id_evento INT REFERENCES evento(id),
    id_artista INT REFERENCES artista(id),
    PRIMARY KEY (id_evento, id_artista)
);

CREATE TABLE patrocinador (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    tipo TEXT
);

CREATE TABLE evento_patrocinador (
    id_evento INT REFERENCES evento(id),
    id_patrocinador INT REFERENCES patrocinador(id),
    PRIMARY KEY (id_evento, id_patrocinador)
);

CREATE TABLE recurso (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL
);

CREATE TABLE evento_recurso (
    id_evento INT REFERENCES evento(id),
    id_recurso INT REFERENCES recurso(id),
    cantidad INT CHECK (cantidad >= 0),
    PRIMARY KEY (id_evento, id_recurso)
);

-- Calificación del evento

CREATE TABLE calificacion_evento (
    id_evento INT REFERENCES evento(id),
    id_asistente INT REFERENCES asistente(id),
    calificacion INT CHECK (calificacion >= 1 AND calificacion <= 5),
    comentario TEXT,
    PRIMARY KEY (id_evento, id_asistente)
);

-- Inserciones mínimas de prueba

INSERT INTO rol_usuario (nombre) VALUES ('Organizador'), ('Administrador');
INSERT INTO ciudad (nombre, departamento) VALUES ('Ciudad de Guatemala', 'Guatemala');
INSERT INTO lugar (nombre, direccion, id_ciudad, capacidad) VALUES ('Teatro Nacional', '6a Avenida, zona 1', 1, 1200);
INSERT INTO categoria_evento (nombre) VALUES ('Música'), ('Danza');
INSERT INTO tipo_evento (nombre) VALUES ('Concierto'), ('Festival');
INSERT INTO tema_evento (nombre) VALUES ('Tradición'), ('Juventud');
INSERT INTO tipo_entrada (descripcion, precio_base) VALUES ('General', 100.00), ('VIP', 250.00);
INSERT INTO medio_pago (metodo) VALUES ('Efectivo'), ('Tarjeta');

INSERT INTO usuario (nombre, email, id_rol) VALUES ('María López', 'maria@uvg.edu.gt', 1);
INSERT INTO asistente (nombre, correo, fecha_nacimiento) VALUES ('Carlos Díaz', 'carlos@example.com', '2001-05-10');
INSERT INTO artista (nombre, tipo) VALUES ('Grupo Folklórico', 'Baile');
INSERT INTO patrocinador (nombre, tipo) VALUES ('Cerveza Gallo', 'Privado');
INSERT INTO recurso (nombre, tipo) VALUES ('Proyector', 'Tecnología');
