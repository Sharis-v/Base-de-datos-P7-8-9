-- 1. Limpieza total con CASCADE para evitar errores de dependencia
DROP TABLE IF EXISTS PARTICIPACION, PROYECTO, INSCRIPCION, SECCION, ESTUDIANTE, CURSO, PROFESOR, DEPARTAMENTO CASCADE;

-- 2. Creación de Tablas (Asegurando columnas para tus 20 consultas)
CREATE TABLE DEPARTAMENTO (
    id_depto SERIAL PRIMARY KEY, 
    nombre VARCHAR(100), 
    edificio VARCHAR(50), 
    presupuesto INT
);

CREATE TABLE PROFESOR (
    id_prof SERIAL PRIMARY KEY, 
    nombre VARCHAR(100), 
    id_depto INT REFERENCES DEPARTAMENTO(id_depto)
);

CREATE TABLE CURSO (
    id_curso SERIAL PRIMARY KEY, 
    titulo VARCHAR(100), 
    creditos INT, 
    id_depto INT REFERENCES DEPARTAMENTO(id_depto)
);

CREATE TABLE ESTUDIANTE (
    id_est SERIAL PRIMARY KEY, 
    nombre VARCHAR(100), 
    carrera VARCHAR(50), 
    promedio FLOAT, 
    id_depto INT REFERENCES DEPARTAMENTO(id_depto)
);

CREATE TABLE SECCION (
    id_sec SERIAL PRIMARY KEY, 
    id_curso INT REFERENCES CURSO(id_curso), 
    id_prof INT REFERENCES PROFESOR(id_prof), 
    anio INT
);

CREATE TABLE INSCRIPCION (
    id_est INT REFERENCES ESTUDIANTE(id_est), 
    id_sec INT REFERENCES SECCION(id_sec), 
    nota FLOAT, 
    PRIMARY KEY(id_est, id_sec)
);

CREATE TABLE PROYECTO (
    id_proy SERIAL PRIMARY KEY, 
    nombre_p VARCHAR(100), 
    id_lider INT REFERENCES PROFESOR(id_prof),
    presupuesto INT -- Agregado para consulta 19 (Theta Join)
);

CREATE TABLE PARTICIPACION (
    id_est INT REFERENCES ESTUDIANTE(id_est), 
    id_proy INT REFERENCES PROYECTO(id_proy), 
    horas INT, 
    PRIMARY KEY(id_est, id_proy)
);

-- 3. Inserción de Departamentos (10 registros)
INSERT INTO DEPARTAMENTO (nombre, edificio, presupuesto) VALUES 
('Sistemas y Computación', 'Edificio A', 500000), ('Ingeniería Industrial', 'Edificio B', 450000),
('Ciencias Económicas', 'Edificio C', 300000), ('Ingeniería Mecánica', 'Edificio D', 400000),
('Ciencias Básicas', 'Edificio E', 250000), ('Ingeniería Eléctrica', 'Edificio F', 350000),
('Gestión Empresarial', 'Edificio G', 280000), ('Arquitectura', 'Edificio H', 420000),
('Idiomas', 'Edificio I', 150000), ('Posgrado', 'Edificio J', 600000);

-- 4. Inserción de Profesores (20 registros reales)
INSERT INTO PROFESOR (nombre, id_depto)
SELECT 
    (ARRAY['Dr. Alejandro', 'Dra. Beatriz', 'Mtro. Carlos', 'Dra. Dolores', 'Ing. Eduardo', 'Dra. Fernanda', 'Mtro. Gerardo', 'Dra. Hilda', 'Ing. Iván', 'Mtra. Josefina'])[floor(random() * 10) + 1] || ' ' ||
    (ARRAY['Hernández', 'García', 'Martínez', 'López', 'González', 'Rodríguez', 'Pérez', 'Sánchez', 'Ramírez', 'Cruz'])[floor(random() * 10) + 1],
    (gs % 10) + 1
FROM generate_series(1, 20) gs;

-- 5. Inserción de Cursos (20 registros)
INSERT INTO CURSO (titulo, creditos, id_depto)
SELECT 
    (ARRAY['Bases de Datos', 'Programación Web', 'Cálculo Diferencial', 'Álgebra Lineal', 'Termodinámica', 'Ética Profesional', 'Redes de Computadoras', 'Inteligencia Artificial', 'Física Moderna', 'Estructura de Datos'])[floor(random() * 10) + 1] || ' ' || gs,
    (gs % 5) + 2,
    (gs % 10) + 1
FROM generate_series(1, 20) gs;

-- 6. INSERCIÓN MASIVA DE ESTUDIANTES (+110 con nombres mexicanos)
INSERT INTO ESTUDIANTE (nombre, carrera, promedio, id_depto)
SELECT 
    (ARRAY['Juan', 'María', 'José', 'Guadalupe', 'Francisco', 'Juana', 'Antonio', 'Verónica', 'Pedro', 'Rosa', 'Miguel', 'Leticia', 'Raúl', 'Elena', 'Jorge', 'Silvia', 'Diego', 'Adriana', 'Luis', 'Gabriela'])[floor(random() * 20) + 1] || ' ' ||
    (ARRAY['Hernández', 'García', 'Martínez', 'López', 'González', 'Rodríguez', 'Pérez', 'Sánchez', 'Ramírez', 'Cruz', 'Flores', 'Gómez', 'Morales', 'Vázquez', 'Jiménez', 'Reyes', 'Díaz', 'Torres', 'Gutiérrez', 'Ruiz'])[floor(random() * 20) + 1] || ' ' ||
    (ARRAY['Sosa', 'Mendoza', 'Tapia', 'Luna', 'Mejía', 'Zúñiga', 'Villarreal', 'Castañeda', 'Valdez', 'Peralta'])[floor(random() * 10) + 1],
    CASE WHEN gs % 3 = 0 THEN 'Sistemas' WHEN gs % 3 = 1 THEN 'Industrial' ELSE 'Mecatrónica' END,
    (7.0 + random() * 3.0),
    (floor(random() * 10) + 1)
FROM generate_series(1, 115) gs;

-- 7. Secciones, Inscripciones y Proyectos (+100 tuplas lógicas)
INSERT INTO SECCION (id_curso, id_prof, anio)
SELECT (gs % 20) + 1, (gs % 20) + 1, 2025 FROM generate_series(1, 30) gs;

INSERT INTO INSCRIPCION (id_est, id_sec, nota) 
SELECT (floor(random() * 110) + 1), (floor(random() * 30) + 1), (6.0 + random() * 4.0)
FROM generate_series(1, 200) gs ON CONFLICT DO NOTHING;

INSERT INTO PROYECTO (nombre_p, id_lider, presupuesto) 
SELECT 'Proyecto de Investigación ' || gs, (gs % 20) + 1, (50000 + (gs * 10000)) FROM generate_series(1, 15) gs;

INSERT INTO PARTICIPACION (id_est, id_proy, horas) 
SELECT (floor(random() * 110) + 1), (floor(random() * 15) + 1), (10 + floor(random() * 40)) 
FROM generate_series(1, 80) gs ON CONFLICT DO NOTHING;