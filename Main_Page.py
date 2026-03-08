from haversine import haversine
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium
import os
from sidebar import create_sidebar

st.set_page_config(
    page_title='Main Page',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state="expanded"
)

# ===========================================================================
#Importar os dados
# ===========================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
df1 = pd.read_csv(os.path.join(current_dir, 'dataset', 'zomato_cleaned.csv'))

# ===========================================================================
#Funções
# ===========================================================================
def ajuste_votes(df1):
    df_aux = df1['votes'].sum()
    df_aux = f'{df_aux:,.0f}'
    df_aux = df_aux.replace(',','.')
    return df_aux


def restaurantes_map(df1):
    df_aux = df1.loc[:,['restaurant_name','average_cost_for_two','currency','aggregate_rating','country_code','city','cuisines','latitude','longitude']]
    map = folium.Map(location=[0, 0],zoom_start=2)
    marker_cluster = folium.plugins.MarkerCluster().add_to(map)
    for index,location in df_aux.iterrows():
        folium.Marker([location['latitude'],location['longitude']],
                    popup=folium.Popup(f'''<h6><b>{location['restaurant_name']}</b></h6>
                    <h6>Preço: {location['average_cost_for_two']} ({location['currency']}) para dois <br>
                    Culinária: {location['cuisines']} <br>
                    Avaliação: {location['aggregate_rating']}/5.0</h6>''',
                    max_width=300,min_width=150),
                    tooltip=location["restaurant_name"],
                    icon=folium.Icon(color='green', icon='home', prefix='fa')).add_to(marker_cluster)

    folium_static(map,width=1024,height=600)



# --------------------- Início da Estrutura Lógica do Código ---------------


# ===========================================================================
#Barra lateral
# ===========================================================================
filters = create_sidebar(df1, page='main')
df1 = df1[df1['country_code'].isin(filters['country_fil'])]

# ===========================================================================
#Layout no Streamlit
# ===========================================================================
st.markdown('# Fome Zero!')
st.markdown('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')

#container dividio em 5 colunas
with st.container():
    st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        df_aux = df1['restaurant_id'].nunique()
        col1.metric('Restaurantes Cadastrados',df_aux)

    with col2:
        df_aux = df1['country_code'].nunique()
        col2.metric('Países Cadastrados',df_aux)

    with col3:
        df_aux = df1['city'].nunique()
        col3.metric('Cidades Cadastrados',df_aux)

    with col4:
        df_aux = ajuste_votes(df1)
        col4.metric('Avaliações Feitas na Plataforma',df_aux)

    with col5:
        df_aux = df1['cuisines'].nunique()
        col5.metric('Tipos de Culinárias Oferecidas',df_aux)


#mapa de restaurantes por localidade
with st.container():
    restaurantes_map(df1)
