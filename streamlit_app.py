import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Título de la app
st.title("Análisis de Ventas del Supermercado Alan")

# Cargar los datos
data = {'Producto': ['A', 'B', 'C'], 'Ventas': [100, 200, 150]}
df = pd.DataFrame(data)

# Mostrar una tabla de datos
st.write("Tabla de ventas:")
st.dataframe(df)

# Graficar
st.write("Gráfico de ventas:")
plt.bar(df['Producto'], df['Ventas'])
st.pyplot(plt)
