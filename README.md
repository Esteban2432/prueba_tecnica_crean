# Prueba Técnica CREAN — App de Inversiones

Solución analítica para identificar clientes con mayor probabilidad de adoptar la nueva
App de inversiones y estimar el monto potencial de inversión a 12 meses.

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
- **06_Documentacion**: modelo conceptual, diagrama de procesos y esquema de operación.

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
