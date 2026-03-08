from haversine import haversine
import plotly.express as px
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import os
from sidebar import create_sidebar

st.set_page_config(
    page_title='Countries',
    page_icon='🌎',
    layout='wide'
)

# ===========================================================================
#Importar os dados
# ===========================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
df1 = pd.read_csv(os.path.join(current_dir, '..\\dataset', 'zomato_cleaned.csv'))

# ===========================================================================
#Funções
# ===========================================================================

def rest_per_contry(df1):
    df_aux = df1.loc[:, ['country_code', 'restaurant_id']].groupby('country_code').nunique().sort_values(by='restaurant_id', ascending=False).reset_index()
    fig = px.bar(df_aux, x='country_code',y='restaurant_id',text_auto=True,labels={'country_code':'Países','restaurant_id':'Quantidade de Restaurantes'},title='Quantidade de Restaurantes Registrados por País')
    return fig


def cities_per_contry(df1):
    df_aux = df1.loc[:, ['country_code', 'city']].groupby('country_code').nunique().sort_values(by='city', ascending=False).reset_index()
    fig = px.bar(df_aux, x='country_code',y='city',text_auto=True,labels={'country_code':'Países','city':'Quantidade de Cidades'},title='Quantidade de Cidades Registradas por País')
    return fig


def votes_per_contry(df1):
    df_aux = df1.loc[:, ['country_code', 'votes']].groupby('country_code').mean().sort_values(by='votes', ascending=False).reset_index().round(2)
    fig = px.bar(df_aux, x='country_code',y='votes',text_auto=True,labels={'country_code':'Países','votes':'Quantidade de Avaliações'},title='Média de Avaliações feitas por País')
    return fig


def average_cost_per_country(df1):
    df_aux = df1.loc[:, ['country_code', 'average_cost_for_two']].groupby('country_code').mean().sort_values(by='average_cost_for_two', ascending=False).reset_index().round(2)
    fig = px.bar(df_aux, x='country_code',y='average_cost_for_two',text_auto=True,labels={'country_code':'Países','average_cost_for_two':'Preço de prato para duas Pessoas'},title='Média do Preço de um prato para duas pessoas por País')
    return fig

# --------------------- Início da Estrutura Lógica do Código ---------------

# ===========================================================================
#Barra lateral
# ===========================================================================
filters = create_sidebar(df1, page='countries')
df1 = df1[df1['country_code'].isin(filters['country_fil'])]

# ===========================================================================
#Layout no Streamlit
# ===========================================================================
st.markdown('# 🌎 Visão Países')

with st.container():
    fig = rest_per_contry(df1)
    st.plotly_chart(fig,use_container_width=True,theme=None)

with st.container():
    fig = cities_per_contry(df1)
    st.plotly_chart(fig,use_container_width=True,theme=None)


with st.container():
    col1, col2 = st.columns(2)
    with col1:
        fig = votes_per_contry(df1)
        st.plotly_chart(fig,use_container_width=True,theme=None)

    with col2:
        fig = average_cost_per_country(df1)
        st.plotly_chart(fig,use_container_width=True,theme=None)
