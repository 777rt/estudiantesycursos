from flask import Blueprint, render_template, request, redirect, url_for, flash
from base.models.curso import Curso

cursos_bp = Blueprint('cursos', __name__)

#Ruta para mostrar todos los cursos y el formulario de la creacion 
@cursos_bp.route('/cursos')
def index():
    cursos = Curso.get_all()
    return render_template('cursos/index.html', cursos=cursos)

#Ruta para mostrar el formulario de nuevo curso
@cursos_bp.route('/cursos/new')
def new():
    return render_template('cursos/new.html')

#Ruta para procesar la creacion de un nuevo curso
@cursos_bp.route('/cursos/create', methods=['POST'])
def create():
    form_data = request.form.to_dict()
    
    # Validar los datos del formulario
    if not Curso.validate_curso(form_data):
        return redirect(url_for('cursos.new'))
    
    # Crear el curso
    curso_id = Curso.save(form_data)
    if curso_id:
        flash("Curso creado exitosamente", "success")
        return redirect(url_for('cursos.index'))
    else:
        flash("Error al crear el curso", "error")
        return redirect(url_for('cursos.new'))

#Ruta para mostrar un curso especifico y sus estudiantes
@cursos_bp.route('/cursos/<int:curso_id>')
def show(curso_id):
    curso = Curso.get_one_with_estudiantes(curso_id)
    if not curso:
        flash("Curso no encontrado", "error")
        return redirect(url_for('cursos.index'))
    return render_template('cursos/show.html', curso=curso)

#Ruta para mostrar el formulario de edicion de un curso
@cursos_bp.route('/cursos/<int:curso_id>/edit')
def edit(curso_id):
    curso = Curso.get_one(curso_id)
    if not curso:
        flash("Curso no encontrado para editar", "error")
        return redirect(url_for('cursos.index'))
    return render_template('cursos/edit.html', curso=curso)

#Ruta para procesar la actualizacion de un curso
@cursos_bp.route('/cursos/<int:curso_id>/update', methods=['POST'])
def update(curso_id):
    form_data = request.form.to_dict()
    form_data['id'] = curso_id
    
    # Validar los datos del formulario
    if not Curso.validate_curso(form_data):
        return redirect(url_for('cursos.edit', curso_id=curso_id))
    
    # Actualizar el curso
    if Curso.update(form_data):
        flash("Curso actualizado con exito", "success")
        return redirect(url_for('cursos.show', curso_id=curso_id))
    else:
        flash("Error al actualizar el curso", "error")
        return redirect(url_for('cursos.edit', curso_id=curso_id))

#Ruta para eliminar un curso
@cursos_bp.route('/cursos/<int:curso_id>/delete', methods=['POST'])
def delete(curso_id):
    if Curso.delete(curso_id):
        flash("Curso eliminado con exito", "success")
    else:
        flash("Error al eliminar el curso", "error")
    return redirect(url_for('cursos.index'))
