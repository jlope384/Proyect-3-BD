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

-- INSERCIÓN DE DATOS

-- Roles de Usuario
INSERT INTO rol_usuario (nombre) VALUES 
('Organizador'), ('Administrador'), ('Staff'), ('Invitado'), ('Proveedor');

-- Ciudades
INSERT INTO ciudad (nombre, departamento) VALUES 
('Ciudad de Guatemala', 'Guatemala'),
('Quetzaltenango', 'Quetzaltenango'),
('Antigua Guatemala', 'Sacatepéquez'),
('Escuintla', 'Escuintla'),
('Chimaltenango', 'Chimaltenango'),
('Huehuetenango', 'Huehuetenango'),
('Cobán', 'Alta Verapaz'),
('Puerto Barrios', 'Izabal'),
('Retalhuleu', 'Retalhuleu'),
('Mazatenango', 'Suchitepéquez'),
('Jalapa', 'Jalapa'),
('Zacapa', 'Zacapa'),
('Flores', 'Petén'),
('Sololá', 'Sololá'),
('Totonicapán', 'Totonicapán');

-- Lugares
INSERT INTO lugar (nombre, direccion, id_ciudad, capacidad) VALUES 
('Teatro Nacional', '6a Avenida, zona 1', 1, 1200),
('Centro Cultural Miguel Ángel Asturias', '24 calle 3-81, zona 1', 1, 2500),
('Teatro Lux', '6a avenida 11-02, zona 1', 2, 800),
('Centro Cultural de Antigua', '5a calle oriente #5', 3, 500),
('Convention Center', '15 avenida 1-50, zona 13', 1, 5000),
('Estadio Doroteo Guamuch Flores', '10a avenida, zona 5', 1, 26500),
('Teatro Municipal', '12 avenida 0-60, zona 1', 2, 600),
('Auditorio Juan Bautista Gutiérrez', 'Universidad Francisco Marroquín', 1, 1200),
('Teatro Abril', '7a avenida 12-36, zona 9', 1, 1500),
('Centro Cultural España', '6a calle 11-02, zona 1', 1, 300),
('Teatro de Cámara', 'Calle Santander, Antigua', 3, 200),
('Teatro Roma', 'Avenida Las Américas, zona 13', 1, 1000),
('Centro Cultural Universitario', 'Universidad de San Carlos', 1, 800),
('Teatro del IGA', 'Avenida La Reforma 13-70, zona 9', 1, 700),
('Teatro de la Universidad del Valle', '18 avenida 11-95, zona 15', 1, 900);

-- Categorías de Evento
INSERT INTO categoria_evento (nombre) VALUES 
('Música'), ('Danza'), ('Teatro'), ('Artes Visuales'), ('Literatura'),
('Cine'), ('Conferencia'), ('Taller'), ('Festival'), ('Deporte'),
('Gastronomía'), ('Moda'), ('Tecnología'), ('Negocios'), ('Religioso');

-- Tipos de Evento
INSERT INTO tipo_evento (nombre) VALUES 
('Concierto'), ('Festival'), ('Exposición'), ('Obra de Teatro'), ('Conferencia'),
('Taller'), ('Seminario'), ('Competencia'), ('Feria'), ('Espectáculo'),
('Gala'), ('Premiación'), ('Maratón'), ('Charla'), ('Networking');

-- Temas de Evento
INSERT INTO tema_evento (nombre) VALUES 
('Tradición'), ('Juventud'), ('Innovación'), ('Cultura'), ('Educación'),
('Sostenibilidad'), ('Salud'), ('Diversidad'), ('Historia'), ('Futuro'),
('Comunidad'), ('Arte Contemporáneo'), ('Tecnología'), ('Empoderamiento'), ('Solidaridad');

-- Tipos de Entrada
INSERT INTO tipo_entrada (descripcion, precio_base) VALUES 
('General', 100.00), ('VIP', 250.00), ('Estudiante', 50.00), ('Niños', 30.00),
('Adulto Mayor', 40.00), ('Early Bird', 80.00), ('Platinum', 500.00), ('Gold', 350.00),
('Silver', 200.00), ('Patrocinador', 0.00), ('Prensa', 0.00), ('Invitación', 0.00),
('Grupo (5+ personas)', 75.00), ('Día 1', 120.00), ('Día 2', 120.00), ('Pase Completo', 200.00);

-- Medios de Pago
INSERT INTO medio_pago (metodo) VALUES 
('Efectivo'), ('Tarjeta de Crédito'), ('Tarjeta de Débito'), ('Transferencia Bancaria'),
('PayPal'), ('Bitcoin'), ('Cheque'), ('Pago Móvil'), ('Depósito Bancario'), 
('Pago en Cuotas'), ('Puntos de Recompensa'), ('Vale Corporativo');

