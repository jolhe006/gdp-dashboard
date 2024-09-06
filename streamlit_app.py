import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go

# Título del Dashboard
st.title("Dashboard de Rendimiento de Ventas del Supermercado Alan")

# Leer los datos desde los archivos CSV en la carpeta "data"
# Asegúrate de que los archivos están en la carpeta "data"
ventas_file = 'data/ventas.csv'
correlaciones_file = 'data/correlaciones.csv'

# Cargar los datos
try:
    ventas_df = pd.read_csv(ventas_file)
    correlaciones_df = pd.read_csv(correlaciones_file)
    
    st.success("Datos cargados correctamente.")
except FileNotFoundError:
    st.error(f"No se encontró el archivo {ventas_file} o {correlaciones_file}. Asegúrate de que los archivos están en la carpeta data.")
    st.stop()

# Convertir los datos relevantes
ventas_df['Fecha'] = pd.to_datetime(ventas_df['Fecha'])
weekly_sales_new = ventas_df.groupby(pd.Grouper(key='Fecha', freq='W'))['Ventas'].sum()

# Sección 1: Tendencias de Ventas Semanales
st.subheader("Tendencias de Ventas Semanales")

fig1, ax1 = plt.subplots()
ax1.plot(weekly_sales_new.index, weekly_sales_new.values, marker='o', label='Ventas Semanales')
z = np.polyfit(np.arange(len(weekly_sales_new)), weekly_sales_new.values, 1)
p = np.poly1d(z)
ax1.plot(weekly_sales_new.index, p(np.arange(len(weekly_sales_new))), "r--", label='Tendencia')
ax1.set_xlabel("Fecha")
ax1.set_ylabel("Monto de Ventas")
ax1.set_title("Ventas Semanales con Línea de Tendencia")
ax1.legend()
st.pyplot(fig1)

# Sección 2: Desviaciones en las Ventas Diarias
st.subheader("Desviaciones en las Ventas Diarias")

daily_sales_deviation_new = ventas_df.set_index('Fecha').resample('D').sum()['Ventas'] - ventas_df['Ventas'].mean()

fig2, ax2 = plt.subplots()
colors_new = ['green' if val > 0 else 'red' for val in daily_sales_deviation_new]
ax2.bar(daily_sales_deviation_new.index, daily_sales_deviation_new.values, color=colors_new)
ax2.axhline(0, color='black', linewidth=0.8)
ax2.set_xlabel("Fecha")
ax2.set_ylabel("Desviación de la Media")
ax2.set_title("Desviaciones en las Ventas Diarias")
st.pyplot(fig2)

# Sección 3: Comparación de Ventas en Días Festivos vs No Festivos
st.subheader("Distribución de Ventas: Días Festivos vs No Festivos")

# Suponemos que el CSV incluye una columna 'EsFestivo' que indica si el día es festivo (1) o no (0)
total_holiday_sales = ventas_df[ventas_df['EsFestivo'] == 1]['Ventas'].sum()
non_holiday_sales = ventas_df[ventas_df['EsFestivo'] == 0]['Ventas'].sum()

labels = ['Ventas en Días Festivos', 'Ventas en Días No Festivos']
sales_data = [total_holiday_sales, non_holiday_sales]

fig3 = go.Figure(data=[go.Pie(labels=labels, values=sales_data, hole=.3)])
fig3.update_layout(title="Ventas en Días Festivos vs Días No Festivos")
st.plotly_chart(fig3)

# Sección 4: Mapa de Calor de Correlaciones entre Productos
st.subheader("Mapa de Calor de Correlaciones entre Productos")

# Leer el archivo de correlaciones y mostrar el heatmap
fig4, ax4 = plt.subplots()
sns.heatmap(correlaciones_df, annot=True, cmap='coolwarm', ax=ax4)
ax4.set_title("Correlaciones entre Productos")
st.pyplot(fig4)

# Conclusión final
st.write("Este dashboard interactivo muestra el rendimiento de ventas en el Supermercado Alan. "
         "Proporciona información sobre las tendencias de ventas, desviaciones diarias, impacto de los días festivos "
         "y las correlaciones entre productos.")
