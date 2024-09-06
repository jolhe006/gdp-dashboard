import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go

# Título del Dashboard
st.title("Dashboard de Rendimiento de Ventas")

# Leer los datos desde los archivos CSV en la carpeta "data"
# Asegúrate de que los archivos están en la carpeta "data"
ventas_file = 'data/ventas.csv'
correlaciones_file = 'data/correlaciones.csv'

# Cargar los datos
try:
    ventas_df = pd.read_csv(ventas_file)
    precios_df = pd.read_csv(precios_file)

    # Corregir los nombres de las columnas
    ventas_df.columns = ['datetime', 'day_of_week', 'total', 'place', 'angbutter', 'plain_bread', 
                         'jam', 'americano', 'croissant', 'caffe_latte', 'espresso', 
                         'tiramisu_croissant', 'gateau_chocolat', 'pandoro', 'cheese_cake',
                         'lemon_ade', 'orange_pound', 'wiener', 'vanilla_latte', 
                         'berry_ade', 'tiramisu', 'meringue_cookies']
    
    precios_df.columns = ['Product', 'Price']
    
    st.success("Datos cargados correctamente.")
except FileNotFoundError:
    st.error(f"No se encontró el archivo {ventas_file} o {precios_file}. Asegúrate de que los archivos están en la carpeta data.")
    st.stop()

# Convertir los datos relevantes
ventas_df['datetime'] = pd.to_datetime(ventas_df['datetime'])
weekly_sales_new = ventas_df.groupby(pd.Grouper(key='datetime', freq='W'))['total'].sum()

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

daily_sales_deviation_new = ventas_df.set_index('datetime').resample('D').sum()['total'] - ventas_df['total'].mean()

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
total_holiday_sales = ventas_df[ventas_df['day_of_week'].isin(['Sun', 'Sat'])]['total'].sum()
non_holiday_sales = ventas_df[~ventas_df['day_of_week'].isin(['Sun', 'Sat'])]['total'].sum()

labels = ['Ventas en Días Festivos', 'Ventas en Días No Festivos']
sales_data = [total_holiday_sales, non_holiday_sales]

fig3 = go.Figure(data=[go.Pie(labels=labels, values=sales_data, hole=.3)])
fig3.update_layout(title="Ventas en Días Festivos vs Días No Festivos")
st.plotly_chart(fig3)

# Sección 4: Mapa de Calor de Correlaciones entre Productos
st.subheader("Mapa de Calor de Correlaciones entre Productos")

# Crear un DataFrame con las correlaciones simuladas de los productos
correlaciones_df = ventas_df[['angbutter', 'plain_bread', 'croissant', 'espresso', 'tiramisu']].corr()

fig4, ax4 = plt.subplots()
sns.heatmap(correlaciones_df, annot=True, cmap='coolwarm', ax=ax4)
ax4.set_title("Correlaciones entre Productos")
st.pyplot(fig4)

# Conclusión final
st.write("Este dashboard interactivo muestra el rendimiento de ventas en el Supermercado Alan. "
         "Proporciona información sobre las tendencias de ventas, desviaciones diarias, impacto de los días festivos "
         "y las correlaciones entre productos.")

