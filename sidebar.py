from warnings import filters

import pandas as pd
import streamlit as st
from PIL import Image
import os

# ===========================================================================
#Importar os dados
# ===========================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
df1 = pd.read_csv(os.path.join(current_dir, 'dataset', 'zomato_cleaned.csv'))

# ===========================================================================
#Barra lateral
# ===========================================================================
def create_sidebar(df1, page='main'):

    image = Image.open('logo.png')

    col1, col2 = st.sidebar.columns([1, 2])
    with col1:
        st.image(image, width=60)
    with col2:
        st.markdown('# Fome Zero')

    # Filtro de países aparece em todas as páginas
    countries = df1['country_code'].unique()
    country_fil = st.sidebar.multiselect(
        'Escolha os Países que Deseja visualizar as informações',
        countries,
        default=countries
    )

    # Filtros exclusivos da página cuisines
    if page == 'cuisines':
        top_rest_slider = st.sidebar.slider(
            'Selecione a quantidade de Restaurantes que deseja visualizar',
            value=10,
            min_value=1,
            max_value=20
        )
        cuisines = df1['cuisines'].unique()
        cuisines_fil = st.sidebar.multiselect(
            'Escolha os Tipos de Culinária',
            cuisines,
            default=cuisines
        )

    # Download só na main
    if page == 'main':
        st.sidebar.markdown("""---""")
        st.sidebar.markdown('## Dados Tratados')
        st.sidebar.download_button(
            label='📥 Download',
            data=df1.to_csv(index=False).encode('utf-8'),
            file_name='zomato_cleaned.csv',
            mime='text/csv'
        )

    # Monta o dicionário de retorno de acordo com a página
    filters = {'country_fil': country_fil}

    if page == 'cuisines':
        filters['cuisines_fil'] = cuisines_fil
        filters['top_rest_slider'] = top_rest_slider

    return filters
