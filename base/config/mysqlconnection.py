import os
from dotenv import load_dotenv
# Importamos la librería pymysql para interactuar con MySQL
import pymysql.cursors

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-muy-segura-aqui'

# Esta clase proporciona una instancia para conectarse a la base de datos MySQL
class MySQLConnection:
    # Método constructor que recibe el nombre de la base de datos como parámetro
    def __init__(self, db):
        # Configuración de la conexión, se pueden ajustar el usuario, la contraseña y otros parámetros según sea necesario
        connection = pymysql.connect(
            host='localhost',
            port=3306,  # Puerto de la base de datos
            user='root',       # Nombre de usuario de la base de datos
            password='root',  # Contraseña del usuario de la base de datos
            db='esquema_estudiantes_cursos',             # Nombre de la base de datos
            charset='utf8mb4',  # Codificación de caracteres
            # Los resultados se devuelven como diccionarios
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True)   # Realiza automáticamente un commit después de cada consulta
        # Se almacena la conexión establecida en un atributo de la clase
        self.connection = connection

    # Método para ejecutar consultas SQL en la base de datos
    # Recibe una consulta SQL (query) y opcionalmente datos (data) para consultas parametrizadas
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                # Si deseas depurar, imprime la consulta generada con mogrify
                if data:
                    print("Running Query:", cursor.mogrify(query, data))
                # Ejecutamos la consulta directamente
                cursor.execute(query, data)
                # Si la consulta es un INSERT, se devuelve el ID de la última fila insertada
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                # Si es una consulta SELECT, devolvemos el resultado como una lista de diccionarios
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                # Para consultas UPDATE o DELETE, confirmamos la transacción
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong", e)
                return False
            finally:
                # No cierres la conexión aquí, solo asegúrate de que el cursor se libere correctamente.
                pass

def connectToMySQL(db):
    return MySQLConnection(db)

# Clase Database para mantener compatibilidad con el resto de la aplicación
class Database:
    @staticmethod
    def get_connection():
        """Obtener conexión usando la nueva clase MySQLConnection"""
        mysql_connection = connectToMySQL('esquema_estudiantes_cursos')
        return mysql_connection.connection

    @staticmethod
    def init_database():
        """Inicializar la base de datos y crear tablas"""
        try:
            mysql_conn = connectToMySQL('esquema_estudiantes_cursos')
            # Crear tabla de cursos
            create_cursos_table = '''
            CREATE TABLE IF NOT EXISTS cursos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                descripcion TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )'''
            mysql_conn.query_db(create_cursos_table)
            
            # Crear tabla de estudiantes
            create_estudiantes_table = '''
            CREATE TABLE IF NOT EXISTS estudiantes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                curso_id INT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
            )'''
            mysql_conn.query_db(create_estudiantes_table)

            # Crear índices para mejorar rendimiento
            try:
                mysql_conn.query_db('CREATE INDEX idx_estudiantes_curso_id ON estudiantes(curso_id)')
            except:
                pass  # El índice ya existe
            try:
                mysql_conn.query_db('CREATE INDEX idx_estudiantes_email ON estudiantes(email)')
            except:
                pass  # El índice ya existe
            try:
                mysql_conn.query_db('CREATE INDEX idx_cursos_nombre ON cursos(nombre)')
            except:
                pass  # El índice ya existe

            print("✅ Base de datos inicializada correctamente")
        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
            raise

    @staticmethod
    def execute_query(query, params=None, fetch=False):
        """Ejecutar consulta SQL usando la nueva clase MySQLConnection"""
        try:
            mysql_conn = connectToMySQL('esquema_estudiantes_cursos')
            result = mysql_conn.query_db(query, params)
            if fetch:
                return result if result else []
            else:
                return result
        except Exception as e:
            print(f"❌ Error ejecutando consulta: {e}")
            raise

    @staticmethod
    def test_connection():
        """Probar la conexión a la base de datos"""
        try:
            mysql_conn = connectToMySQL('esquema_estudiantes_cursos')
            result = mysql_conn.query_db("SELECT 1")
            return True
        except Exception as e:
            print(f"❌ Error probando conexión: {e}")
            return False