-- Usuarios
INSERT INTO usuario (nombre, email, id_rol) VALUES 
('María López', 'maria@uvg.edu.gt', 1),
('Juan Pérez', 'juan@organizador.com', 1),
('Ana Martínez', 'ana.martinez@eventosgt.com', 2),
('Carlos Ramírez', 'carlos@admin.com', 2),
('Luisa García', 'luisa@staff.com', 3),
('Pedro Hernández', 'pedro@staff.com', 3),
('Sofía Morales', 'sofia@invitado.com', 4),
('Miguel Torres', 'miguel@proveedor.com', 5),
('Elena Castro', 'elena@organizador.com', 1),
('Roberto Jiménez', 'roberto@admin.com', 2),
('Carmen Ruíz', 'carmen@staff.com', 3),
('Jorge Mendoza', 'jorge@invitado.com', 4),
('Patricia Núñez', 'patricia@proveedor.com', 5),
('Fernando Gómez', 'fernando@organizador.com', 1),
('Daniela Ortega', 'daniela@admin.com', 2);

-- Asistentes
INSERT INTO asistente (nombre, correo, fecha_nacimiento) VALUES 
('Carlos Díaz', 'carlos@example.com', '2001-05-10'),
('Laura Méndez', 'laura@mail.com', '1995-08-15'),
('Alejandro Ruiz', 'alejandro@correo.com', '1988-11-22'),
('Gabriela Soto', 'gabriela@email.com', '1999-03-30'),
('Ricardo Vargas', 'ricardo@mail.com', '1975-07-18'),
('Silvia Castro', 'silvia@correo.com', '2000-12-05'),
('Oscar Morales', 'oscar@email.com', '1992-09-14'),
('Verónica López', 'veronica@mail.com', '1985-04-25'),
('Francisco Gutiérrez', 'francisco@correo.com', '1998-01-08'),
('Isabel Ramírez', 'isabel@email.com', '1979-06-19'),
('Manuel Herrera', 'manuel@mail.com', '2002-02-28'),
('Adriana Flores', 'adriana@correo.com', '1994-10-11'),
('Eduardo Rivas', 'eduardo@email.com', '1983-07-23'),
('Mariana Torres', 'mariana@mail.com', '1997-05-16'),
('Javier Mérida', 'javier@correo.com', '1990-08-09');

-- Artistas
INSERT INTO artista (nombre, tipo) VALUES 
('Grupo Folklórico', 'Baile'),
('Ricardo Arjona', 'Músico'),
('Malacates Trish Trash', 'Banda'),
('Alux Nahual', 'Banda'),
('Tocados por el Arte', 'Danza Contemporánea'),
('Teatro de los Andes', 'Teatro'),
('Sandra Morán', 'Escritora'),
('Francisco Méndez', 'Pintor'),
('Orquesta Sinfónica Nacional', 'Orquesta'),
('Marimba Chapinlandia', 'Marimba'),
('Los Ángeles', 'Grupo Musical'),
('Huelga de Dolores', 'Performance'),
('Viento en Contra', 'Banda'),
('Plástica Maya', 'Artes Visuales'),
('Titeres del Cadejo', 'Teatro de Títeres');

-- Patrocinadores
INSERT INTO patrocinador (nombre, tipo) VALUES 
('Cerveza Gallo', 'Privado'),
('Banco Industrial', 'Bancario'),
('Tigo', 'Telecomunicaciones'),
('Pollo Campero', 'Alimentos'),
('Cementos Progreso', 'Industrial'),
('Universidad del Valle', 'Educación'),
('Municipalidad de Guatemala', 'Gobierno'),
('Ministerio de Cultura', 'Gobierno'),
('Prensa Libre', 'Medios'),
('Fundación Paiz', 'ONG'),
('Bantrab', 'Bancario'),
('Claro', 'Telecomunicaciones'),
('Cemaco', 'Retail'),
('La Reforma', 'Medios'),
('Fundación G&T', 'ONG');

-- Recursos
INSERT INTO recurso (nombre, tipo) VALUES 
('Proyector', 'Tecnología'),
('Sistema de Sonido', 'Audio'),
('Micrófonos', 'Audio'),
('Luces LED', 'Iluminación'),
('Escenario Modular', 'Estructura'),
('Sillas Plegables', 'Mobiliario'),
('Mesas', 'Mobiliario'),
('Barreras de Seguridad', 'Seguridad'),
('Pantalla Gigante', 'Tecnología'),
('Generador Eléctrico', 'Energía'),
('Carpas', 'Estructura'),
('Catering', 'Alimentos'),
('Vestuario', 'Indumentaria'),
('Maquillaje', 'Indumentaria'),
('Transporte', 'Logística');

