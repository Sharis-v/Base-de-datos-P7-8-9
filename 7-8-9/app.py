import os
import time
import psycopg2
from flask import Flask, render_template, url_for, redirect

# 1. Definir la aplicación Flask
app = Flask(__name__)

# 2. Configuración de las 20 consultas (Prácticas 7, 8 y 9)
consultas = {
    "1": {"cat": "P7: Selección", "t": "Cursos con créditos > 3", "desc": "Filtra los cursos que tienen una carga académica mayor a 3 créditos.", "ar": "σ creditos > 3 (CURSO)", "crt": "{t | CURSO(t) ∧ t.creditos > 3}", "crd": "{<id, tit, cre, dep> | <id, tit, cre, dep> ∈ CURSO ∧ cre > 3}", "sql": "SELECT * FROM CURSO WHERE creditos > 3"},
    "2": {"cat": "P7: Proyección", "t": "Nombres de Estudiantes", "desc": "Extrae exclusivamente la columna de nombres de la tabla Estudiante.", "ar": "π nombre (ESTUDIANTE)", "crt": "{t | ∃e (ESTUDIANTE(e) ∧ t.nombre = e.nombre)}", "crd": "{<nom> | ∃i,c,p (<i,nom,c,p> ∈ ESTUDIANTE)}", "sql": "SELECT nombre FROM ESTUDIANTE"},
    "3": {"cat": "P7: Unión", "t": "Nombres de Profesores y Estudiantes", "desc": "Combina los nombres de ambas tablas eliminando duplicados.", "ar": "π nombre (ESTUDIANTE) ∪ π nombre (PROFESOR)", "crt": "{t | ∃e (ESTUDIANTE(e) ∧ t.nombre = e.nombre) ∨ ∃p (PROFESOR(p) ∧ t.nombre = p.nombre)}", "crd": "N/A", "sql": "SELECT nombre FROM ESTUDIANTE UNION SELECT nombre FROM PROFESOR"},
    "4": {"cat": "P7: Intersección", "t": "Profesores que lideran proyectos", "desc": "Identifica a los profesores cuyo ID aparece también en la tabla de Proyectos como líderes.", "ar": "π id_prof (PROFESOR) ∩ π id_lider (PROYECTO)", "crt": "{t | ∃p(PROFESOR(p) ∧ t.id=p.id_prof) ∧ ∃pr(PROYECTO(pr) ∧ t.id=pr.id_lider)}", "crd": "N/A", "sql": "SELECT id_prof FROM PROFESOR INTERSECT SELECT id_lider FROM PROYECTO"},
    "5": {"cat": "P7: Diferencia", "t": "Departamentos sin cursos", "desc": "Muestra los departamentos que no tienen ninguna oferta académica registrada.", "ar": "π id_depto (DEPARTAMENTO) - π id_depto (CURSO)", "crt": "{d | DEPARTAMENTO(d) ∧ ¬∃c(CURSO(c) ∧ c.id_depto=d.id_depto)}", "crd": "N/A", "sql": "SELECT id_depto FROM DEPARTAMENTO EXCEPT SELECT id_depto FROM CURSO"},
    "6": {"cat": "P8: Join", "t": "Estudiantes y sus Departamentos", "desc": "Une la tabla Estudiante con Departamento para mostrar a qué edificio pertenecen.", "ar": "ESTUDIANTE ⋈ DEPARTAMENTO", "crt": "{t | ∃e,d (ESTUDIANTE(e) ∧ DEPARTAMENTO(d) ∧ e.id_depto = d.id_depto)}", "crd": "N/A", "sql": "SELECT E.nombre, D.nombre as depto FROM ESTUDIANTE E JOIN DEPARTAMENTO D ON E.id_depto = D.id_depto"},
    "7": {"cat": "P8: Agregación", "t": "Promedio de Notas por Estudiante", "desc": "Calcula la nota media de cada estudiante inscrita en el sistema.", "ar": "id_est γ AVG(nota) (INSCRIPCION)", "crt": "N/A", "crd": "N/A", "sql": "SELECT id_est, AVG(nota) FROM INSCRIPCION GROUP BY id_est"},
    "8": {"cat": "P8: Agrupación (COUNT)", "t": "Total de alumnos por carrera", "desc": "Cuenta cuántos estudiantes están inscritos en cada carrera.", "ar": "carrera γ COUNT(id_est) (ESTUDIANTE)", "crt": "N/A", "crd": "N/A", "sql": "SELECT carrera, COUNT(id_est) FROM ESTUDIANTE GROUP BY carrera"},
    "9": {"cat": "P8: División", "t": "Estudiantes en TODOS los cursos", "desc": "Identifica alumnos inscritos en la totalidad de los cursos ofrecidos.", "ar": "INSCRIPCION ÷ CURSO", "crt": "{e | ESTUDIANTE(e) ∧ ∀c(CURSO(c) ⇒ ∃i,s(i.id_est=e.id_est ∧ s.id_curso=c.id_curso))}", "crd": "N/A", "sql": "SELECT nombre FROM ESTUDIANTE E WHERE NOT EXISTS (SELECT id_curso FROM CURSO EXCEPT SELECT S.id_curso FROM INSCRIPCION I JOIN SECCION S ON I.id_sec = S.id_sec WHERE I.id_est = E.id_est)"},
    "10": {"cat": "P8: Left Join", "t": "Profesores y sus proyectos", "desc": "Muestra todos los profesores y el proyecto que lideran, incluyendo profesores sin proyecto.", "ar": "PROFESOR ⟕ PROYECTO", "crt": "N/A", "crd": "N/A", "sql": "SELECT P.nombre, PR.nombre_p FROM PROFESOR P LEFT JOIN PROYECTO PR ON P.id_prof = PR.id_lider"},
    "11": {"cat": "P9: Cálculo Relacional (∃)", "t": "Profesores con Proyectos (Existencial)", "desc": "Usa el cuantificador existencial para hallar profesores con al menos un proyecto.", "ar": "π nombre (PROFESOR ⋈ PROYECTO)", "crt": "{p | PROFESOR(p) ∧ ∃pr(PROYECTO(pr) ∧ pr.id_lider = p.id_prof)}", "crd": "N/A", "sql": "SELECT nombre FROM PROFESOR WHERE id_prof IN (SELECT id_lider FROM PROYECTO)"},
    "12": {"cat": "P9: Cálculo Relacional (∀)", "t": "Cursos con notas perfectas", "desc": "Cursos donde todos los alumnos tienen nota mayor a 9.", "ar": "N/A", "crt": "{c | CURSO(c) ∧ ∀i(INSCRIPCION(i) ⇒ i.nota > 9)}", "crd": "N/A", "sql": "SELECT titulo FROM CURSO C WHERE NOT EXISTS (SELECT 1 FROM INSCRIPCION I JOIN SECCION S ON I.id_sec = S.id_sec WHERE S.id_curso = C.id_curso AND I.nota <= 9)"},
    "13": {"cat": "P9: CRT - Selección Compuesta", "t": "Sistemas con Promedio Alto", "desc": "Cálculo de tuplas para alumnos de Sistemas con promedio > 9.", "ar": "σ carrera='Sistemas' ∧ promedio > 9 (ESTUDIANTE)", "crt": "{t | ESTUDIANTE(t) ∧ t.carrera='Sistemas' ∧ t.promedio > 9}", "crd": "N/A", "sql": "SELECT * FROM ESTUDIANTE WHERE carrera='Sistemas' AND promedio > 9"},
    "14": {"cat": "P9: CRD - Join Triple", "t": "Relación Alumno-Curso-Nota", "desc": "Cálculo de dominios para mostrar el historial académico detallado.", "ar": "E ⋈ I ⋈ S ⋈ C", "crt": "N/A", "crd": "{<n, tit, no> | ∃id,sid,cid... (<id,n,...> ∈ ESTUDIANTE ∧ <id,sid,no> ∈ INSCRIPCION ∧ <cid,tit,...> ∈ CURSO)}", "sql": "SELECT E.nombre, C.titulo, I.nota FROM ESTUDIANTE E JOIN INSCRIPCION I ON E.id_est = I.id_est JOIN SECCION S ON I.id_sec = S.id_sec JOIN CURSO C ON S.id_curso = C.id_curso"},
    "15": {"cat": "P9: Negación", "t": "Alumnos sin inscripciones", "desc": "Usa negación en cálculo para hallar alumnos que no se han inscrito a nada.", "ar": "ESTUDIANTE ▷ INSCRIPCION", "crt": "{e | ESTUDIANTE(e) ∧ ¬∃i(INSCRIPCION(i) ∧ i.id_est=e.id_est)}", "crd": "N/A", "sql": "SELECT nombre FROM ESTUDIANTE WHERE id_est NOT IN (SELECT id_est FROM INSCRIPCION)"},
    "16": {"cat": "P7: Selección", "t": "Departamentos en Edificio A", "desc": "Muestra los departamentos ubicados físicamente en el Edificio A.", "ar": "σ edificio = 'Edificio A' (DEPARTAMENTO)", "crt": "{t | DEPARTAMENTO(t) ∧ t.edificio = 'Edificio A'}", "crd": "N/A", "sql": "SELECT * FROM DEPARTAMENTO WHERE edificio = 'Edificio A'"},
    "17": {"cat": "P8: Agregación (MAX)", "t": "Presupuesto máximo", "desc": "Halla el presupuesto más alto entre todos los departamentos.", "ar": "γ MAX(presupuesto) (DEPARTAMENTO)", "crt": "N/A", "crd": "N/A", "sql": "SELECT MAX(presupuesto) FROM DEPARTAMENTO"},
    "18": {"cat": "P9: Existencial", "t": "Alumnos en proyectos", "desc": "Encuentra estudiantes que están colaborando en algún proyecto.", "ar": "π nombre (ESTUDIANTE ⋈ PARTICIPACION)", "crt": "{e | ESTUDIANTE(e) ∧ ∃p(PARTICIPACION(p) ∧ p.id_est=e.id_est)}", "crd": "N/A", "sql": "SELECT DISTINCT nombre FROM ESTUDIANTE WHERE id_est IN (SELECT id_est FROM PARTICIPACION)"},
    "19": {"cat": "P8: Theta Join", "t": "Proyectos vs Depto", "desc": "Muestra proyectos cuyo presupuesto excede el del departamento del líder.", "ar": "PROYECTO ⋈_{cond} DEPARTAMENTO", "crt": "N/A", "crd": "N/A", "sql": "SELECT PR.nombre_p FROM PROYECTO PR JOIN PROFESOR P ON PR.id_lider = P.id_prof JOIN DEPARTAMENTO D ON P.id_depto = D.id_depto WHERE PR.presupuesto > D.presupuesto"},
    "20": {"cat": "P8: Agrupación (HAVING)", "t": "Carreras con promedio > 8", "desc": "Muestra las carreras cuyo promedio de todos sus alumnos supera el 8.", "ar": "N/A", "crt": "N/A", "crd": "N/A", "sql": "SELECT carrera, AVG(promedio) FROM ESTUDIANTE GROUP BY carrera HAVING AVG(promedio) > 8"}
}

