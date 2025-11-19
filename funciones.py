import sqlite3

# RUTA A BASE DE DATOS
DB_RUTA = r"M:\DB Browser SQLite projects\Proyecto\proyecto.db"

############################## CONEXIÓN BASE DE DATOS ##############################
def obtener_conexion():
    conexion = sqlite3.connect(DB_RUTA)
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion

# SELECT TABLAS
def listar_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = [t[0] for t in cursor.fetchall()]
    conexion.close()
    return tablas

############################## TABLA ALUMNO ##############################

# INSERT ALUMNO
def insertar_alumno(nombre, correo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO Alumno (nombre, correo) VALUES (?, ?)", (nombre, correo))
    conexion.commit()
    conexion.close()

# SELECT ALUMNO
def obtener_alumnos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Alumno")
    alumnos = cursor.fetchall()
    conexion.close()
    return alumnos

# UPDATE ALUMNO
def actualizar_alumno(id_alumno, nombre=None, correo=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if nombre:
        cursor.execute("UPDATE Alumno SET nombre=? WHERE id_alumno=?", (nombre, id_alumno))
    if correo:
        cursor.execute("UPDATE Alumno SET correo=? WHERE id_alumno=?", (correo, id_alumno))
    conexion.commit()
    conexion.close()

# DELETE ALUMNO
def eliminar_alumno(id_alumno):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM Alumno WHERE id_alumno=?", (id_alumno,))
    conexion.commit()
    conexion.close()

############################## TABLA CURSO ##############################

# INSERT CURSO
def insertar_curso(nombre, descripcion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO Curso (nombre, descripcion) VALUES (?, ?)", (nombre, descripcion))
    conexion.commit()
    conexion.close()

# SELECT CURSO
def obtener_cursos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Curso")
    cursos = cursor.fetchall()
    conexion.close()
    return cursos

def actualizar_curso(id_curso, nombre=None, descripcion=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if nombre:
        cursor.execute("UPDATE Curso SET nombre=? WHERE id_curso=?", (nombre, id_curso))
    if descripcion:
        cursor.execute("UPDATE Curso SET descripcion=? WHERE id_curso=?", (descripcion, id_curso))
    conexion.commit()
    conexion.close()


def eliminar_curso(id_curso):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM Curso WHERE id_curso=?", (id_curso,))
    conexion.commit()
    conexion.close()

############################## TABLA ALUMNO_CURSO ##############################

# INSERT ALUMNO_CURSO
def asignar_alumno_curso(id_alumno, id_curso):
    try:
        with sqlite3.connect(DB_RUTA) as conexion:
            conexion.execute("PRAGMA foreign_keys = ON;")
            conexion.execute(
                "INSERT INTO Alumno_Curso (id_alumno, id_curso) VALUES (?, ?)",
                (id_alumno, id_curso)
            )
    except sqlite3.IntegrityError:
        raise ValueError("Ese alumno ya está en ese curso")


# SELECT ALUMNO_CURSO
def obtener_alumnos_curso():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Alumno_Curso")
    registros = cursor.fetchall()
    conexion.close()
    return registros

# UPDATE ALUMNO_CURSO
def actualizar_alumno_curso(id_alumno, id_curso, nuevo_id_curso):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE Alumno_Curso SET id_curso=? WHERE id_alumno=? AND id_curso=?", (nuevo_id_curso, id_alumno, id_curso))
    conexion.commit()
    conexion.close()

# DELETE ALUMNO_CURSO
def eliminar_alumno_curso(id_alumno, id_curso):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM Alumno_Curso WHERE id_alumno=? AND id_curso=?", (id_alumno, id_curso))
    conexion.commit()
    conexion.close()

############################## TABLA TAREA ##############################

# INSERT TAREA
def insertar_tarea(titulo, fecha_entrega, id_curso):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO Tarea (titulo, fecha_entrega, id_curso) VALUES (?, ?, ?)", (titulo, fecha_entrega, id_curso))
    conexion.commit()
    conexion.close()

# SELECT TAREA
def obtener_tareas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Tarea")
    tareas = cursor.fetchall()
    conexion.close()
    return tareas

# UPDATE TAREA
def actualizar_tarea(id_tarea, titulo=None, fecha_entrega=None, id_curso=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if titulo:
        cursor.execute("UPDATE Tarea SET titulo=? WHERE id_tarea=?", (titulo, id_tarea))
    if fecha_entrega:
        cursor.execute("UPDATE Tarea SET fecha_entrega=? WHERE id_tarea=?", (fecha_entrega, id_tarea))
    if id_curso:
        cursor.execute("UPDATE Tarea SET id_curso=? WHERE id_tarea=?", (id_curso, id_tarea))
    conexion.commit()
    conexion.close()

# DELETE TAREA
def eliminar_tarea(id_tarea):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM Tarea WHERE id_tarea=?", (id_tarea,))
    conexion.commit()
    conexion.close()

############################## TABLA ENTREGA ##############################

# INSERT ENTREGA
def insertar_entrega(id_alumno, id_tarea, fecha, nota):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO Entrega (fecha_envio, nota, id_alumno, id_tarea) VALUES (?, ?, ?, ?)", (fecha, nota, id_alumno, id_tarea))
    conexion.commit()
    conexion.close()

# SELECT ENTREGA
def obtener_entregas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Entrega")
    entregas = cursor.fetchall()
    conexion.close()
    return entregas

# UPDATE ENTREGA
def actualizar_entrega(id_entrega, fecha_envio=None, nota=None, id_alumno=None, id_tarea=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if fecha_envio:
        cursor.execute("UPDATE Entrega SET fecha_envio=? WHERE id_entrega=?", (fecha_envio, id_entrega))
    if nota:
        cursor.execute("UPDATE Entrega SET nota=? WHERE id_entrega=?", (nota, id_entrega))
    if id_alumno:
        cursor.execute("UPDATE Entrega SET id_alumno=? WHERE id_entrega=?", (id_alumno, id_entrega))
    if id_tarea:
        cursor.execute("UPDATE Entrega SET id_tarea=? WHERE id_entrega=?", (id_tarea, id_entrega))
    conexion.commit()
    conexion.close()

# DELETE ENTREGA
def eliminar_entrega(id_entrega):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM Entrega WHERE id_entrega=?", (id_entrega,))
    conexion.commit()
    conexion.close()