-- Eventos
INSERT INTO evento (nombre, fecha, hora, descripcion, id_lugar, id_categoria_evento, id_tipo_evento, id_tema_evento, id_usuario) VALUES 
('Concierto de Rock Nacional', '2023-11-15', '20:00:00', 'Los mejores grupos de rock nacional en un solo lugar', 1, 1, 1, 2, 1),
('Festival de Danza Contemporánea', '2023-10-20', '18:30:00', 'Presentación de compañías nacionales e internacionales', 2, 2, 2, 4, 2),
('Exposición de Arte Maya', '2023-09-05', '09:00:00', 'Exhibición de arte precolombino y contemporáneo inspirado en la cultura maya', 3, 4, 3, 9, 3),
('Conferencia de Tecnología', '2023-12-10', '14:00:00', 'Charlas sobre innovación tecnológica en Guatemala', 4, 13, 5, 3, 4),
('Maratón de la Ciudad', '2023-11-05', '06:00:00', 'Carrera atlética por las calles de la ciudad', 5, 10, 13, 6, 5),
('Feria del Libro', '2023-08-25', '10:00:00', 'Evento literario con presentaciones de libros y autores', 6, 5, 9, 5, 6),
('Gala de Beneficencia', '2023-12-15', '19:00:00', 'Evento para recaudar fondos para niños necesitados', 7, 15, 11, 15, 7),
('Taller de Pintura', '2023-09-30', '15:00:00', 'Taller práctico de técnicas de pintura al óleo', 8, 4, 6, 12, 8),
('Concierto de Marimba', '2023-10-12', '17:00:00', 'Presentación de marimbas tradicionales', 9, 1, 1, 1, 9),
('Festival de Cine', '2023-11-20', '16:00:00', 'Proyección de películas nacionales e internacionales', 10, 6, 2, 7, 10),
('Obra de Teatro: El Principito', '2023-10-05', '20:00:00', 'Adaptación teatral de la famosa novela', 11, 3, 4, 5, 11),
('Conferencia de Sostenibilidad', '2023-09-15', '10:00:00', 'Charlas sobre desarrollo sostenible', 12, 7, 5, 6, 12),
('Competencia de Breakdance', '2023-11-25', '14:00:00', 'Batalla de crews de breakdance nacionales', 13, 2, 8, 2, 13),
('Feria Gastronómica', '2023-10-30', '11:00:00', 'Muestra de cocina tradicional guatemalteca', 14, 11, 9, 1, 14),
('Espectáculo de Circo', '2023-12-20', '19:30:00', 'Show de circo contemporáneo', 15, 10, 10, 4, 15);

-- Evento-Artista
INSERT INTO evento_artista (id_evento, id_artista) VALUES 
(1, 2), (1, 3), (1, 4), (1, 11), (1, 13),
(2, 5), (2, 9), (2, 10),
(3, 8), (3, 14),
(4, 7),
(5, 6), (5, 15),
(6, 7),
(7, 1), (7, 10),
(8, 8),
(9, 10),
(10, 6), (10, 15),
(11, 6),
(12, 7),
(13, 5),
(14, 1), (14, 10),
(15, 5), (15, 6);

-- Evento-Patrocinador
INSERT INTO evento_patrocinador (id_evento, id_patrocinador) VALUES 
(1, 1), (1, 2), (1, 3),
(2, 4), (2, 5), (2, 6),
(3, 7), (3, 8), (3, 9),
(4, 10), (4, 11), (4, 12),
(5, 13), (5, 14), (5, 15),
(6, 1), (6, 2),
(7, 3), (7, 4),
(8, 5), (8, 6),
(9, 7), (9, 8),
(10, 9), (10, 10),
(11, 11), (11, 12),
(12, 13), (12, 14),
(13, 15), (13, 1),
(14, 2), (14, 3),
(15, 4), (15, 5);

