#Proyecto para usuarios 
#Importaremos el modulo flask
from flask import Flask
from flask_bcrypt import Bcrypt  # type: ignore

#Inicializa Bcrypt (sin pasar la app todavia)
bcrypt = Bcrypt()

def create_app():
    #Creamos la instancia de la app
    app = Flask(__name__)

    #Configuramos la clave secreta directamente para el desarrollo
    app.secret_key = 'TP4medioB'

    #Vincular Bcrypt a la aplicacion
    bcrypt.init_app(app)

    #--Registro de Blueprints--
    #Importamos los blueprints (asegurate que esten bien
    #Definidos en sus respectivos archivos)
    from .controllers import user_controller #El punto indica la importacion relativa
    from .models import estudiantes_controller, cursos_controller

    #Registramos los blueprints
    app.register_blueprint(user_controller.user_bp)
    app.register_blueprint(estudiantes_controller.estudiantes_bp)
    app.register_blueprint(cursos_controller.cursos_bp)

    #Ruta principal que redirige a la pagina de inicio o registro/login
    @app.route('/')
    def index():
        from flask import redirect, session, render_template
        #Importaciones locales para evitar problemas de importacion circular
        if 'user_id' in session: 
            return redirect('/dashboard')
        return render_template('bienvenida.html')
    
    return app