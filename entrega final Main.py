# ================================================================
# main.py
# Proyecto: Costo de Vida Universitario en Chile
# Curso: EAE253B - Economía y Ciencia de Datos
# Autores: André van Bavel | Nicolás Droppelmann
# Profesor: Carlos Alvarado
# Fecha: 5 de Diciembre, 2025
# ================================================================

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sqlite3
import requests
from datetime import datetime
from analisis import resumen_mensual, escenario_inflacion, escenario_tipo_cambio


app = FastAPI(
    title="API - Costo de Vida Universitario en Chile",
    description="Analiza cómo la inflación y el tipo de cambio afectan los gastos de un estudiante chileno.",
    version="3.0"
)

# ---------------------------
# Modelos y conexión a la BD
# ---------------------------


class Gasto(BaseModel):
    """
    Modelo Pydantic que representa un gasto individual con su categoría y monto.
    """
    categoria: str
    monto: float


def get_db_connection():
    """
    Crea y devuelve una conexión a la base de datos SQLite 'gastos.db'.
    Configura row_factory para obtener los resultados como diccionarios.
    """
    conn = sqlite3.connect("gastos.db")
    conn.row_factory = sqlite3.Row
    return conn


def obtener_ipc_ultimo_valido() -> float:
    """
    Consulta la API pública de mindicador.cl y devuelve el último valor de IPC
    cuyo valor sea distinto de 0. Lanza una excepción HTTP si no hay datos válidos.
    """
    r = requests.get("https://mindicador.cl/api/ipc")
    d = r.json()

    for punto in d["serie"]:
        if punto["valor"] != 0:
            return punto["valor"]

    raise HTTPException(
        status_code=502,
        detail="IPC no disponible temporalmente (todos los valores son 0)."
    )


# ---------------------------
# Endpoints personales
# ---------------------------


@app.get("/personal/familia", tags=["Personales"])
def info_familia():
    """
    Entrega información básica del estudiante y su grupo familiar a modo de ejemplo personal.
    """
    return {
        "nombre_andre": "André Van Bavel",
        "ciudad_andre": "Curicó, Chile",
        "familia_andre": 5,
        "edad_andre": 24,
        "estado_andre": "Soltero",
        "nombre_nicolas": "Nicolás Droppelmann",
        "ciudad_nicolas": "Vermont,EE.UU.",
        "familia_nicolas": 5,
        "edad_nicolas": 23,
        "estado_nicolas": "Casado"
    }


@app.get("/personal/intereses", tags=["Personales"])
def intereses():
    """
    Devuelve una lista de intereses personales relacionados con economía, ciencia de datos y hobbies.
    """
    return {
        "nombre": "André Van Bavel",
        "intereses_andre": ["Economía", "Ciencia de Datos", "Fútbol", "Viajar", "Proyectos personales"],
        "nombre": "Nicolás Droppelmann",
        "intereses_nicolas": ["Economía", "Ciencia de Datos", "Fútbol", "Viajar", "Rezar los sabados por la noche"]
    }


@app.get("/personal/historial", tags=["Personales"])
def historial():
    """
    Resume el historial académico del estudiante: carrera, universidad, semestres cursados y promedio.
    """
    return {
        "nombre": "André Van Bavel",
        "carrera": "Ingeniería Comercial",
        "universidad": "Pontificia Universidad Católica de Chile",
        "semestres_cursados": 9,
        "promedio": 6.1,
        "nombre": "Nicolás Droppelmann",
        "carrera": "Ingeniería Comercial",
        "universidad": "Pontificia Universidad Católica de Chile",
        "semestres_cursados": 8,
        "promedio": 3.95
    }


# ---------------------------
# Endpoints de gastos (CRUD)
# ---------------------------


@app.get("/api/db/gastos", tags=["Base de Datos"])
def obtener_gastos():
    """
    Devuelve la lista completa de gastos registrados en la base de datos SQLite 'gastos.db'.
    """
    conn = get_db_connection()
    gastos = conn.execute("SELECT * FROM gastos").fetchall()
    conn.close()
    return [dict(g) for g in gastos]


