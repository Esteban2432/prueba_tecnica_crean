"""Funciones compartidas entre notebooks: carga de datos y limpieza."""

import sqlite3
import pandas as pd


def cargar_tabla(ruta_db, nombre_tabla):
    """
    Carga una tabla completa de una base de datos SQLite como un DataFrame de pandas.

    ruta_db: ruta al archivo .db (ej. '../02_Datos/clientes/clientes.db')
    nombre_tabla: nombre de la tabla dentro de esa base (ej. 'clientes')
    """
    conexion = sqlite3.connect(ruta_db)
    df = pd.read_sql(f"SELECT * FROM {nombre_tabla}", conexion)
    conexion.close()
    return df


def ultimo_saldo_por_cliente(ruta_db, nombre_tabla):
    """
    Para cada cliente, devuelve su saldo mas reciente conocido en esta tabla de producto.

    Se usa esta funcion (en vez de sumar o promediar todos los registros) porque las
    tablas de producto no se midieron con la misma frecuencia entre si: algunas traen
    casi una foto diaria y otras una foto mensual (ver notebook 00, seccion 6). Tomar
    solo el ultimo saldo conocido deja a todos los productos medidos con la misma vara.
    """
    df = cargar_tabla(ruta_db, nombre_tabla)
    df = df.sort_values('fecha')
    ultimo = df.groupby('numero_id').last()['saldo']
    return ultimo.rename('saldo')
