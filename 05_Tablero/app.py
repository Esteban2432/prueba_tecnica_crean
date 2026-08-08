"""Tablero (Streamlit) con los resultados del análisis y recomendaciones accionables."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
RUTA_SCORING = BASE_DIR.parent / "04_Resultados" / "scoring_final.csv"

st.set_page_config(page_title="App de Inversiones CREAN — Tablero", layout="wide")


@st.cache_data
def cargar_datos():
    return pd.read_csv(RUTA_SCORING)


scoring = cargar_datos()

st.title("App de Inversiones CREAN — Tablero de resultados")
st.markdown(
    "Resultado del análisis de propensión de adopción y monto potencial de inversión, "
    "para priorizar la estrategia de lanzamiento de la nueva App de inversiones."
)

tab_resumen, tab_exploracion, tab_prioritarios, tab_proceso = st.tabs(
    ["Resumen ejecutivo", "Exploración por segmento", "Clientes prioritarios", "Cómo funciona"]
)

# ---------------------------------------------------------------------------
with tab_resumen:
    clientes_esperados = scoring["probabilidad_adopcion"].sum()
    volumen_esperado = scoring["valor_esperado"].sum()
    total_clientes = len(scoring)

    col1, col2, col3 = st.columns(3)
    col1.metric("Clientes esperados que adoptarían", f"{clientes_esperados:,.0f}")
    col2.metric("Volumen esperado en 12 meses", f"${volumen_esperado:,.0f}")
    col3.metric("% de la base total", f"{100 * clientes_esperados / total_clientes:.1f}%")

    st.markdown("---")

    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("Volumen esperado por segmento")
        por_segmento = (
            scoring.groupby("desc_segmento")
            .agg(clientes_esperados=("probabilidad_adopcion", "sum"),
                 volumen_esperado=("valor_esperado", "sum"))
            .sort_values("volumen_esperado", ascending=False)
            .reset_index()
        )
        fig_segmento = px.bar(
            por_segmento, x="desc_segmento", y="volumen_esperado",
            labels={"desc_segmento": "Segmento", "volumen_esperado": "Volumen esperado (pesos)"},
        )
        st.plotly_chart(fig_segmento, use_container_width=True)

    with col_der:
        st.subheader("Volumen esperado por grupo/arquetipo")
        por_grupo = (
            scoring.groupby("nombre_cluster")
            .agg(clientes_esperados=("probabilidad_adopcion", "sum"),
                 volumen_esperado=("valor_esperado", "sum"))
            .sort_values("volumen_esperado", ascending=False)
            .reset_index()
        )
        fig_grupo = px.bar(
            por_grupo, x="nombre_cluster", y="volumen_esperado",
            labels={"nombre_cluster": "Grupo", "volumen_esperado": "Volumen esperado (pesos)"},
        )
        st.plotly_chart(fig_grupo, use_container_width=True)

    st.markdown("---")
    st.subheader("Recomendaciones accionables")

    segmento_top = por_segmento.iloc[0]
    grupo_top = por_grupo.iloc[0]
    pct_volumen_top_segmento = 100 * segmento_top["volumen_esperado"] / volumen_esperado
    pct_clientes_top_segmento = 100 * segmento_top["clientes_esperados"] / clientes_esperados

    st.markdown(f"""
- **Priorizar el segmento {segmento_top['desc_segmento']} primero**: concentra el
  {pct_volumen_top_segmento:.0f}% del volumen esperado con solo el
  {pct_clientes_top_segmento:.0f}% de los clientes esperados — el mayor retorno por
  cliente contactado.
- **El grupo "{grupo_top['nombre_cluster']}" es la mayor oportunidad en volumen absoluto**:
  enfocar ahí la primera campaña de activación, antes de expandir a los demás grupos.
- **Usar la pestaña "Clientes prioritarios"** para obtener la lista concreta a entregar al
  equipo comercial en el primer ciclo de contacto.
