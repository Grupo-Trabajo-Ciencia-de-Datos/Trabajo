📌 Costo de Vida Universitario en Chile
Entrega Final – EAE253B Economía y Ciencia de Datos

Autores: André van Bavel | Nicolás Droppelmann
Profesor: Carlos Alvarado
Semestre: 2° semestre 2025
Última actualización: 6 de diciembre de 2025

1. ¿De qué trata este proyecto?

Esta API tiene como objetivo analizar el costo de vida mensual de un estudiante universitario en Chile, combinando:

Gastos personales registrados en una base de datos local.

Indicadores económicos reales, obtenidos desde la API pública mindicador.cl
.

Cálculos analíticos, como:

impacto de la inflación sobre el presupuesto,

simulaciones bajo distintos tipos de cambio,

resúmenes mensuales por categoría.

La API está desarrollada en FastAPI, usa SQLite como base de datos, y expone todos sus endpoints de manera ordenada a través de Swagger (/docs).

Esta entrega final mejora y completa la entrega 3 incorporando:

CRUD completo para la tabla de gastos.

Endpoints analíticos que usan tanto la base de datos como APIs externas.

Documentación clara en el código y en este README.

Separación de la lógica económica en un módulo aparte (analisis.py).

2. Instalación y ejecución
2.1 Requisitos

Python 3.9 o superior

pip instalado

(Opcional) sqlite3 en la terminal para revisar la base de datos

2.2 Crear entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate      # Mac / Linux
venv\Scripts\activate         # Windows

pip install fastapi uvicorn requests


(No es necesario instalar sqlite3 vía pip, viene con Python.)

2.3 Crear la base de datos

Tienes dos opciones válidas:

🔹 Opción A: usar ingesta.py (recomendada)
python ingesta.py


Este script se encarga de:

Crear gastos.db si no existe.

Crear las tablas necesarias.

Insertar datos de ejemplo (gastos e indicadores).

🔹 Opción B: usar schema.sql
sqlite3 gastos.db < schema.sql


Esto recrea la estructura de la base. Luego se pueden insertar datos manualmente o con otros scripts.

2.4 Levantar la API

Con el entorno virtual activado, ejecutar:

uvicorn main:app --reload


Si todo sale bien, deberías ver algo como:

Uvicorn running on http://127.0.0.1:8000


Luego, en el navegador:

👉 http://127.0.0.1:8000/docs

Ahí aparece la documentación interactiva (Swagger) con todos los endpoints.

3. Estructura del proyecto
proyecto-costo-vida/
│
├── main.py         # API principal: endpoints, rutas y conexión con la BD
├── analisis.py     # Funciones de análisis económico (inflación, tipo de cambio, resúmenes)
├── ingesta.py      # Script para crear y poblar la base de datos
├── schema.sql      # Esquema SQL para reconstruir la base de datos
├── gastos.db       # Base SQLite con datos (se genera si no existe)
└── README.md       # Este documento

Resumen rápido de cada archivo

main.py
Define la aplicación FastAPI, el modelo Gasto, las rutas (endpoints) y cómo se conecta con la base de datos y con analisis.py.

analisis.py
Contiene la lógica económica: resumen mensual de gastos, escenarios de inflación y escenarios de tipo de cambio.

ingesta.py
Crea la base gastos.db y la llena con datos iniciales. Es útil para levantar el proyecto desde cero.

schema.sql
Guarda la estructura de las tablas (gastos, indicadores) en SQL puro, para reconstruir la base fácilmente.

gastos.db
Es la base de datos real. La API lee y escribe aquí.

4. Modelo de datos

La base de datos cuenta con dos tablas principales:

CREATE TABLE gastos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  categoria TEXT,
  monto REAL,
  fecha TEXT
);

CREATE TABLE indicadores (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fecha TEXT,
  indicador TEXT,
  valor REAL
);


gastos: contiene los gastos personales (por categoría, monto y fecha).

indicadores: almacena valores históricos de indicadores económicos (IPC, dólar, etc.).

5. Endpoints de la API

A continuación se resumen los endpoints más importantes, agrupados por tipo.

Todos se pueden probar fácilmente desde http://127.0.0.1:8000/docs.

5.1 Endpoints personales

Estos endpoints son más ilustrativos que funcionales, y sirven para cumplir requisitos del curso y mostrar cómo se devuelve información fija.

GET /personal/familia
Devuelve información básica del estudiante y su familia.

GET /personal/intereses
Lista intereses del estudiante (economía, ciencia de datos, etc.).

GET /personal/historial
Entrega información académica (carrera, universidad, semestres cursados, promedio).

5.2 CRUD completo de gastos (SQLite)

Estos endpoints trabajan directamente con la tabla gastos de la base de datos gastos.db.

GET /api/db/gastos
Devuelve todos los gastos registrados.

POST /api/db/gastos
Crea un gasto nuevo.
Ejemplo de body:

