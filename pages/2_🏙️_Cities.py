from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import os
from sidebar import create_sidebar

st.set_page_config(
    page_title='Cities',
    page_icon='🏙️',
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
def top10_cities(df1):
    df_aux = df1.loc[:, ['country_code','city', 'restaurant_id']].groupby(['city', 'country_code']).nunique().sort_values(by='restaurant_id', ascending=False).reset_index()
    fig = px.bar(df_aux.head(10), x='city',y='restaurant_id',text_auto=True,labels={'city':'Cidade','restaurant_id':'Quantidade de Restaurantes','country_code':'País',},color='country_code',title='Top 10 Cidades com mais Restaurantes na Base de Dados')
    return fig



def top7_rest_up4(df1):
    df_aux = df1.loc[:,['country_code','city','aggregate_rating','restaurant_id']].groupby(['country_code','city','restaurant_id']).mean().sort_values(by=['restaurant_id','city'],ascending=[False,True]).reset_index()
    df_aux = df_aux.loc[df_aux['aggregate_rating'] >= 4,['country_code','city','restaurant_id']].groupby(['country_code','city']).count().sort_values(by=['restaurant_id','city'],ascending=[False,True]).reset_index()
    fig = px.bar(df_aux.head(7), x='city',y='restaurant_id',text_auto=True,labels={'city':'Cidade','restaurant_id':'Quantidade de Restaurantes','country_code':'País'},color='country_code',title='Top 7 Cidades com Restaurantes com média de avaliação acima de 4')
    return fig


def top7_rest_down2_5(df1):
    df_aux = df1.loc[:,['country_code','city','aggregate_rating','restaurant_id']].groupby(['country_code','city','restaurant_id']).mean().sort_values(by=['restaurant_id','city'],ascending=[False,True]).reset_index()
    df_aux = df_aux.loc[df_aux['aggregate_rating'] <= 2.5,['country_code','city','restaurant_id']].groupby(['country_code','city']).count().sort_values(by=['restaurant_id','city'],ascending=[False,True]).reset_index()
    fig = px.bar(df_aux.head(7), x='city',y='restaurant_id',text_auto=True,labels={'city':'Cidade','restaurant_id':'Quantidade de Restaurantes','country_code':'País'},color='country_code',title='Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5')
    return fig


def top10_cuisines(df1):
    df_aux = df1.loc[:,['country_code','city','cuisines','restaurant_id']].groupby(['country_code','city','cuisines']).count().sort_values(by=['restaurant_id'],ascending=[False]).reset_index()
    df_aux = df_aux.loc[:,['country_code','city','cuisines']].groupby(['country_code','city']).count().sort_values(by=['cuisines','city','country_code'],ascending=[False,True,True]).reset_index()
    fig = px.bar(df_aux.head(10), x='city',y='cuisines',text_auto=True,labels={'city':'Cidade','cuisines':'Quantidade de Tipos Culinários Únicos','country_code':'País'},color='country_code',title='Top 10 Cidades mais restaurantes com tipos culinários distintos')
    return fig


# --------------------- Início da Estrutura Lógica do Código ---------------

# ===========================================================================
#Barra lateral
# ===========================================================================
filters = create_sidebar(df1, page='cities')
df1 = df1[df1['country_code'].isin(filters['country_fil'])]

# ===========================================================================
#Layout no Streamlit
# ===========================================================================
st.markdown('# 🏙️ Visão Cidades')

with st.container():
    fig = top10_cities(df1)
    st.plotly_chart(fig,use_container_width=True,theme=None)


with st.container():
    col1, col2 = st.columns(2)
    with col1:
        fig = top7_rest_up4(df1)
        st.plotly_chart(fig,use_container_width=True,theme=None)


    with col2:
        fig = top7_rest_down2_5(df1)
        st.plotly_chart(fig,use_container_width=True,theme=None)


with st.container():
    fig = top10_cuisines(df1)
    st.plotly_chart(fig,use_container_width=True,theme=None)