-- Evento-Recurso
INSERT INTO evento_recurso (id_evento, id_recurso, cantidad) VALUES 
(1, 1, 2), (1, 2, 1), (1, 3, 6), (1, 4, 10),
(2, 5, 1), (2, 6, 200), (2, 7, 10), (2, 8, 4),
(3, 9, 1), (3, 10, 1), (3, 11, 3),
(4, 1, 1), (4, 2, 1), (4, 3, 2), (4, 6, 100),
(5, 12, 1), (5, 13, 1), (5, 15, 5),
(6, 1, 2), (6, 6, 50), (6, 7, 20),
(7, 4, 15), (7, 5, 1), (7, 6, 150), (7, 12, 1),
(8, 13, 1), (8, 14, 1), (8, 7, 10),
(9, 2, 1), (9, 3, 4), (9, 6, 100),
(10, 1, 3), (10, 2, 1), (10, 9, 1),
(11, 5, 1), (11, 6, 80), (11, 13, 1), (11, 14, 1),
(12, 1, 1), (12, 2, 1), (12, 3, 2), (12, 6, 120),
(13, 4, 8), (13, 5, 1), (13, 8, 4),
(14, 7, 30), (14, 12, 1), (14, 15, 2),
(15, 4, 20), (15, 5, 1), (15, 13, 1), (15, 14, 2);

-- Entradas
INSERT INTO entrada (id_evento, id_asistente, id_tipo_entrada, id_medio_pago, fecha_compra, precio_final) VALUES 
(1, 1, 1, 2, '2023-10-01', 100.00),
(1, 2, 2, 1, '2023-10-02', 250.00),
(1, 3, 3, 3, '2023-10-03', 50.00),
(2, 4, 1, 4, '2023-09-15', 100.00),
(2, 5, 1, 5, '2023-09-16', 100.00),
(3, 6, 4, 6, '2023-08-20', 30.00),
(3, 7, 5, 7, '2023-08-21', 40.00),
(4, 8, 6, 8, '2023-11-01', 80.00),
(4, 9, 1, 9, '2023-11-02', 100.00),
(5, 10, 7, 10, '2023-10-10', 500.00),
(5, 11, 8, 1, '2023-10-11', 350.00),
(6, 12, 9, 2, '2023-07-25', 200.00),
(6, 13, 10, 3, '2023-07-26', 0.00),
(7, 14, 11, 4, '2023-11-20', 0.00),
(7, 15, 12, 5, '2023-11-21', 0.00),
(8, 1, 13, 6, '2023-09-01', 75.00),
(8, 2, 14, 7, '2023-09-02', 120.00),
(9, 3, 15, 8, '2023-09-25', 200.00),
(9, 4, 1, 9, '2023-09-26', 100.00),
(10, 5, 2, 10, '2023-10-15', 250.00);

-- Registro de Asistencia
INSERT INTO registro_asistencia (id_evento, id_asistente, fecha_hora) VALUES 
(1, 1, '2023-11-15 19:45:00'),
(1, 2, '2023-11-15 19:50:00'),
(1, 3, '2023-11-15 19:55:00'),
(2, 4, '2023-10-20 18:20:00'),
(2, 5, '2023-10-20 18:25:00'),
(3, 6, '2023-09-05 09:10:00'),
(3, 7, '2023-09-05 09:15:00'),
(4, 8, '2023-12-10 13:45:00'),
(4, 9, '2023-12-10 13:50:00'),
(5, 10, '2023-11-05 05:30:00'),
(5, 11, '2023-11-05 05:35:00'),
(6, 12, '2023-08-25 09:55:00'),
(6, 13, '2023-08-25 10:00:00'),
(7, 14, '2023-12-15 18:45:00'),
(7, 15, '2023-12-15 18:50:00');

-- Calificación de Eventos
INSERT INTO calificacion_evento (id_evento, id_asistente, calificacion, comentario) VALUES 
(1, 1, 5, 'Excelente concierto, gran energía de los artistas'),
(1, 2, 4, 'Buen evento, pero el sonido podría mejorar'),
(1, 3, 5, 'Increíble experiencia, volvería a ir'),
(2, 4, 3, 'Interesante pero algunas piezas fueron muy largas'),
(2, 5, 4, 'Bailarines muy talentosos'),
(3, 6, 5, 'Arte impresionante, muy bien organizado'),
(3, 7, 4, 'Buena selección de piezas'),
(4, 8, 5, 'Charlas muy informativas e inspiradoras'),
(4, 9, 4, 'Buen contenido, pero poco tiempo para preguntas'),
(5, 10, 5, 'Excelente organización del maratón'),
(5, 11, 3, 'Faltaron más estaciones de agua'),
(6, 12, 4, 'Gran variedad de libros y autores'),
(6, 13, 5, 'Evento cultural muy necesario'),
(7, 14, 5, 'Hermosa gala por una buena causa'),
(7, 15, 4, 'Buena organización y ambiente');
