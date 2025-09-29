-- Script SQL para crear la base de datos y tablas necesarias
-- Ejecutar este script en MySQL antes de usar la aplicación

-- Crear la base de datos principal para usuarios
CREATE DATABASE IF NOT EXISTS esquema;
USE esquema;

-- Crear la tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Crear la base de datos para estudiantes y cursos
CREATE DATABASE IF NOT EXISTS esquema_estudiantes_cursos;
USE esquema_estudiantes_cursos;

-- Crear la tabla de cursos
CREATE TABLE IF NOT EXISTS cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Crear la tabla de estudiantes
CREATE TABLE IF NOT EXISTS estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    curso_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE SET NULL
);

-- Insertar algunos usuarios de ejemplo (opcional)
USE esquema;
INSERT INTO usuarios (nombre, email, password) VALUES 
('Juan Pérez', 'juan@ejemplo.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8Qz8K8K2'), -- password: 123456
('María García', 'maria@ejemplo.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8Qz8K8K2'), -- password: 123456
('Carlos López', 'carlos@ejemplo.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8Qz8K8K2'); -- password: 123456

-- Insertar algunos cursos de ejemplo
USE esquema_estudiantes_cursos;
INSERT INTO cursos (nombre, descripcion) VALUES 
('Programación Web', 'Curso completo de desarrollo web con HTML, CSS, JavaScript y frameworks modernos'),
('Base de Datos', 'Aprendizaje de diseño y administración de bases de datos relacionales'),
('Python Avanzado', 'Programación avanzada en Python con frameworks como Django y Flask'),
('Desarrollo Móvil', 'Creación de aplicaciones móviles para iOS y Android');

-- Insertar algunos estudiantes de ejemplo
INSERT INTO estudiantes (nombre, apellido, email, curso_id) VALUES 
('Ana', 'Martínez', 'ana.martinez@ejemplo.com', 1),
('Luis', 'Rodríguez', 'luis.rodriguez@ejemplo.com', 1),
('Carmen', 'González', 'carmen.gonzalez@ejemplo.com', 2),
('Pedro', 'Sánchez', 'pedro.sanchez@ejemplo.com', 3),
('Laura', 'Fernández', 'laura.fernandez@ejemplo.com', 4);

-- Mostrar la estructura de las tablas
USE esquema;
DESCRIBE usuarios;

USE esquema_estudiantes_cursos;
DESCRIBE cursos;
DESCRIBE estudiantes;

-- Mostrar los datos insertados
USE esquema;
SELECT * FROM usuarios;

USE esquema_estudiantes_cursos;
SELECT * FROM cursos;
SELECT * FROM estudiantes;
