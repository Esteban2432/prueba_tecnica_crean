# Prueba Técnica CREAN — App de Inversiones

Solución analítica para identificar clientes con mayor probabilidad de adoptar la nueva
App de inversiones y estimar el monto potencial de inversión a 12 meses.

## Resumen ejecutivo

Sobre una base de 859,796 clientes, el modelo estima:

- **~211,000 clientes esperados** que adoptarían la App (~24.5% de la base).
- **~$511.600 millones de pesos** de volumen de inversión esperado en los primeros 12 meses.
- El segmento **preferencial** concentra la mayor parte del volumen esperado con relativamente pocos clientes; el grupo **"Base consolidada con patrimonio"** (uno de los 4 arquetipos identificados) es la mayor oportunidad en volumen absoluto.

**Supuestos clave a tener presentes:**

- No existe todavía ningún cliente que haya "adoptado" la App (aún no se lanza), así que el modelo de propensión usa como aproximación (*proxy*) la tenencia de **Invesbot** — el producto de inversión digital ya existente más parecido a la nueva App.
- Los datos entregados tienen algunos valores extremos que casi con certeza son errores (ej. ingresos mensuales en billones de pesos); se documentaron y trataron explícitamente, sin descartar clientes reales de alto patrimonio.
- Los clientes que no aparecen en alguna tabla de producto se tratan como "sin evidencia del producto", no como "confirmado que no lo tienen" (las fuentes vienen muestreadas, tope de 1 millón de filas cada una).

El detalle completo de cada decisión, con la evidencia que la respalda, está documentado
directamente en los notebooks (`03_Notebooks/`) y en `06_Documentacion/`.

## Estructura del repositorio

- **01_Prueba**: descripción del caso y requerimientos.
- **02_Datos**: fuentes de información originales (7 bases SQLite).
- **03_Notebooks**: el flujo de trabajo completo, en orden de ejecución.
  - `00_diagnostico_y_toma_de_decisiones.ipynb`: calidad de los datos y reglas de limpieza.
  - `01_integracion_y_limpieza.ipynb`: construye la tabla `Cliente 360`.
  - `02_analisis_exploratorio.ipynb`: caracterización de la base de clientes.
  - `03_modelo_propension.ipynb`: modelo de propensión de adopción.
  - `04_segmentacion_clusters.ipynb`: segmentación de clientes en arquetipos.
  - `05_monto_y_dimensionamiento.ipynb`: monto potencial y dimensionamiento del negocio.
- **04_Resultados**: salidas generadas por los notebooks (no se versionan en git — ver
  instrucciones de ejecución abajo).
- **05_Tablero**: tablero interactivo (Streamlit) con los resultados.
- **06_Documentacion**: documentación de negocio de la solución.
  - [`modelo_conceptual_y_procesos.md`](06_Documentacion/modelo_conceptual_y_procesos.md): diagrama de flujo, actores, y cómo se conecta con los procesos de CREAN.
  - [`esquema_de_operacion.md`](06_Documentacion/esquema_de_operacion.md): cómo se actualiza, vigila y mantiene la solución en el tiempo.

## Cómo ejecutar la solución

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Generar los resultados

Los archivos de `04_Resultados/` no están incluidos en el repositorio (se generan al
correr los notebooks — dos de ellos superan el límite de tamaño de archivo de GitHub).
Ejecutar, en orden, desde `03_Notebooks/`:

1. `01_integracion_y_limpieza.ipynb`
2. `03_modelo_propension.ipynb`
3. `04_segmentacion_clusters.ipynb`
4. `05_monto_y_dimensionamiento.ipynb`

(`00_diagnostico_y_toma_de_decisiones.ipynb` y `02_analisis_exploratorio.ipynb` son de
diagnóstico y análisis — no generan archivos que otros notebooks necesiten, se pueden
correr en cualquier momento).

### 3. Correr el tablero

```bash
streamlit run 05_Tablero/app.py
```

## Consideraciones sobre los datos originales

- Cada conjunto de datos se entrega en un archivo **.zip** independiente.
- Dentro de cada archivo comprimido hay una base de datos **SQLite (.db)** con la información correspondiente.
- Cada base de datos contiene una única tabla con hasta **1 millón de registros**.