# 3. Función para conectar a la base de datos
def query_db(sql):
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'db'),
            database='universidad',
            user='usuario',
            password='ariana'
        )
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cols = [d[0] for d in cur.description]
        cur.close()
        conn.close()
        return res, cols
    except Exception as e:
        return [("Error de conexión", str(e))], ["Error"]

# 4. Rutas de la Aplicación
@app.route('/')
def home():
    # Buscamos la imagen descargada de Mermaid en static/diagrama.png
    img_path = os.path.join(app.root_path, 'static', 'diagrama.png')
    diagrama_existe = os.path.exists(img_path)
    
    # 'version' evita que el navegador guarde la imagen vieja en caché
    version = int(time.time())
    
    return render_template('index.html', 
                           consultas=consultas, 
                           diagrama_listo=diagrama_existe, 
                           version=version)

@app.route('/run/<id>')
def run(id):
    if id in consultas:
        c = consultas[id]
        res, cols = query_db(c['sql'])
        version = int(time.time())
        return render_template('index.html', consultas=consultas, sel=c, res=res, cols=cols, version=version)
    return redirect(url_for('home'))

@app.route('/generar_diagrama')
def generar_diagrama():
    # Esta ruta ya no genera el código, solo vuelve al inicio
    # para mostrar el diagrama.png que ya tienes en static/
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)