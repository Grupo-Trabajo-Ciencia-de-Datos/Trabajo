Costo de Vida Universitario en Chile

Entrega Final – EAE253B Economía y Ciencia de Datos

Autores: André van Bavel · Nicolás Droppelmann

Profesor: Carlos Alvarado

Semestre: 2º semestre 2025

Última actualización: 6 de diciembre de 2025

1. ¿De qué trata este proyecto?

Esta API analiza el costo de vida mensual de un estudiante universitario en Chile, combinando:

Gastos personales registrados en una base de datos local (SQLite).

Indicadores económicos reales obtenidos desde la API pública mindicador.cl (IPC y dólar).

Cálculos analíticos como:

impacto de la inflación sobre el presupuesto,

simulaciones bajo distintos tipos de cambio,

resúmenes mensuales por categoría.

La API está desarrollada en FastAPI, usa SQLite como base de datos y expone sus endpoints de forma ordenada en Swagger (/docs).

Esta entrega final mejora y completa la entrega 3 incorporando:

CRUD completo de gastos (GET, POST, PUT, DELETE).

Limpieza y validación de datos externos.

Nuevos endpoints analíticos.

Documentación completa del proyecto.

2. 📁 Estructura del Proyecto
proyecto-costo-vida/
│
├── main.py
├── analisis.py
├── schema.sql
├── gastos.db
│
├── scripts/
│   └── ingesta.py
│
└── README.md

3. ⚙️ Instalación y configuración
1. Crear entorno virtual
python -m venv venv


Mac / Linux:

source venv/bin/activate


Windows:

venv\Scripts\activate

2. Instalar dependencias
pip install fastapi uvicorn requests

3. Crear base de datos
sqlite3 gastos.db < schema.sql

4. Ejecutar script de ingesta
python scripts/ingesta.py

5. Iniciar la API
uvicorn main:app --reload


Luego entrar a:

👉 http://127.0.0.1:8000/docs

4. 🧩 Endpoints principales
🔵 Personales

GET /personal/familia
Información básica personal.

GET /personal/intereses
Intereses del estudiante.

GET /personal/historial
Historial académico.

🟢 CRUD de Gastos

GET /api/db/gastos
Lista de todos los gastos.

POST /api/db/gastos
Agregar un nuevo gasto.

GET /api/db/gastos/{id}
Obtener gasto por ID.

PUT /api/db/gastos/{id}
Actualizar gasto.

DELETE /api/db/gastos/{id}
Eliminar gasto.

🟣 APIs Económicas (mindicador.cl)

GET /api/economia/ipc
Obtiene el último IPC válido.

GET /api/economia/tipo_cambio
Obtiene el valor actual del dólar.

🟠 Base de datos de indicadores

GET /api/db/indicadores?indicador=ipc
Consulta histórica local.

🔥 Analíticos

GET /api/analisis/impacto-inflacion
Analiza cómo afecta el IPC al presupuesto.

GET /gastos/escenario-inflacion
Simula alza porcentual de gastos.

GET /gastos/escenario-tipo-cambio
Simula impacto del dólar.

5. 🗂 Base de datos (SQLite)
Tabla: gastos
id INTEGER PRIMARY KEY AUTOINCREMENT,
categoria TEXT,
monto REAL,
fecha TEXT

Tabla: indicadores
id INTEGER PRIMARY KEY AUTOINCREMENT,
fecha TEXT,
indicador TEXT,
valor REAL

6. 🛠 Tecnologías utilizadas

FastAPI

SQLite

Requests

Uvicorn

Swagger UI

7. 👥 Contribución del equipo

André van Bavel
Diseño, endpoints, análisis económico, documentación final.

Nicolás Droppelmann
Funciones analíticas, debugging, SQL, testing.

8. 📬 Contacto

André van Bavel: andre.vanbavel@uc.cl

Nicolás Droppelmann: ndroppelmann@uc.cl

Profesor: Carlos Alvarado — cealvara@uc.cl

Repositorio:
https://github.com/Grupo-Trabajo-Ciencia-de-Datos/Trabajo

9. ⭐ Próximos pasos

Cache local para reducir cargas externas.

Autenticación.

Tests unitarios.

Dashboard visual (Streamlit).

10. ✔️ Última actualización

6 de diciembre de 2025

