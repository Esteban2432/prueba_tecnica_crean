# Esquema de operación

## Propósito

Este documento describe cómo la solución analítica opera **en el tiempo**, una vez está
en producción: cómo se generan los resultados, cada cuánto se actualizan, quién los
consume, y qué mecanismos existen para vigilar que sigan siendo confiables y para hacerlos
evolucionar.

## 1. Generación de resultados

Los resultados se generan corriendo, en orden, el mismo flujo de notebooks ya construido:

```
00 (diagnóstico) → 01 (integración) → 02 (exploración) → 03 (propensión)
                                                      ↘
                                                        05 (monto y dimensionamiento) → scoring_final.csv
                                                      ↗
                                        04 (segmentación)
```

El notebook 00 es un chequeo de calidad que no necesita correrse cada vez (solo cuando
cambia la estructura de las fuentes); del 01 al 05 sí se ejecutan completos cada ciclo,
porque cada uno depende del resultado del anterior.

## 2. Frecuencia de actualización

La mayoría de las fuentes de datos originales se miden con una foto **mensual** (ver
notebook 00, sección 6). Por eso se propone una **actualización mensual** del pipeline
completo: es la frecuencia más alta a la que realmente cambian los datos de entrada — 
actualizar más seguido no aportaría información nueva, y actualizar con menos frecuencia
dejaría desactualizada la priorización comercial por más tiempo del necesario.

## 3. Consumo de resultados

Ya descrito en el diagrama de procesos (`modelo_conceptual_y_procesos.md`): el resultado
final (`scoring_final.csv`) alimenta el tablero, que consumen el equipo comercial, el
equipo de producto/finanzas y el equipo CREAN, cada uno para un fin distinto.

## 4. Seguimiento (monitoreo)

Una vez la App esté lanzada y empiece a tener adopción real, hay señales concretas que se
deberían vigilar cada ciclo:

| Qué vigilar | Por qué importa |
|---|---|
| Tasa real de adopción vs. la probabilidad promedio que predijo el modelo | Si se alejan mucho, el modelo dejó de representar bien la realidad (el supuesto de usar Invesbot como referencia pierde vigencia una vez hay datos reales de la App) |
| Distribución de `probabilidad_adopcion` y de `monto_potencial_estimado` de un ciclo a otro | Cambios bruscos pueden indicar un problema en los datos de entrada, no necesariamente en el modelo |
| Tamaño de cada grupo/arquetipo (notebook 04) | Si un grupo crece o se reduce mucho, puede valer la pena revisar si los 4 arquetipos siguen siendo representativos |
| Porcentaje de clientes con datos faltantes (`estimador_ingreso`, tipo de vivienda, etc.) | Si ese porcentaje sube mucho, puede ser síntoma de un problema en alguna fuente aguas arriba |

## 5. Mantenimiento — responsables

| Responsabilidad | A cargo de |
|---|---|
| Calidad y disponibilidad de las 7 fuentes de datos originales | Equipo de datos / administración de información |
| Ejecución mensual del pipeline y actualización de `scoring_final.csv` | Equipo CREAN (dueño de la solución) |
| Revisión de los supuestos documentados (ej. el umbral de valores imposibles, el uso de Invesbot como proxy) | Equipo CREAN, en conjunto con negocio |
| Uso del tablero para priorización comercial | Equipo comercial |

## 6. Evolución de la solución

- **Reemplazar el proxy de Invesbot:** una vez la nueva App tenga suficientes clientes
  reales que la hayan adoptado, el modelo de propensión (notebook 03) debería
  reentrenarse usando adopción real de la App como variable objetivo, en vez de la
  tenencia de Invesbot — el proxy actual deja de ser necesario cuando ya existe el dato
  real que se quería aproximar.
- **Revisar los arquetipos:** si el negocio cambia su oferta de productos o su base de
  clientes cambia de composición de forma importante, conviene volver a correr el método
  del codo (notebook 04) para confirmar si 4 grupos siguen siendo el número adecuado.
- **Ajustar supuestos documentados:** cada supuesto de este proyecto (umbral de valores
  imposibles, tratamiento de clientes sin señal de producto, etc.) quedó explícito en los
  notebooks correspondientes — deben revisarse periódicamente, no asumirse como
  permanentes.
