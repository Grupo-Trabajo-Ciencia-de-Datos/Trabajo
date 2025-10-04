# Entrega 2 — Ciencia de Datos

Proyecto: Costo de vida universitario en Chile  
Integrantes: André van Bavel, Nicolás Droppelmann


# Resumen
Este proyecto implementa una API en FastAPI que simula el presupuesto mensual de un estudiante universitario en Chile. Incluye 3 endpoints personales (familia, gastos, académico) y un CRUD basico y un esquema inicial de base de datos SQL.


# Instrucciones de cómo probar la API

# 1. Crear y activar el entorno virtual 
En la terminal, dentro de la carpeta del proyecto:
python -m venv venv
.\venv\Scripts\Activate

# 2. Instalar dependencias necesarias
pip install fastapi uvicorn

# 3. Ejecutar la API
python -m uvicorn main:app --reload

# 4. Abrir en el navegador el siguiente link:
http://127.0.0.1:8000/docs

# Documentacion de endpoints personales

1. Familia: Devuelve la estructura del hogar universitario.
    Metodo: GET
    Ruta: /api/personal/familia
    Ejemplo de respuesta:
    {
        "tamaño_hogar": 3,
        "comuna": "Santiago Centro",
        "tipo_vivienda": "departamento compartido"
    }

2. Gastos Mensuales: Devuelve el gasto mensual simulado por categoría.
    Metodo: GET
    Ruta: /api/personal/gastos-mensuales
    Ejemplo de respuesta:
    {
        "Gastos": {
            "alimentacion": 105000,
            "transporte": 20000,
            "vivienda": 250000,
            "educacion": 80000,
            "ocio": 50000
      },
      "Total": 505000
    }

3. Academico: Devuelve la carga académica simulada del semestre.
    Metodo: GET
    Ruta: /api/personal/academico
    Ejemplo de respuesta:
        {
            "ramos": 5,
            "horas_semana": 22,
            "modalidad": "presencial"
        }