@app.post("/api/db/gastos", tags=["Base de Datos"])
def agregar_gasto(gasto: Gasto):
    """
    Inserta un nuevo gasto en la base de datos con la categoría, el monto y la fecha actual.
    """
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO gastos (categoria, monto, fecha) VALUES (?, ?, ?)",
        (gasto.categoria, gasto.monto, datetime.now().strftime("%Y-%m-%d"))
    )
    conn.commit()
    conn.close()
    return {"mensaje": "Gasto agregado", "categoria": gasto.categoria, "monto": gasto.monto}


@app.get("/api/db/gastos/{gasto_id}", tags=["Base de Datos"])
def obtener_gasto_por_id(gasto_id: int):
    """
    Recupera un gasto específico según su identificador único (id) desde la base de datos.
    """
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM gastos WHERE id = ?", (gasto_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return dict(row)


@app.put("/api/db/gastos/{gasto_id}", tags=["Base de Datos"])
def actualizar_gasto(gasto_id: int, gasto: Gasto):
    """
    Actualiza la categoría y el monto de un gasto existente identificado por su id.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE gastos SET categoria = ?, monto = ? WHERE id = ?",
        (gasto.categoria, gasto.monto, gasto_id)
    )
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return {"mensaje": "Gasto actualizado", "id": gasto_id}


@app.delete("/api/db/gastos/{gasto_id}", tags=["Base de Datos"])
def eliminar_gasto(gasto_id: int):
    """
    Elimina de forma permanente un gasto de la base de datos según su id.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM gastos WHERE id = ?", (gasto_id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return {"mensaje": "Gasto eliminado correctamente"}


# ---------------------------
# Endpoints económicos externos
# ---------------------------


@app.get("/api/economia/ipc", tags=["Económicos"])
def obtener_ipc():
    """
    Obtiene el último valor disponible del IPC desde la API pública de mindicador.cl,
    ignorando registros cuyo valor sea 0.
    """
    try:
        r = requests.get("https://mindicador.cl/api/ipc")
        d = r.json()

        punto_valido = None
        for punto in d["serie"]:
            if punto["valor"] != 0:
                punto_valido = punto
                break

        if punto_valido is None:
            raise HTTPException(
                status_code=502,
                detail="IPC no disponible temporalmente (todos los valores son 0)."
            )

        return {
            "indicador": d["nombre"],
            "fecha": punto_valido["fecha"][:10],
            "valor": punto_valido["valor"],
            "fuente": "mindicador.cl"
        }
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener IPC.")


