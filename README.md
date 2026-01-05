# Base-de-datos-P7-8-9
SGBD Universitario - Implementación de Álgebra Relacional, Cálculo Relacional y SQL con Flask, PostgreSQL y Docker.
# 📚 Álgebra y Cálculo Relacional
**Materia:** Bases de Datos  
**Prácticas:** 7, 8 y 9
**Autor:** Fernanda Sharis Montiel Valdivia
** Este repositorio contiene una aplicación web interactiva desarrollada con Flask y PostgreSQL, diseñada para demostrar la equivalencia entre las expresiones de Álgebra Relacional, Cálculo Relacional y sentencias SQL en un entorno universitario.

## Cómo ejecutar
Este proyecto está dockerizado para evitar errores de configuración.
1. Tener instalado **Docker** y **Docker Compose**.
2. Ejecutar el comando: `docker-compose up --build`
3. Abrir en el navegador: `http://localhost:5000`

## Tecnologías utilizadas
- **Backend:** Python (Flask)
- **Base de Datos:** PostgreSQL
- **Infraestructura:** Docker
- **Frontend:** Bootstrap 5 (Responsive)

## Contenido de las Prácticas
1. **Práctica 7:** Operadores básicos (Selección, Proyección, Unión, Intersección, Diferencia).
2. **Práctica 8:** Operadores avanzados (Join, Agrupación, Agregación y División Relacional).
3. **Práctica 9:** Cálculo Relacional de Tuplas (CRT) y Dominios (CRD) demostrando equivalencia con SQL.

##  Justificación del Proyecto 

Este proyecto ha sido diseñado  para cubrir los requerimientos de entrega mediante un repositorio de GitHub, asegurando la evaluación de la lógica relacional:

1. **Expresiones en Álgebra y Cálculo:** Cada una de las 20 consultas dentro de la aplicación muestra dinámicamente su expresión matemática. Esto permite validar la equivalencia entre el modelo teórico y la ejecución física en SQL.
2. **Descripción en Lenguaje Natural:** Se incluye una explicación clara para cada consulta, facilitando la comprensión de la lógica aplicada.
3. **Población Masiva de Datos:** El sistema cuenta con un script de inicialización (`init.sql`) que genera automáticamente más de 115 registros, cumpliendo con el requisito de volumen de datos.
4. **Esquema EER:** Se integra la visualización del Modelo Entidad-Relación Extendido que rige la base de datos.

---

##  Mapeo de Prácticas y Consultas

| ID   | Práctica | Operación Relacional | Descripción |
|:-----|:--------:|:---------------------|:------------|
| 1-5  |   **P7** |   Operadores Básicos | Selección, Proyección, Unión, Intersección y Diferencia. |
| 6-10 |   **P8** | Operadores Extendidos| Join, Agregación, Agrupación y División Relacional. |
| 11-15|   **P9** |   Cálculo Relacional | Consultas basadas en tuplas (CRT) y dominios (CRD) con cuantificadores. |
| 16-20| **     **|      Combinadas      | Consultas de validación de presupuesto y promedios por carrera. |

| Consulta            | Álgebra Relacional                        | Cálculo Relacional (CRT) |
| :---                | :-----------------                        | :----------------------- |
| **P7: Selección**   | $\sigma_{creditos > 3}(CURSO)$            | $\{t \mid CURSO(t) \wedge t.creditos > 3\}$ |
| **P8: División**    | $INSCRIPCION \div CURSO$                  | $\{e \mid ESTUDIANTE(e) \wedge \forall c(CURSO(c) \Rightarrow \exists i,s(...))\}$ |
| **P9: Existencial** | $\pi_{nombre}(PROFESOR \bowtie PROYECTO)$ | $\{p \mid PROFESOR(p) \wedge \exists pr(PROYECTO(pr) \wedge ...)\}$ |


---

## Guía de Despliegue (Docker)

El proyecto está completamente dockerizado para garantizar que funcione en cualquier entorno sin necesidad de configurar dependencias locales.

### Requisitos:
* Docker Desktop instalado.

### Pasos:
1. **Clonar el repositorio:** `git clone <URL_DEL_REPOSITORIO>`
2. **Construir el entorno:**
   ```bash
   docker-compose down -v
   docker-compose up --build


