# Sistema CRUD de Usuarios

Un sistema completo de gestión de usuarios desarrollado con Flask, que incluye operaciones CRUD (Create, Read, Update, Delete) y autenticación de usuarios.

## Características

- ✅ **CRUD Completo**: Crear, leer, actualizar y eliminar usuarios, estudiantes y cursos
- ✅ **Autenticación**: Sistema de login/logout con sesiones
- ✅ **Validación**: Validación de formularios y emails únicos
- ✅ **Seguridad**: Contraseñas encriptadas con bcrypt
- ✅ **Interfaz Moderna**: Diseño responsive con Bootstrap 5
- ✅ **Base de Datos**: Integración con MySQL
- ✅ **Módulos Separados**: Gestión independiente de usuarios, estudiantes y cursos
- ✅ **Relaciones**: Estudiantes asociados a cursos específicos

## Requisitos Previos

- Python 3.7+
- MySQL 5.7+
- pip (gestor de paquetes de Python)

## Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd Proyecto_usuario
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requeriments.txt
   ```

3. **Configurar la base de datos**
   - Abrir MySQL y ejecutar el archivo `database_setup.sql`
   - O crear manualmente la base de datos `esquema` y la tabla `usuarios`

4. **Configurar la conexión a la base de datos**
   - Editar `base/config/mysqlconnection.py` si es necesario
   - Cambiar credenciales de MySQL (usuario, contraseña, host, puerto)

## Uso

1. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```
   O alternativamente:
   ```bash
   python server.py
   ```

2. **Acceder a la aplicación**
   - Abrir el navegador en `http://localhost:5000`
   - La aplicación redirigirá automáticamente según el estado de sesión

## Estructura del Proyecto

```
Proyecto_usuario/
├── app.py                          # Punto de entrada principal
├── server.py                       # Servidor alternativo
├── database_setup.sql             # Script de configuración de BD
├── requeriments.txt               # Dependencias de Python
├── readme.md                      # Este archivo
└── base/                          # Módulo principal de la aplicación
    ├── __init__.py               # Configuración de Flask
    ├── config/
    │   └── mysqlconnection.py     # Conexión a MySQL
    ├── controllers/
    │   └── user_controller.py     # Controladores de usuarios
    ├── models/
    │   └── user.py               # Modelo de usuario
    ├── static/
    │   ├── css/
    │   │   └── style.css         # Estilos personalizados
    │   └── js/
    │       └── main.js           # JavaScript personalizado
    └── templates/                # Plantillas HTML
        ├── base.html            # Plantilla base
        ├── bienvenida.html      # Página de bienvenida
        └── users/               # Plantillas de usuarios
            ├── index.html        # Lista de usuarios
            ├── new.html          # Crear usuario
            ├── show.html         # Ver usuario
            ├── edit.html         # Editar usuario
            ├── login.html        # Iniciar sesión
            └── dashboard.html    # Panel de usuario
```

## Funcionalidades

### Para Usuarios No Autenticados
- Ver página de bienvenida
- Registrarse como nuevo usuario
- Iniciar sesión
- Ver lista pública de usuarios

### Para Usuarios Autenticados
- Acceder al dashboard personal
- Ver, editar y eliminar usuarios
- Crear nuevos usuarios
- Cerrar sesión

## Rutas Disponibles

### Usuarios
- `/` - Página de bienvenida
- `/users` - Lista de usuarios
- `/users/new` - Formulario de nuevo usuario
- `/users/create` - Crear usuario (POST)
- `/users/<id>` - Ver usuario específico
- `/users/<id>/edit` - Editar usuario
- `/users/<id>/update` - Actualizar usuario (POST)
- `/users/<id>/delete` - Eliminar usuario (POST)
- `/login` - Formulario de login
- `/dashboard` - Panel de usuario autenticado
- `/logout` - Cerrar sesión

### Estudiantes
- `/estudiantes` - Lista de estudiantes
- `/estudiante/new` - Formulario de nuevo estudiante
- `/estudiantes/create` - Crear estudiante (POST)
- `/estudiantes/<id>` - Ver estudiante específico
- `/estudiantes/<id>/edit` - Editar estudiante
- `/estudiantes/<id>/update` - Actualizar estudiante (POST)
- `/estudiantes/<id>/delete` - Eliminar estudiante (POST)

### Cursos
- `/cursos` - Lista de cursos
- `/cursos/new` - Formulario de nuevo curso
- `/cursos/create` - Crear curso (POST)
- `/cursos/<id>` - Ver curso específico y sus estudiantes
- `/cursos/<id>/edit` - Editar curso
- `/cursos/<id>/update` - Actualizar curso (POST)
- `/cursos/<id>/delete` - Eliminar curso (POST)

## Configuración de Base de Datos

La aplicación utiliza MySQL con las siguientes estructuras:

### Base de datos: esquema (usuarios)
```sql
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Base de datos: esquema_estudiantes_cursos
```sql
CREATE TABLE cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    curso_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE SET NULL
);
```

## Usuarios de Prueba

El script `database_setup.sql` incluye datos de ejemplo:

### Usuarios
- **Email**: juan@ejemplo.com, **Contraseña**: 123456
- **Email**: maria@ejemplo.com, **Contraseña**: 123456
- **Email**: carlos@ejemplo.com, **Contraseña**: 123456

### Cursos
- Programación Web
- Base de Datos
- Python Avanzado
- Desarrollo Móvil

### Estudiantes
- Ana Martínez (Programación Web)
- Luis Rodríguez (Programación Web)
- Carmen González (Base de Datos)
- Pedro Sánchez (Python Avanzado)
- Laura Fernández (Desarrollo Móvil)

## Solución de Problemas

### Error de Conexión a MySQL
- Verificar que MySQL esté ejecutándose
- Comprobar credenciales en `mysqlconnection.py`
- Asegurar que la base de datos `esquema` existe

### Error de Importación
- Verificar que todas las dependencias estén instaladas
- Ejecutar `pip install -r requeriments.txt`

### Error de Templates
- Verificar que los archivos HTML estén en `base/templates/`
- Comprobar la estructura de directorios

## Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: MySQL
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Seguridad**: Flask-Bcrypt para encriptación
- **ORM**: PyMySQL para conexión a base de datos

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
