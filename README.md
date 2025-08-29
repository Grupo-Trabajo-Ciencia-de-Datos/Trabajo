Propuesta del Proyecto
La idea del proyecto será determinar cómo se puede ver afectado el costo de vida de un estudiante en Chile al modificar sus conductas dentro de un contexto económico nacional que es variable. Lograremos responder preguntas como: ¿Cuánto más costosas pueden ser mis suscripciones mensuales frente a un aumento en el precio del dólar? - ¿Cómo cambia mi poder adquisitivo con la inflación reciente? - ¿Cómo puedo optimizar mis gastos frente a mi presupuesto mensual?
Nos basaremos en dos tipos de información disponible: (i) datos personales ordenados por categorías típicas de un estudiante (comida, transporte, educación, ocio, etc), armando de esta manera una canasta personalizada de referencia. (ii) Datos macroeconómicos oficiales (inflación, tipo de cambio, tasas de política monetaria). De esta manera podremos generar un análisis para distintos escenarios económicos y cómo estos afectan en mayor o menor medida el poder adquisitivo real de un estudiante determinado

Endpoints:
1.GET /api/personal/familia → Entrega de forma anonimizada la estructura del hogar universitario (tamaño, comuna, situación de vivienda) para contextualizar el consumo.

2.GET /api/personal/gastos-mensuales → Devuelve el gasto mensual actual por categorías (alimentación, transporte, vivienda, educación, ocio) como canasta base de referencia.

3.GET /api/personal/academico → Muestra la carga académica/semestre (nº ramos, horas, modalidad), útil para explicar patrones de gasto.

4.GET /api/economia/inflacion/{periodo} → Obtiene la inflación anual o interanual del periodo solicitado desde fuente oficial.

5.GET /api/economia/tpm/{periodo} → Recupera la Tasa de Política Monetaria (TPM) para el periodo, como indicador del ciclo monetario.

6.GET /api/economia/tipo-cambio/{periodo} → Trae USDCLP (mensual o diario agregado) para calcular el encarecimiento de diferentes actividades en respuesta al tipo de cambio.

7.GET /api/finanzas/tasas-credito-consumo → Entrega tasas representativas de crédito de consumo para sensibilizar el costo de financiar imprevistos.

8.GET /api/db/gastos/{id} → Consulta un gasto específico almacenado en la base de datos.

9.PUT /api/db/gastos/{id} → Actualiza un gasto existente (monto o categoría) en la base de datos editable.

10.POST /api/db/gastos → Crea nuevos gastos/categorías para armar escenarios sin tocar la canasta base.

11.DELETE /api/db/gastos/{id} → Elimina un gasto de la base de datos editable para limpiar escenarios simulados.

12.GET /api/analisis/impacto-inflacion?periodo=AAAA → Calcula la pérdida o recuperación del poder adquisitivo real, mostrando equivalencia de gasto nominal a precios actuales y categorías más afectadas.

13.GET /api/analisis/sensibilidad-suscripciones?periodo=AAAA-MM&lista=netflix,spotify → Calcula el cambio porcentual y real de suscripciones en USD ante movimientos del dólar. Usa canasta personal + tipo-cambio.

3. Identificación de fuentes de datos y APIs externas a utilizar. 
 En el caso de la inflación y la TPM ocuparemos las series del Banco Central de Chile, que entrega estadísticas oficiales y actualizadas, de esta fuente también obtendremos el tipo de cambio USD/CLP (dólar observado) para convertir los precios de suscripciones en dólares y medir su sensibilidad frente a cambios en el dólar. Para las tasas de crédito de consumo tomaremos referencias publicadas por la CMF u organismos financieros que las ponen a disposición de forma abierta. Además, de manera opcional, agregaremos un endpoint con datos del World Bank para comparar el PIB per cápita entre países y dar un contexto internacional. 
