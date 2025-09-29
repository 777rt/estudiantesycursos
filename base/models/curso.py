from base.config.mysqlconnection import connectToMySQL
from flask import flash

# Nombre de tu base de datos (! asegurate de que coincida con la que creaste en MySQL¡)
DB_NAME = 'esquema_estudiantes_cursos'

class Curso:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.estudiantes = [] # Lista para almacenar estudiantes asociados

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cursos ORDER BY nombre ASC;"
        results = connectToMySQL(DB_NAME).query_db(query)
        cursos = []
        if results:
            for curso_data in results:  # type: ignore
                cursos.append(cls(curso_data))
        return cursos
    
    @classmethod
    def get_one(cls, curso_id):
        query = "SELECT * FROM cursos WHERE id = %(id)s;"
        data = {'id': curso_id}
        result = connectToMySQL(DB_NAME).query_db(query, data)
        if result:
            return cls(result[0])  # type: ignore
        return None
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO cursos (nombre, descripcion) VALUES (%(nombre)s, %(descripcion)s);"
        result = connectToMySQL(DB_NAME).query_db(query, data)
        return result
    
    @classmethod
    def update(cls, data):
        query = "UPDATE cursos SET nombre=%(nombre)s, descripcion=%(descripcion)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(DB_NAME).query_db(query, data)
    
    @classmethod
    def delete(cls, curso_id):
        query = "DELETE FROM cursos WHERE id=%(id)s;"
        data = {'id': curso_id}
        return connectToMySQL(DB_NAME).query_db(query, data)
    
    @classmethod
    def get_one_with_estudiantes(cls, curso_id):
        query = """
            SELECT c.*, e.id AS estudiante_id, e.nombre AS estudiante_nombre, e.apellido AS estudiante_apellido, e.email AS estudiante_email
            FROM cursos c
            LEFT JOIN estudiantes e ON c.id = e.curso_id
            WHERE c.id = %(id)s;
                """
        
        data = {'id': curso_id}
        results = connectToMySQL(DB_NAME).query_db(query, data)

        if not results:
            return None
        
        # Crear la instancia del curso una sola vez
        curso = cls(results[0])  # type: ignore # Usamos el primer resultado para crear el curso

        # Agregar estudiantes al curso
        for row in results:  # type: ignore
            if row['estudiante_id']: #Si hay datos de estudiante
                estudiante_data = {
                    'id': row['estudiante_id'],
                    'nombre': row['estudiante_nombre'],
                    'apellido': row['estudiante_apellido'],
                    'email': row['estudiante_email'],
                    'curso_id': row['id'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
                curso.estudiantes.append(estudiante_data)
        
        return curso
    
    @staticmethod
    def validate_curso(curso):
        is_valid = True
        if len(curso['nombre']) < 2:
            flash("El nombre del curso debe tener al menos 2 caracteres.", "curso_error")
            is_valid = False
        if len(curso['descripcion']) < 5:
            flash("La descripción del curso debe tener al menos 5 caracteres.", "curso_error")
            is_valid = False
        return is_valid