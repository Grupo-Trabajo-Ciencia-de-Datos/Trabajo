-- esquema inicial de base de datos para la entrega 2
-- base: SQLite

PRAGMA foreign_keys = ON;

-- tabla principal de gastos
CREATE TABLE IF NOT EXISTS gastos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT NOT NULL,          -- ejemplo: alimentacion, transporte, vivienda
    monto INTEGER NOT NULL,           -- monto del gasto en CLP
    fecha TEXT NOT NULL DEFAULT (date('now')) -- fecha en formato 'YYYY-MM-DD'
);

-- Indice opcional para consultas mas rapidas por categoria
-- CREATE INDEX IF NOT EXISTS idx_gastos_categoria ON gastos(categoria);

-- verificar poner en terminal:
sqlite3 gastos.db < schema.sql
-- para verificar que se creo tambien poner en terminal:
sqlite3 gastos.db ".tables"
sqlite3 gastos.db ".schemagastos"