-- Crear la base de datos principal para estudiantes y cursos
CREATE DATABASE IF NOT EXISTS esquema_estudiantes_cursos;
USE esquema_estudiantes_cursos;

-- =====================================================
-- TABLA: cursos
-- =====================================================
CREATE TABLE IF NOT EXISTS cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA: estudiantes
-- =====================================================
CREATE TABLE IF NOT EXISTS estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    curso_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
);

-- =====================================================
-- CREAR ÍNDICES PARA OPTIMIZAR CONSULTAS
-- =====================================================
CREATE INDEX idx_estudiantes_curso_id ON estudiantes(curso_id);
CREATE INDEX idx_estudiantes_email ON estudiantes(email);
CREATE INDEX idx_cursos_nombre ON cursos(nombre);


-- =====================================================
-- VERIFICACIÓN DE LA CONFIGURACIÓN
-- =====================================================

-- Mostrar las tablas creadas
SHOW TABLES;

-- Verificar la estructura de las tablas
DESCRIBE cursos;
DESCRIBE estudiantes;

-- Mostrar datos de ejemplo insertados
SELECT 'CURSOS CREADOS:' as Info;
SELECT id, nombre, descripcion FROM cursos;

SELECT 'ESTUDIANTES CREADOS:' as Info;
SELECT e.id, e.nombre, e.apellido, e.email, c.nombre as curso 
FROM estudiantes e 
JOIN cursos c ON e.curso_id = c.id;
