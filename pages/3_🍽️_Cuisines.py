from haversine import haversine
import plotly.express as px
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import os
from sidebar import create_sidebar

st.set_page_config(
    page_title='Cuisines',
    page_icon='🍽️',
    layout='wide'
)

# ===========================================================================
#Importar os dados
# ===========================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
df1 = pd.read_csv(os.path.join(current_dir, '..', 'dataset', 'zomato_cleaned.csv'))

# ===========================================================================
#Funções
# ===========================================================================
def cuisines_votes_restaurant(media, cuisine):
    df_aux = df1.loc[df1['cuisines'] == cuisine, ['restaurant_name', 'restaurant_id', 'aggregate_rating']].groupby(['restaurant_name', 'restaurant_id']).mean().sort_values(by='aggregate_rating', ascending=True).reset_index()

    # Verifica se há dados para a culinária selecionada
    if df_aux.empty:
        return None, None, None

    if media == 'maior':
        df_aux = df_aux.loc[df_aux['aggregate_rating'] == df_aux['aggregate_rating'].max(), ['restaurant_name', 'restaurant_id']].sort_values(by='restaurant_id', ascending=True)
    elif media == 'menor':
        df_aux = df_aux.loc[df_aux['aggregate_rating'] == df_aux['aggregate_rating'].min(), ['restaurant_name', 'restaurant_id']].sort_values(by='restaurant_id', ascending=True)
    else:
        print('Opção de média inválida. Por favor, escolha "maior" ou "menor".')
        return None, None, None

    restaurant_id = df_aux.iloc[0, 1]
    df_info = df1.loc[df1['restaurant_id'] == restaurant_id,
                      ['restaurant_name', 'country_code', 'city',
                       'average_cost_for_two', 'currency',
                       'cuisines', 'aggregate_rating']].iloc[0]

    label = f'{df_info["cuisines"]}: {df_info["restaurant_name"]}'
    value = f'{df_info["aggregate_rating"]}/5.0'
    ajuda = f'''País: {df_info["country_code"]}
Cidade: {df_info["city"]}
Média prato para dois: {df_info["average_cost_for_two"]} ({df_info["currency"]})'''

    return label, value, ajuda



def top_dataframe(df1):
    dataframe = df1.loc[df1['aggregate_rating'] == df1['aggregate_rating'].max(),['restaurant_id', 'restaurant_name', 'country_code', 'city','cuisines','average_cost_for_two','aggregate_rating','votes']].sort_values(by='restaurant_id',ascending=True)
    dataframe['restaurant_id'] = df1.loc[:, 'restaurant_id'].apply(lambda x: "{0:>20}".format(x))
    dataframe['votes'] = df1.loc[:, 'votes'].apply(lambda x: "{0:>20}".format(x))
    dataframe.columns = ['ID Restaurante', 'Nome do Restaurante', 'País', 'Cisade','Culinária','Média do preço de um prato para dois','Avaliação média','Qtde de votos']
    return dataframe






def bar_1(df1,data_slider):
    graf1 = df1.loc[:,['cuisines','aggregate_rating']].groupby(['cuisines']).mean().sort_values(by='aggregate_rating',ascending=False).reset_index().round(2)
    graf1 = px.bar(graf1.head(data_slider), x='cuisines',y='aggregate_rating',text_auto=True,labels={'cuisines':'Tipo de Culinária','aggregate_rating':'Média da Avaliação Média'},title=f'Top {data_slider} Melhores Tipos de Culiárias')
    return graf1


def bar_2(df1,data_slider):
    graf1 = df1.loc[:,['cuisines','aggregate_rating']].groupby(['cuisines']).mean().sort_values(by='aggregate_rating',ascending=True).reset_index().round(2)
    graf1 = px.bar(graf1.head(data_slider), x='cuisines',y='aggregate_rating',text_auto=True,labels={'cuisines':'Tipo de Culinária','aggregate_rating':'Média da Avaliação Média'},title=f'Top {data_slider} Piores Tipos de Culiárias')
    return graf1



# --------------------- Início da Estrutura Lógica do Código ---------------

# ===========================================================================
#Barra lateral
# ===========================================================================
filters = create_sidebar(df1, page='cuisines')
df1 = df1[df1['country_code'].isin(filters['country_fil'])]
df1 = df1[df1['cuisines'].isin(filters['cuisines_fil'])]
top_n = filters['top_rest_slider']

# ===========================================================================
#Layout no Streamlit
# ===========================================================================
st.markdown('# 🍽️ Visão Tipos de Culinárias')
st.markdown('## Melhores Restaurantes dos Principais tipos Culinários')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        label, value, ajuda = cuisines_votes_restaurant('maior', 'Italian')
        if label is not None:
            st.metric(label=label, value=value, help=ajuda)
        else:
            st.metric(label='Italian: N/A', value='N/A', help='Sem dados para os filtros selecionados')


    with col2:
        label, value, ajuda = cuisines_votes_restaurant('maior', 'American')
        if label is not None:
            st.metric(label=label, value=value, help=ajuda)
        else:
            st.metric(label='American: N/A', value='N/A', help='Sem dados para os filtros selecionados')

    with col3:
        label, value, ajuda = cuisines_votes_restaurant('maior', 'Arabian')
        if label is not None:
            st.metric(label=label, value=value, help=ajuda)
        else:
            st.metric(label='Arabian: N/A', value='N/A', help='Sem dados para os filtros selecionados')

    with col4:
        label, value, ajuda = cuisines_votes_restaurant('maior', 'Japanese')
        if label is not None:
            st.metric(label=label, value=value, help=ajuda)
        else:
            st.metric(label='Japanese: N/A', value='N/A', help='Sem dados para os filtros selecionados')

    with col5:
        label, value, ajuda = cuisines_votes_restaurant('maior', 'Home-made')
        if label is not None:
            st.metric(label=label, value=value, help=ajuda)
        else:
            st.metric(label='Home-made: N/A', value='N/A', help='Sem dados para os filtros selecionados')


with st.container():
    st.markdown(f'## Top {top_n} Restaurantes')
    dataframe = top_dataframe(df1)
    st.dataframe(dataframe.head(top_n))


with st.container():
    col1, col2 = st.columns(2)
    with col1:
        graf1 = bar_1(df1,top_n)
        st.plotly_chart(graf1,use_container_width=True,theme=None)

    with col2:
        graf1 = bar_2(df1,top_n)
        st.plotly_chart(graf1,use_container_width=True,theme=None)
