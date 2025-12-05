from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

# Configuración de la API

app = FastAPI(
    title="Entrega 2 - Ciencia de Datos",
    version="1.0",
    description="API para simular el costo de vida de un estudiante universitario en Chile."
)


# Modelos Pydantic (para validar datos de entrada)

class GastoIn(BaseModel):
    categoria: str
    monto: int
    fecha: str = None  # opcional


# Base de datos SQLite

def init_db():
    conn = sqlite3.connect("gastos.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            monto INTEGER NOT NULL,
            fecha TEXT DEFAULT CURRENT_DATE
        )
    """)
    conn.commit()
    conn.close()

init_db()


# Endpoints Personales


@app.get("/api/personal/familia")
def get_familia():
    
    # Devuelve la estructura del hogar universitario.
    
    return {
        "tamaño_hogar": 3,
        "comuna": "Santiago Centro",
        "tipo_vivienda": "departamento compartido"
    }

@app.get("/api/personal/gastos-mensuales")
def get_gastos_mensuales():
    
    # Devuelve el gasto mensual simulado por categoría.
    
    gastos = {
        "alimentacion": 105000,
        "transporte": 20000,
        "vivienda": 250000,
        "educacion": 80000,
        "ocio": 50000,
    }
    total = sum(gastos.values())
    return {"Gastos": gastos, "Total": total}

@app.get("/api/personal/academico")
def get_academico():
    
    # Devuelve la carga académica simulada del semestre.
    
    return {
        "ramos": 5,
        "horas_semana": 22,
        "modalidad": "presencial"
    }


# Endpoints CRUD (con base de datos)


@app.post("/api/db/gastos")
def guardar_gasto(gasto: GastoIn):
    
    # Guarda un gasto en la base de datos local.
    
    conn = sqlite3.connect("gastos.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO gastos (categoria, monto, fecha) VALUES (?, ?, ?)",
                (gasto.categoria, gasto.monto, gasto.fecha))
    conn.commit()
    conn.close()
    return {"mensaje": "Gasto guardado exitosamente"}

@app.get("/api/db/gastos/{id}")
def leer_gasto(id: int):
    
    # Recupera un gasto por su ID.
    
    conn = sqlite3.connect("gastos.db")
    cur = conn.cursor()
    cur.execute("SELECT id, categoria, monto, fecha FROM gastos WHERE id = ?", (id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "categoria": row[1], "monto": row[2], "fecha": row[3]}
    return {"error": "Gasto no encontrado"}

