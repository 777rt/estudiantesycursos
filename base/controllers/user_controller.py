from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from base.models.user import User
from base import bcrypt

user_bp = Blueprint('users', __name__)

# Ruta para mostrar todos los usuarios
@user_bp.route('/users')
def index():
    users = User.get_all()
    return render_template('users/index.html', users=users)

# Ruta para mostrar el formulario de nuevo usuario
@user_bp.route('/users/new')
def new():
    return render_template('users/new.html')

# Ruta para procesar la creación de un nuevo usuario
@user_bp.route('/users/create', methods=['POST'])
def create():
    form_data = request.form.to_dict()
    
    # Validar los datos del formulario
    if not User.validate_user(form_data):
        return redirect(url_for('users.new'))
    
    # Encriptar la contraseña
    form_data['password'] = bcrypt.generate_password_hash(form_data['password'])
    
    # Crear el usuario
    user_id = User.create(form_data)
    if user_id:
        flash("Usuario creado exitosamente", "success")
        return redirect(url_for('users.index'))
    else:
        flash("Error al crear el usuario", "error")
        return redirect(url_for('users.new'))

# Ruta para mostrar un usuario específico
@user_bp.route('/users/<int:user_id>')
def show(user_id):
    user = User.get_one(user_id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('users.index'))
    return render_template('users/show.html', user=user)

# Ruta para mostrar el formulario de edición
@user_bp.route('/users/<int:user_id>/edit')
def edit(user_id):
    user = User.get_one(user_id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('users.index'))
    return render_template('users/edit.html', user=user)

# Ruta para procesar la actualización
@user_bp.route('/users/<int:user_id>/update', methods=['POST'])
def update(user_id):
    form_data = request.form.to_dict()
    form_data['id'] = user_id
    
    # Validar los datos del formulario
    if not User.validate_user(form_data):
        return redirect(url_for('users.edit', user_id=user_id))
    
    # Actualizar el usuario
    if User.update(form_data):
        flash("Usuario actualizado exitosamente", "success")
        return redirect(url_for('users.show', user_id=user_id))
    else:
        flash("Error al actualizar el usuario", "error")
        return redirect(url_for('users.edit', user_id=user_id))

# Ruta para eliminar un usuario
@user_bp.route('/users/<int:user_id>/delete', methods=['POST'])
def delete(user_id):
    if User.delete(user_id):
        flash("Usuario eliminado exitosamente", "success")
    else:
        flash("Error al eliminar el usuario", "error")
    return redirect(url_for('users.index'))

# Ruta para mostrar el formulario de login
@user_bp.route('/login')
def login_form():
    return render_template('users/login.html')

# Ruta para procesar el login
@user_bp.route('/login', methods=['POST'])
def login():
    form_data = request.form.to_dict()
    user = User.get_by_email(form_data['email'])
    
    if user and bcrypt.check_password_hash(user.password, form_data['password']):
        session['user_id'] = user.id
        session['user_name'] = user.name
        flash(f"Bienvenido, {user.name}!", "success")
        return redirect(url_for('users.dashboard'))
    else:
        flash("Email o contraseña incorrectos", "error")
        return redirect(url_for('users.login_form'))

# Ruta para el dashboard
@user_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder al dashboard", "error")
        return redirect(url_for('users.login_form'))
    
    user = User.get_one(session['user_id'])
    return render_template('users/dashboard.html', user=user)

# Ruta para cerrar sesión
@user_bp.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión exitosamente", "success")
    return redirect(url_for('users.login_form'))
