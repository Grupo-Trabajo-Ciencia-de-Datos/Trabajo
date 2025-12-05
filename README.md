 Costo de Vida Universitario en Chile

Entrega Final – EAE253B Economía y Ciencia de Datos

Autores: André van Bavel, Nicolás Droppelmann

Profesor: Carlos Alvarado

Semestre: 2° semestre 2025

Última actualización: 6 de diciembre de 2025


¿De qué trata este proyecto?

Esta API analiza el costo de vida mensual de un estudiante universitario en Chile.
Combina gastos personales almacenados en una base de datos local (SQLite) con indicadores económicos reales obtenidos desde la API pública mindicador.cl
 (IPC y tipo de cambio).

La aplicación ofrece, entre otras cosas:

Registro y consulta de gastos: Un CRUD básico para categorías como alimentación, transporte, ocio, etc.

Consulta de indicadores económicos: Obtención del IPC y tipo de cambio del dólar en tiempo real.

Análisis del presupuesto: Cálculo del impacto de la inflación sobre el presupuesto y simulaciones bajo distintos escenarios de tipo de cambio.

Resumen mensual: Consolidación de gastos por mes y categoría para comprender mejor en qué se está gastando.

Todo esto se expone mediante endpoints REST documentados automáticamente en Swagger (/docs) gracias a FastAPI.


 Instalación y Configuración
Requisitos previos:

Python 3.9 o superior

pip instalado

Crear el entorno virtual e instalar dependencias
python3 -m venv venv
source venv/bin/activate            # En macOS/Linux
venv\Scripts\activate             # En Windows
pip install -r requirements.txt     # Instala fastapi, uvicorn, requests, pydantic, etc.

Configurar la base de datos

Crea el archivo de base de datos y sus tablas ejecutando el esquema SQL:

sqlite3 gastos.db < schema.sql


(Opcional) Si quieres cargar datos macroeconómicos iniciales, ejecuta el script de ingesta:

python scripts/ingesta.py


Este script consulta la API de mindicador.cl y guarda en la tabla indicadores los últimos valores de IPC y dólar. Al finalizar, mostrará un mensaje confirmando la operación.

Cómo ejecutar la API:

Con el entorno virtual activo y la base de datos inicializada, arranca el servidor de desarrollo con Uvicorn:

uvicorn main:app --reload


Abre tu navegador en http://127.0.0.1:8000/docs
 para ver la documentación interactiva de Swagger. Desde ahí podrás probar todos los endpoints.

Endpoints principales:

--Endpoints de gastos (personales)

Método	Ruta	Descripción

GET	/api/db/gastos	Lista todos los gastos guardados en la base de datos.

POST	/api/db/gastos	Agrega un nuevo gasto (requiere categoria y monto).

GET	/api/db/gastos/{id}	Devuelve un gasto específico por su ID.

PUT	/api/db/gastos/{id}	Actualiza la categoría y monto de un gasto existente.

DELETE	/api/db/gastos/{id}	Elimina un gasto por su ID.


--Endpoints de economía (externos)

Método	Ruta	Descripción

GET	/api/economia/ipc	Obtiene el último valor del Índice de Precios al Consumidor (IPC).

GET	/api/economia/tipo_cambio	Obtiene el valor actual del dólar observado (USD/CLP).

Estos endpoints consultan mindicador.cl. Se incluye una validación para devolver el dato más reciente que no sea 0.


--Endpoints de indicadores (base de datos)

Método	Ruta	Descripción

GET	/api/db/indicadores?indicador=ipc	Devuelve los registros históricos de un indicador (ipc o dolar) guardados en la BD.

Endpoints de análisis

Método	Ruta	Parámetros	Descripción

GET	/api/analisis/impacto-inflacion	periodo (str)	Estima el impacto de la inflación sobre los gastos totales para un periodo (por ejemplo 2025-11).

GET	/gastos/escenario-inflacion	porcentaje (float)	Simula el aumento de gastos si la inflación sube un cierto porcentaje. Usa la función escenario_inflacion del módulo analisis.

GET	/gastos/escenario-tipo-cambio	tipo_cambio (float)	Simula el costo de tus gastos si el dólar cambia al valor dado.

Ejemplo de uso: 

Escenario de tipo de cambio

Supongamos que quieres saber cómo afectaría a tus gastos un dólar a CLP 1 000. Puedes llamar:

GET /gastos/escenario-tipo-cambio?tipo_cambio=1000


La respuesta mostrará cómo cada gasto en pesos aumentaría o disminuiría según el nuevo tipo de cambio, junto con un mensaje explicativo.

Base de datos:


La aplicación utiliza dos tablas principales:

-- Tabla de gastos personales
CREATE TABLE gastos (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT,
    monto    REAL,
    fecha    TEXT
);

-- Tabla de indicadores económicos
CREATE TABLE indicadores (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha     TEXT,
    indicador TEXT,
    valor     REAL,
    fuente    TEXT
);


gastos almacena cada gasto que el usuario registra.
indicadores guarda los valores del IPC y tipo de cambio descargados por el script de ingesta o insertados manualmente.

Datos de ejemplo

5 registros de gastos iniciales (arriendo, alimentación, transporte, ocio, educación).

10 registros de IPC y dólar obtenidos de mindicador.cl a lo largo de noviembre/diciembre de 2025.

Tecnologías utilizadas:

FastAPI: framework web moderno y asíncrono para construir APIs en Python.

SQLite: base de datos ligera para almacenamiento local.

Pydantic: validación de datos y creación de modelos.

Uvicorn: servidor ASGI para desarrollo.

APIs externas:

mindicador.cl: fuente oficial chilena para índices como IPC y dólar observado.

Python 3.9+

pip/venv para manejo de dependencias

pytest para pruebas unitarias (no incluidas, pero recomendadas)

Git/GitHub para control de versiones y despliegue.

📈 Próximos pasos y mejoras

Agregar cache para respuestas de APIs externas (menos latencia y menor uso de la cuota de mindicador.cl).

Implementar autenticación básica para endpoints de escritura (POST/PUT/DELETE).

Añadir un endpoint analítico para sensibilizar costos mixtos (CLP + USD) según el tipo de cambio.

Explorar la integración con dashboards (por ejemplo, using Streamlit o Dash) para visualizaciones interactivas.

 
 Contribuciones:
 
División del trabajo

André van Bavel: desarrollo de los endpoints principales.

Nicolás Droppelmann: diseño de escenarios de análisis, desarrollo de documentación y presentación final.

Trabajamos de forma colaborativa utilizando Visual Studio Code y GitHub, compartiendo el repositorio y realizando pruebas conjuntas. Entre clases y ayudantías, discutimos iteraciones y refinamos el enfoque tanto en la parte técnica como en la económica.

📝 Licencia

Proyecto desarrollado para el curso EAE253B – Economía y Ciencia de Datos de la Pontificia Universidad Católica de Chile (2025).
El código se entrega con fines educativos y se puede reutilizar citando a los autores.

📞 Contacto

Estudiante 1: André van Bavel — andre.vanbavel@uc.cl

Estudiante 2: Nicolás Droppelmann — ndroppelmann@uc.cl

Profesor: Carlos Alvarado — cealvara@uc.cl

Repositorio: https://github.com/andrevanbavel-web/Grupo-Trabajo-Ciencia-de-Datos/Trabajo

🙏 Agradecimientos

Profesor Carlos Alvarado y ayudantes del curso por sus explicaciones y guía.

Compañeros del curso por el feedback y colaboración.

Equipo detrás de mindicador.cl
 por proveer datos actualizados.

Última actualización: 6 de diciembre de 2025