""")

# ---------------------------------------------------------------------------
with tab_exploracion:
    st.subheader("Filtrar la base")

    segmentos_sel = st.multiselect(
        "Segmento", options=sorted(scoring["desc_segmento"].unique()),
        default=sorted(scoring["desc_segmento"].unique()),
    )
    grupos_sel = st.multiselect(
        "Grupo / arquetipo", options=sorted(scoring["nombre_cluster"].unique()),
        default=sorted(scoring["nombre_cluster"].unique()),
    )

    filtrado = scoring[
        scoring["desc_segmento"].isin(segmentos_sel) & scoring["nombre_cluster"].isin(grupos_sel)
    ]
    st.write(f"**{len(filtrado):,}** clientes en la selección actual")

    col_izq, col_der = st.columns(2)
    with col_izq:
        fig_prob = px.histogram(
            filtrado, x="probabilidad_adopcion", nbins=40,
            labels={"probabilidad_adopcion": "Probabilidad de adopción"},
            title="Distribución de la probabilidad de adopción",
        )
        st.plotly_chart(fig_prob, use_container_width=True)
    with col_der:
        fig_monto = px.histogram(
            filtrado, x="monto_potencial_estimado", nbins=40,
            labels={"monto_potencial_estimado": "Monto potencial estimado (pesos)"},
            title="Distribución del monto potencial estimado",
        )
        st.plotly_chart(fig_monto, use_container_width=True)

# ---------------------------------------------------------------------------
with tab_prioritarios:
    st.subheader("Lista de clientes prioritarios")
    st.markdown(
        "Ordenados por **valor esperado** (probabilidad de adopción × monto potencial "
        "estimado) — la lista que se entregaría al equipo comercial para el primer ciclo "
        "de contacto."
    )

    n_clientes = st.slider("Cuántos clientes mostrar", min_value=10, max_value=500, value=50, step=10)

    top_clientes = scoring.sort_values("valor_esperado", ascending=False).head(n_clientes)
    st.dataframe(top_clientes, use_container_width=True)

    csv_descarga = top_clientes.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Descargar esta lista (CSV)", data=csv_descarga,
        file_name="clientes_prioritarios.csv", mime="text/csv",
    )

# ---------------------------------------------------------------------------
with tab_proceso:
    st.subheader("Cómo esta solución se conecta con CREAN")
    st.markdown(
        "El detalle completo (actores, flujos de información, puntos de decisión) está "
        "documentado en `06_Documentacion/modelo_conceptual_y_procesos.md`. Resumen del "
        "flujo:"
    )

    diagrama = """
    digraph G {
        rankdir=TD;
        node [shape=box, style=filled, fillcolor="#e8eef7"];

        Fuentes [label="7 fuentes de datos"];
        C360 [label="Cliente 360"];
        M1 [label="Modelo de propension"];
        M2 [label="Segmentacion (arquetipos)"];
        M3 [label="Modelo de monto potencial"];
        SF [label="scoring_final.csv"];
        TB [label="Tablero"];
        A1 [label="Equipo comercial"];
        A2 [label="Equipo de producto / finanzas"];
        A3 [label="Equipo CREAN"];

        Fuentes -> C360;
        C360 -> M1;
        C360 -> M2;
        C360 -> M3;
        M1 -> SF;
        M2 -> SF;
        M3 -> SF;
        SF -> TB;
        TB -> A1;
        TB -> A2;
        TB -> A3;
        A1 -> "Afiliar al servicio";
        A2 -> "Gestionar ingresos y gastos";
        A3 -> "Monitorear el servicio";
    }
    """
    st.graphviz_chart(diagrama)

    st.markdown("""
| Actor | Qué recibe | Qué decide |
|---|---|---|
| Equipo comercial | Lista de clientes priorizados (pestaña anterior) | A quién contactar primero |
| Equipo de producto / finanzas | Dimensionamiento agregado (pestaña "Resumen ejecutivo") | Proyección de impacto e ingresos |
| Equipo CREAN | Resultados y su evolución en el tiempo | Cuándo reentrenar o ajustar supuestos |
""")