{
  "categoria": "Transporte",
  "monto": 30000
}


GET /api/db/gastos/{gasto_id}
Devuelve un gasto específico según su ID.

PUT /api/db/gastos/{gasto_id}
Actualiza la categoría y/o monto de un gasto existente.

DELETE /api/db/gastos/{gasto_id}
Elimina un gasto de forma permanente.

5.3 Endpoints económicos (API externa real)

Estos endpoints consumen datos reales desde mindicador.cl
.

GET /api/economia/ipc

Llama a https://mindicador.cl/api/ipc.

Recorre la serie de datos y toma el último valor distinto de 0 (para evitar registros vacíos).

Devuelve un JSON con:

{
  "indicador": "Índice de Precios al Consumidor (IPC)",
  "fecha": "YYYY-MM-DD",
  "valor": 4.2,
  "fuente": "mindicador.cl"
}


GET /api/economia/tipo_cambio

Llama a https://mindicador.cl/api/dolar.

Devuelve el valor del dólar observado (USD/CLP) más reciente.

5.4 Endpoints sobre la base de datos de indicadores

GET /api/db/indicadores?indicador=ipc
Devuelve todos los registros de la tabla indicadores que coinciden con el nombre del indicador entregado.

Sirve para revisar el histórico guardado por ingesta.py o por otros procesos.

5.5 Endpoints analíticos

Aquí es donde se mezcla todo: gastos personales, datos externos y lógica económica de analisis.py.

GET /api/analisis/impacto-inflacion?periodo=...

Lee los gastos desde gastos.db.

Obtiene el último IPC válido desde mindicador.cl.

Estima un impacto aproximado por categoría.

Devuelve un mensaje interpretando el resultado.

Ejemplo (formato conceptual):

{
  "periodo": "2025-11",
  "ipc": 4.2,
  "impacto_estimado": {
    "Arriendo": "+0.21%",
    "Comida": "+0.21%"
  },
  "mensaje": "Costo de vida ↑ 0.21% aprox."
}

GET /gastos/resumen-mensual?anio=2025&mes=5

Esta ruta se implementa en analisis.py y se expone en main.py.
Calcula para un mes específico:

Total de gastos.

Total por categoría.

Si no hay datos para ese mes, se devuelve un error 404 desde la API.

GET /gastos/escenario-inflacion?porcentaje=10

Simula qué pasa con el presupuesto si la inflación sube, por ejemplo, un 10%.
El resultado permite ver cómo aumentaría el gasto total proyectado.

GET /gastos/escenario-tipo-cambio?tipo_cambio=900

Permite jugar con distintos tipos de cambio (por ejemplo, dólar a 900 o 1.000 pesos) y ver cómo cambiaría el costo de algunos componentes del presupuesto si estuvieran indexados a USD.

5.6 Endpoint raíz

GET /
Solo devuelve un mensaje simple confirmando que la API está viva:

{ "mensaje": "API funcionando correctamente 🚀" }

6. ¿Cómo se conectan todas las piezas?

A grandes rasgos, el flujo es así:

El usuario hace una petición HTTP a un endpoint (por ejemplo, /gastos/escenario-inflacion).

FastAPI (en main.py) recibe esa petición.

Según el endpoint:

Se abre la conexión a la base de datos (gastos.db),

Se consulta una API externa (mindicador.cl),

O se llama a una función en analisis.py.

Se combinan los datos.

Se responde en formato JSON al cliente.

La idea es separar:

Capa de API → main.py (rutas, validaciones, respuestas HTTP)

Capa de lógica → analisis.py (cálculos)

Capa de datos → gastos.db + schema.sql + ingesta.py

7. Tecnologías utilizadas

FastAPI – Framework para construir la API.

Uvicorn – Servidor ASGI para desarrollo.

SQLite – Base de datos local ligera.

Requests – Para conectar con la API de mindicador.cl.

mindicador.cl – Fuente oficial de datos económicos de Chile.

8. Trabajo en equipo

André: desarrollo del código principal de la API, endpoints, conexión con la base de datos, pruebas en Swagger.

Nicolás: apoyo en la lógica de análisis, ingesta de datos, revisión de documentación y preparación para la presentación final.

El trabajo se coordinó usando Visual Studio Code y GitHub, combinando clases, ayudantías y estudio personal.

9. Próximos pasos e ideas de mejora

Implementar autenticación básica (por ejemplo, un token) para los endpoints que modifican datos.

Agregar paginación a los endpoints de gastos cuando la tabla crezca mucho.

Incorporar más análisis económicos (por ejemplo, comparar distintos años, gráficos, etc.).

Escribir tests automáticos con pytest para los endpoints más importantes.

10. Contacto

André van Bavel – andre.vanbavel@uc.cl

Nicolás Droppelmann – ndroppelmann@uc.cl

Profesor: Carlos Alvarado – cealvara@uc.cl


