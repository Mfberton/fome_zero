import pandas as pd
import inflection
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(current_dir, 'zomato.csv'))
df1 = df.copy()

# Renomear as colunas do DataFrame
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

# Substituição dos códigos dos países pelos nomes dos países
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]

# Criação do Tipo de Categoria de Comida
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

# Criação do nome das Cores
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]


def clean_code(df1):
    # Dados do projeto
    df1 = rename_columns(df1)
    df1['country_code'] = df1.loc[:, 'country_code'].apply(lambda x: country_name(x))
    df1['price_range'] = df1.loc[:, 'price_range'].apply(lambda x: create_price_tye(x))
    df1['expressed_color'] = df1.loc[:, 'rating_color'].apply(lambda x: color_name(x))
    df1['cuisines'] = df1['cuisines'].astype(str)
    df1["cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

    #Limpeza dos dados
    df1 = df1.drop(labels=['switch_to_order_menu'], axis='columns')
    df1 = df1.loc[(df1['cuisines'] != 'nan'),:].copy()
    df1 = df1.loc[(df1['cuisines'] != 'Drinks Only'),:].copy()
    df1 = df1.loc[(df1['cuisines'] != 'Mineira'),:].copy()
    df1 = df1.drop_duplicates().reset_index(drop=True)
    return df1

df1 = clean_code(df1)
df1.to_csv(os.path.join(current_dir, 'zomato_cleaned.csv'), index=False)
