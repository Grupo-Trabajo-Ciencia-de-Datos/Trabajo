# scripts/ingesta.py
import sqlite3
import requests

DB_PATH = "gastos.db"
BASE = "https://mindicador.cl/api"  # fuente pública para pruebas

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_tables():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS indicadores (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      indicador TEXT NOT NULL,   -- 'ipc' | 'usdclp'
      fecha TEXT NOT NULL,       -- 'YYYY-MM-DD'
      valor REAL NOT NULL,       -- % mensual (ipc) o precio (usdclp)
      fuente TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

def insertar(indicador: str, fecha: str, valor: float, fuente: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
      INSERT INTO indicadores (indicador, fecha, valor, fuente)
      VALUES (?, ?, ?, ?)
    """, (indicador, fecha, valor, fuente))
    conn.commit()
    conn.close()

def bajar_y_guardar(indicador: str, endpoint: str, max_items: int):
    """
    Descarga serie desde mindicador.cl y guarda las últimas N observaciones.
    indicador: 'ipc' o 'usdclp'
    endpoint:  'ipc' o 'dolar'
    """
    url = f"{BASE}/{endpoint}"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()
    serie = data.get("serie", [])[:max_items]
    fuente = "mindicador.cl"
    for obs in serie:
        # 'fecha' típicamente '2025-09-01T04:00:00.000Z' -> nos quedamos con 'YYYY-MM-DD'
        f_iso = obs["fecha"]
        fecha = f_iso.split("T")[0] if "T" in f_iso else f_iso[:10]
        valor = float(obs["valor"])
        insertar(indicador, fecha, valor, fuente)

if __name__ == "__main__":
    ensure_tables()
    # carga últimos ~24 meses de IPC y ~30 datos recientes de USDCLP
    bajar_y_guardar("ipc", "ipc", max_items=24)
    bajar_y_guardar("usdclp", "dolar", max_items=30)
    print("Ingesta completada ✅")