@app.get("/api/economia/tipo_cambio", tags=["Económicos"])
def obtener_tipo_cambio():
    """
    Obtiene el valor del dólar observado en Chile desde la API pública de mindicador.cl.
    """
    try:
        r = requests.get("https://mindicador.cl/api/dolar")
        d = r.json()
        return {
            "indicador": d["nombre"],
            "fecha": d["serie"][0]["fecha"][:10],
            "valor": d["serie"][0]["valor"],
            "fuente": "mindicador.cl"
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener tipo de cambio.")


# ---------------------------
# Endpoints base de datos (indicadores)
# ---------------------------


@app.get("/api/db/indicadores", tags=["Base de Datos"])
def obtener_indicadores(indicador: str):
    """
    Consulta la tabla 'indicadores' en la base de datos y devuelve todos los registros
    asociados al nombre de indicador entregado como parámetro.
    """
    conn = get_db_connection()
    data = conn.execute(
        "SELECT * FROM indicadores WHERE indicador = ?",
        (indicador,)
    ).fetchall()
    conn.close()
    if not data:
        raise HTTPException(status_code=404, detail=f"No hay datos del indicador '{indicador}'.")
    return [dict(i) for i in data]


# ---------------------------
# Endpoints analíticos
# ---------------------------


@app.get("/api/analisis/impacto-inflacion", tags=["Analíticos"])
def impacto_inflacion(periodo: str):
    """
    Calcula el impacto estimado de la inflación sobre los gastos registrados
    para un periodo dado, utilizando el valor más reciente de IPC disponible.
    """
    conn = get_db_connection()
    gastos = conn.execute("SELECT categoria, monto FROM gastos").fetchall()
    conn.close()
    if not gastos:
        raise HTTPException(status_code=404, detail="No hay gastos registrados.")

    try:
        ipc = obtener_ipc_ultimo_valido()
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener IPC.")

    impacto = {g["categoria"]: f"+{round(ipc * 0.05, 2)}%" for g in gastos}

    return {
        "periodo": periodo,
        "ipc": ipc,
        "impacto_estimado": impacto,
        "mensaje": f"Costo de vida ↑ {round(ipc * 0.05, 2)}% aprox."
    }


@app.get("/gastos/escenario-inflacion", tags=["Analíticos"])
def api_escenario_inflacion(porcentaje: float):
    """
    Simula cómo cambiaría el total de gastos si la inflación aumentara
    en el porcentaje especificado por el usuario.
    """
    return escenario_inflacion(porcentaje)


@app.get("/gastos/escenario-tipo-cambio", tags=["Analíticos"])
def api_escenario_tipo_cambio(tipo_cambio: float):
    """
    Recalcula el total de gastos expresados en CLP y USD para un tipo de cambio dado.
    """
    try:
        return escenario_tipo_cambio(tipo_cambio)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------
# Endpoint: Visualizador BD (HTML)
# ---------------------------


@app.get("/ver-bd", response_class=HTMLResponse, tags=["Utilidades"])
def ver_base_datos():
    """
    Muestra el contenido de las tablas 'gastos' e 'indicadores' en una página HTML simple.
    """
    conn = get_db_connection()
    
    # Obtener gastos
    gastos = conn.execute("SELECT * FROM gastos").fetchall()
    
    # Obtener indicadores (limitado a últimos 20 para no saturar)
    indicadores = conn.execute("SELECT * FROM indicadores ORDER BY fecha DESC LIMIT 20").fetchall()
    
    conn.close()

    estilo = """
    <style>
        body { font-family: sans-serif; padding: 20px; background: #f4f4f4; }
        h1 { color: #333; }
        h2 { border-bottom: 2px solid #666; padding-bottom: 5px; margin-top: 30px;}
        table { border-collapse: collapse; width: 100%; background: white; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }
        th, td { text-align: left; padding: 12px; border-bottom: 1px solid #ddd; }
        th { background-color: #4CAF50; color: white; }
        tr:hover { background-color: #f5f5f5; }
    </style>
    """

    html = f"""
    <html>
    <head>
        <title>Visualizador de Base de Datos</title>
        {estilo}
    </head>
    <body>
        <h1>📂 Contenido de gastos.db</h1>
        
        <h2>💰 Tabla: Gastos</h2>
        <table>
            <tr>
                <th>ID</th> <th>Categoría</th> <th>Monto</th> <th>Fecha</th>
            </tr>
            {"".join(f"<tr><td>{g['id']}</td><td>{g['categoria']}</td><td>{g['monto']}</td><td>{g['fecha']}</td></tr>" for g in gastos)}
        </table>

        <h2>📈 Tabla: Indicadores (Últimos 20)</h2>
        <table>
            <tr>
                <th>ID</th> <th>Indicador</th> <th>Fecha</th> <th>Valor</th>
            </tr>
            {"".join(f"<tr><td>{i['id']}</td><td>{i['indicador']}</td><td>{i['fecha']}</td><td>{i['valor']}</td></tr>" for i in indicadores)}
        </table>
        <p><em>Vista rápida generada por FastAPI</em></p>
    </body>
    </html>
    """
    return html


# ---------------------------
# Endpoint raíz
# ---------------------------


@app.get("/", tags=["Inicio"])
def home():
    """
    Endpoint raíz de la API. Permite verificar que el servidor está corriendo correctamente.
    """
    return {"mensaje": "API funcionando correctamente"}

