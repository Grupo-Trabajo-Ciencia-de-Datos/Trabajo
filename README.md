Entrega Final – API Costo de Vida Universitario en Chile
EAE253B - Economía y Ciencia de Datos

Autores: André van Bavel | Nicolás Droppelmann
Profesor: Carlos Alvarado
Semestre: 2do semestre 2025
Última actualización: 6 de diciembre de 2025

1. Descripción del Proyecto y Objetivos

Este proyecto desarrolla una API completa que permite analizar el costo de vida mensual de un estudiante universitario en Chile utilizando:

Gastos personales registrados en una base de datos SQLite

Indicadores económicos en tiempo real, obtenidos desde la API pública mindicador.cl

Cálculos analíticos, como:

impacto de la inflación sobre el presupuesto,

simulaciones con otros tipos de cambio,

análisis mensual por categoría.

La API fue desarrollada en FastAPI, integra SQL real para manejo de datos (creación, lectura, actualización y eliminación), y está completamente documentada mediante Swagger UI.

La entrega 4 incorpora:

CRUD completo para gastos

APIs externas funcionando con manejo de errores

Funciones analíticas separadas en analisis.py

Documentación extendida en cada endpoint

Explicación detallada del sistema

Base de datos funcional que se genera automáticamente si no existe

El objetivo es crear una herramienta que mezcle ciencia de datos, economía aplicada y programación, y que permita entender cómo cambian los gastos universitarios frente a shocks económicos reales.

2. Instalación y Configuración
Requisitos Previos

Python 3.9+

pip instalado

(Opcional) SQLite3 CLI instalado para revisar la base de datos

2.1 Crear el entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
pip install fastapi uvicorn requests


SQLite ya viene incluido con Python.

2.2 Crear la Base de Datos

Existen dos formas válidas:

Opción A: ejecutar ingesta.py (recomendada)
python ingesta.py


Esto:

crea gastos.db,

genera las tablas necesarias,

inserta registros de ejemplo.

Si aparece:

Base creada y datos insertados correctamente.


Ya está lista.

Opción B: usar schema.sql
sqlite3 gastos.db < schema.sql


Esto reconstruye la base de datos desde cero.

2.3 Ejecutar la API
uvicorn main:app --reload


Luego entrar a:

 http://127.0.0.1:8000/docs

Aquí se puede probar todo sin usar terminal.

3. Estructura del Proyecto (Entrega 4)
proyecto-costo-vida/
│
├── main.py                # Código principal de la API (endpoints y lógica HTTP)
├── analisis.py            # Funciones económicas (inflación, tipo cambio, resumen mensual)
├── ingesta.py             # Crea y puebla la base de datos
├── schema.sql             # Esquema SQL para construir las tablas
├── gastos.db              # Base de datos SQLite generada
└── README.md              # Este documento


Cada archivo cumple un rol bien definido:

main.py: orquesta la API, la BD y los cálculos.

analisis.py: contiene cálculos reales y simulaciones.

ingesta.py: permite levantar todo desde cero si se borra la BD.

schema.sql: referencia para el modelo de datos.

gastos.db: base funcional requerida por los endpoints.

README.md: documentación del proyecto.

4. Detalle de Endpoints (Entrega Final)

La API cuenta con cuatro grupos de endpoints:

 Endpoints Personales
GET /personal/familia

Devuelve información personal básica.

GET /personal/intereses

Lista intereses declarados por el estudiante.

GET /personal/historial

Información académica relevante.

Estos endpoints existen para cumplir el requerimiento de tener endpoints que no dependen de la BD.

 CRUD Completo para Gastos (SQLite)
GET /api/db/gastos

Devuelve la lista completa de gastos almacenados.

POST /api/db/gastos

Agrega un gasto nuevo con fecha automática.

{
  "categoria": "Arriendo",
  "monto": 350000
}

GET /api/db/gastos/{id}

Busca un gasto específico.

PUT /api/db/gastos/{id}

Actualiza categoría o monto.

DELETE /api/db/gastos/{id}

Elimina un registro por ID.

Estos endpoints utilizan SQL puro para modificar gastos.db.

 Endpoints Económicos (APIs externas reales)
GET /api/economia/ipc

Conecta a mindicador.cl/api/ipc

Busca el último valor válido (evita valores 0)

Devuelve:

nombre del indicador,

fecha,

valor numérico,

fuente de datos.

GET /api/economia/tipo_cambio

Similar al anterior, pero para el dólar observado.

 Endpoints Analíticos (Entrega 4)
GET /api/analisis/impacto-inflacion?periodo=YYYY-MM

Calcula:

IPC real desde la API externa

Impacto porcentual aproximado sobre cada categoría de gasto

Mensaje interpretativo del resultado

Ejemplo de salida:

{
  "periodo": "2025-11",
  "ipc": 4.2,
  "impacto_estimado": {
    "Comida": "+0.21%",
    "Arriendo": "+0.21%"
  }
}

GET /gastos/escenario-inflacion?porcentaje=10

Simula cuánto subiría cada gasto si la inflación fuera 10%.

GET /gastos/escenario-tipo-cambio?tipo_cambio=900

Convierte los gastos estimados del mes a otra moneda o expresa el total en USD/CLP según lo que pida el usuario.

5. Base de Datos (modelo actualizado)
Tabla gastos
id INTEGER PRIMARY KEY AUTOINCREMENT
categoria TEXT
monto REAL
fecha TEXT

Tabla indicadores
id INTEGER PRIMARY KEY AUTOINCREMENT
fecha TEXT
indicador TEXT
valor REAL


El sistema permite registrar, consultar, comparar y simular con estos datos.

6. Explicación de Funcionamiento Interno (Entrega 4 completa)
Cómo fluye la información:

El usuario hace una petición HTTP (por ejemplo: /api/analisis/impacto-inflacion).

FastAPI recibe la solicitud y ejecuta la función del endpoint en main.py.

Dependiendo del endpoint:

Lee la base de datos SQLite,

Llama a la API externa de mindicador.cl,

O ejecuta una función analítica en analisis.py.

Todo se combina en una respuesta JSON clara.

Ejemplo:

main.py → obtener IPC externo → leer gastos del mes → analisis.py → devolver cálculo final

7. Tecnologías Utilizadas

FastAPI — para manejar toda la API

Uvicorn — servidor ASGI

SQLite — base de datos local

Requests — consumir APIs externas

mindicador.cl — datos macroeconómicos reales

8. Contribución del Equipo

André: Desarrollo estructural de la API, endpoints completos, SQL, testing y ajustes finales.

Nicolás: Análisis y documentación, ingesta de datos, soporte a cálculos económicos, revisión final.

Trabajo colaborativo vía GitHub y Visual Studio Code.

9. Próximos pasos

Agregar autenticación básica (token simple)

Añadir paginación a gastos

Mejorar análisis económico (elasticidades, deflactores reales, series de tiempo)

Implementar test unitarios con PyTest

10. Contacto

André van Bavel: andre.vanbavel@uc.cl

Nicolás Droppelmann: ndroppelmann@uc.cl

Profesor: cealvara@uc.cl

Repositorio GitHub:
https://github.com/andrevanbavel-web/Grupo-Trabajo-Ciencia-de-Datos

