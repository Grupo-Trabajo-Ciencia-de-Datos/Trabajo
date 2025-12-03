# analisis.py
import sqlite3
from typing import Dict, Any, List

DB_PATH = "gastos.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def resumen_mensual(anio: int, mes: int) -> Dict[str, Any]:
    mes_str = f"{mes:02d}"

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT categoria, SUM(monto) AS total_categoria
            FROM gastos
            WHERE strftime('%Y', fecha) = ?
                AND strftime('%m', fecha) = ?
            GROUP BY categoria
        """, (str(anio), mes_str))

        rows = cur.fetchall()
        detalles = [{"categoria": row["categoria"], "total": float(row["total_categoria"])} for row in rows]
        total_general = sum(d["total"] for d in detalles)

    return {
        "anio": anio,
        "mes": mes,
        "total_general": total_general,
        "detalles": detalles
    }

def escenario_inflacion(porcentaje: float) -> Dict[str, Any]:
    factor = 1 + porcentaje / 100

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT SUM(monto) AS total_actual FROM gastos")
        row = cur.fetchone()
        total_actual = float(row["total_actual"]) if row["total_actual"] else 0.0

    total_ajustado = total_actual * factor

    return {
        "porcentaje_inflacion": porcentaje,
        "total_actual": total_actual,
        "total_ajustado": total_ajustado,
        "diferencia": total_ajustado - total_actual
    }

def escenario_tipo_cambio(tipo_cambio: float) -> Dict[str, Any]:
    if tipo_cambio <= 0:
        raise ValueError("El tipo de cambio debe ser mayor que 0.")

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT SUM(monto) AS total_clp FROM gastos")
        row = cur.fetchone()
        total_clp = float(row["total_clp"]) if row["total_clp"] else 0.0

    total_usd = total_clp / tipo_cambio

    return {
        "tipo_cambio": tipo_cambio,
        "total_clp": total_clp,
        "total_usd": total_usd
    }
