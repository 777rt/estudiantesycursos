import os
from flask import Flask
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def create_app():
    # Determinar rutas del proyecto para templates y static (carpeta raíz del proyecto)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    templates_path = os.path.join(project_root, 'templates')
    static_path = os.path.join(project_root, 'static')

    app = Flask(__name__, template_folder=templates_path, static_folder=static_path, static_url_path='/static')
    app.config['SECRET_KEY'] = 'dev_secret_key'

    # Inicializar extensiones
    bcrypt.init_app(app)

    # Registrar blueprints si existen (cursos, estudiantes)
    try:
        from base.models.cursos_controller import cursos_bp
        app.register_blueprint(cursos_bp)
    except Exception:
        pass

    try:
        from base.models.estudiantes_controller import estudiantes_bp
        app.register_blueprint(estudiantes_bp)
    except Exception:
        pass

    # Ruta raíz: redirige a /cursos si existe esa área
    @app.route('/')
    def index_root():
        from flask import redirect, url_for
        return redirect(url_for('cursos.index'))
    return app
