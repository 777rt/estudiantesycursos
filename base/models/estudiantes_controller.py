from flask import Blueprint, render_template, request, redirect, url_for, flash
from base.models.estudiantes import Estudiante
from base.models.curso import Curso #Necesitamos el modelo para el Dropdown

estudiantes_bp = Blueprint('estudiantes',__name__)

#Ruta para mostrar el formulario de un nuevo estudiante 
@estudiantes_bp.route('/estudiante/new')
def new_estudiante():
    cursos = Curso.get_all()#Obtener todos los cursos para el dropdown
    return render_template('nuevo_estudiante.html', cursos=cursos)

#Ruta para procesar la creacion de un nuevo estudiante
@estudiantes_bp.route('/estudiantes/create', methods=['POST'])
def create_estudiante():
    #El ID del estudiante es 0 para la validacion inicial del mail unico
    form_data = request.form.to_dict()
    form_data['id'] = '0' #Temporal para la validacion de email unico
    # Validar los datos del formulario
    if not Estudiante.validate_estudiante(form_data):   
        return redirect(url_for('estudiantes.new_estudiante'))
    
    # Crear el estudiante
    estudiante_id = Estudiante.save(form_data)
    if estudiante_id:
        flash("Estudiante creado exitosamente", "success")
        return redirect(url_for('estudiantes.index'))
    else:
        flash("Error al crear el estudiante", "error")
        return redirect(url_for('estudiantes.new_estudiante'))

#Ruta para mostrar todos los estudiantes
@estudiantes_bp.route('/estudiantes')
def index():
    estudiantes = Estudiante.get_all()
    return render_template('estudiantes/index.html', estudiantes=estudiantes)

#Ruta para mostrar un estudiante específico
@estudiantes_bp.route('/estudiantes/<int:estudiante_id>')
def show(estudiante_id):
    estudiante = Estudiante.get_one(estudiante_id)
    if not estudiante:
        flash("Estudiante no encontrado", "error")
        return redirect(url_for('estudiantes.index'))
    return render_template('estudiantes/show.html', estudiante=estudiante)

#Ruta para mostrar el formulario de edición
@estudiantes_bp.route('/estudiantes/<int:estudiante_id>/edit')
def edit(estudiante_id):
    estudiante = Estudiante.get_one(estudiante_id)
    cursos = Curso.get_all()
    if not estudiante:
        flash("Estudiante no encontrado", "error")
        return redirect(url_for('estudiantes.index'))
    return render_template('estudiantes/edit.html', estudiante=estudiante, cursos=cursos)

#Ruta para procesar la actualización
@estudiantes_bp.route('/estudiantes/<int:estudiante_id>/update', methods=['POST'])
def update(estudiante_id):
    form_data = request.form.to_dict()
    form_data['id'] = estudiante_id
    
    # Validar los datos del formulario
    if not Estudiante.validate_estudiante(form_data):
        return redirect(url_for('estudiantes.edit', estudiante_id=estudiante_id))
    
    # Actualizar el estudiante
    if Estudiante.update(form_data):
        flash("Estudiante actualizado exitosamente", "success")
        return redirect(url_for('estudiantes.show', estudiante_id=estudiante_id))
    else:
        flash("Error al actualizar el estudiante", "error")
        return redirect(url_for('estudiantes.edit', estudiante_id=estudiante_id))

#Ruta para eliminar un estudiante
@estudiantes_bp.route('/estudiantes/<int:estudiante_id>/delete', methods=['POST'])
def delete(estudiante_id):
    if Estudiante.delete(estudiante_id):
        flash("Estudiante eliminado exitosamente", "success")
    else:
        flash("Error al eliminar el estudiante", "error")
    return redirect(url_for('estudiantes.index'))
    