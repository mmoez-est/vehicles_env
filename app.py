import pandas as pd
import plotly.express as px
import streamlit as st

#### IMPORTAR Y PREPARAR LA BASE DE DATOS ####

# Leer los datos del archivo CSV
car_data = pd.read_csv('vehicles_us.csv')

# Aislar los manufacturadores desde la variable de modelo

car_data["manufacturer"] = car_data["model"].str.split().str[0]

# Hacer una versión del DataFrame con los manufacturadores que aparecen más de 1000 veces

conteo_manuf = car_data['manufacturer'].value_counts(ascending=True)

frecuentes_manuf = conteo_manuf[conteo_manuf > 1000].index

manuf_1000 = car_data[car_data['manufacturer'].isin(frecuentes_manuf)]

# Hacer un DataFrame que contabilice las apariciones de modelo por tipo y manufacturador

conteo_modelo = car_data.groupby(['manufacturer', 'type'], as_index=False)['model'].count()

#### COMENZAR CON LA PRESENTACIÓN DE LOS DATOS ####

### Mostrar el título de la página
st.title("Presentación de datos venta automóbiles")

## Mostrar header y tabla de datos

st.header("Visor de Datos")

# Hacer checkbox para incluír todos los datos de los manufacturadores con menos de 1000 apariciones
# Si no, mostrar el DataFrame 'car_data'

include_all_manuf = st.checkbox('Incluir manufacturadores con menos de 1000 apariciones')

if include_all_manuf:
    st.dataframe(car_data.iloc[:, :-1])
else:
    st.dataframe(manuf_1000.iloc[:, :-1])

# Colocar un divisor entre la tabla y los gráficos para mayor claridad

st.divider()

## Mostrar header del gráfico tipo Long Format Data

st.header("Tipos de vehículos por manufacturadores")

# Crear un botón en la aplicación Streamlit

LFD_button = st.button('Construir gráfico')

# Cuando se hace clic en el botón se muestra el gráfico

if LFD_button:

    st.write('Creación de un gráfico para el conjunto de datos de anuncios de venta de coches')

    # Crear un Gráfico Long Format Data con px
    
    fig = px.bar(conteo_modelo, x="manufacturer", y="model", color="type", title="Tipo de vehículo por manufacturador")

    # Mostrar el gráfico Plotly interactivo en la aplicación Streamlit
    # 'use_container_width=True' ajusta el ancho del gráfico al contenedor

    st.plotly_chart(fig, use_container_width=True)

## Crear header para histograma condition vs model year

st.header("Condición del auto vs el año del modelo")

# Crear botón

hist_button = st.button('Construir histograma')

if hist_button:

    st.write('Creación de un histograma para el conjunto de datos de anuncios de venta de coches')
    
    # Crear un histograma
     
    fig = px.histogram(car_data, x='model_year', color='condition',title='Histograma de condición vs año del modelo')

    # Mostrar el histograma Plotly en Streamlit

    st.plotly_chart(fig, use_container_width=True)

## Crear header para histograma comparativo de precios por manufacturador

st.header("Comparación de distribución de precios entre manufacturadores")

# Aislar los manufacturadores

unique_manuf = car_data['manufacturer'].unique()

# Hacer dos cajas de selección para elegir los manufacturadores a mostrar

opcion_1 = st.selectbox(
    "Selecciona el manufacturador 1",
    (unique_manuf),
    index=None,
    placeholder="Selecciona el primer manufacturador",
)

opcion_2 = st.selectbox(
    "Selecciona el manufacturador 2",
    (unique_manuf),
    index=None,
    placeholder="Selecciona el segundo manufacturador",
)

# Hacer un DataFrame que solo incluya los dos manufacturadores seleccionados

comparacion_manuf = car_data[car_data['manufacturer'].isin([opcion_1, opcion_2])]

# Crear histograma normalizado e histograma normal

fig_2 = px.histogram(x=comparacion_manuf['price'], histnorm="percent", color=comparacion_manuf['manufacturer'], title="Histograma normalizado de distribución de precios entre manufacturadores", labels={'x':'price'})

fig_3 = px.histogram(x=comparacion_manuf['price'], color=comparacion_manuf['manufacturer'], title="Histograma de distribución de precios entre manufacturadores", labels={'x':'price'})


# Hacer checkbox para normalizar el histograma

norm_hist = st.checkbox("Normalizar histograma")

if norm_hist:
    st.plotly_chart(fig_2, use_container_width=True)
else:
    st.plotly_chart(fig_3, use_container_width=True)

## Crear header para gráfico de dispersión

st.header("Interacción entre kilometraje del auto, año del modelo y condición de este")

#Definición del orden y los colores a mostrar como condición

condition_order = ['new','like new','excellent','good','fair','salvage']
condition_color = {'new':'blue','like new':'turquoise','excellent':'green','good':'gold','fair':'orange','salvage':'red'}

# Crear botón

dispersion_button = st.button('Crear gráfico de dispersión')

if dispersion_button:
    # Crear el gráfico

    fig_4 = px.scatter(car_data, x="model_year", y="odometer", color="condition",title="Gráfico de dispersión sobre la relación entre el odómetro, el año del auto y su estado", category_orders={'condition':condition_order}, color_discrete_map=condition_color)
    
    # Mostrar el gráfico en Streamlit
    
    st.plotly_chart(fig_4)
    
# Crear un divisor para dar término a la página

st.divider()