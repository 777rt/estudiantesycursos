#config/mysql

import pymysql.cursors  # type: ignore 

class MySQLConnection:
    def __init__(self, db):
        try: 
            conecction = pymysql.connect(
                host='localhost',
                port=3306,
                user = 'root',
                password = 'root',
                db = db,
                charset = 'utf8mb4',
                cursorclass = pymysql.cursors.DictCursor,
                autocommit = True
                )
            self.connection = conecction
        except pymysql.MySQLError as e:
            print(f"Error al conectar la base de datos: {e}")
            self.connection = None

    def query_db(self, query, data=None):
        if not self.connection:
            print("No hay conexión a la base de datos.")
            return False
        
        with self.connection.cursor() as cursor:
            try:
                if data:
                    print("Running Query:", cursor.mogrify(query, data))
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit() # commit para update / delete
                    return True # para update / delete
            except Exception as e:
                print(f"Hubo un problema en la consulta: {e}")
                return False    
            finally:
                pass # no cerramos la conexión aquí
def connectToMySQL(db):
    return MySQLConnection(db)