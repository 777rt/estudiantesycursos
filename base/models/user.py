from base.config.mysqlconnection import connectToMySQL

class User:
    DB = 'esquema'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create(cls, data):
        query = """ 
                 INSERT INTO usuarios (nombre, email, password)
                VALUES (%(name)s, %(email)s, %(password)s);
                 """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        if results:
            for user_data in results:  # type: ignore
                users.append(cls(user_data))
        return users
    
    @classmethod
    def get_one(cls, user_id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        data = {'id': user_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return cls(result[0])  # type: ignore
        return None
    
    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        data = {'email': email}
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return cls(result[0])  # type: ignore
        return None
    
    @classmethod
    def update(cls, data):
        query = "UPDATE usuarios SET nombre=%(name)s, email=%(email)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete(cls, user_id):
        query = "DELETE FROM usuarios WHERE id=%(id)s;"
        data = {'id': user_id}
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @staticmethod
    def validate_user(user):
        from flask import flash
        is_valid = True
        
        if len(user['name']) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "user_error")
            is_valid = False
            
        if len(user['email']) < 5:
            flash("El email debe tener al menos 5 caracteres.", "user_error")
            is_valid = False
            
        import re
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(user['email']):
            flash("Email inválido.", "user_error")
            is_valid = False
            
        # Verificar si el email ya existe
        existing_user = User.get_by_email(user['email'])
        if existing_user and existing_user.id != int(user.get('id', 0)):
            flash("El email ya está registrado.", "user_error")
            is_valid = False
            
        return is_valid
    