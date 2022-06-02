import pandas as pd
# import plotly.express as px
# import streamlit as st

# st.set_page_config(page_title="Statystyki roczników GUS",
#                    page_icon=":chart_with_downwards_trend:", layout="wide")

# load file
df = pd.read_excel(io="data.xls", sheet_name="roczniki",
                   skiprows=3, usecols='A:E', )

cols = [col for col in df if col != 'Ogółem'] + ["Ogółem"]
df = df[cols]


# rename 1st two columns
df.rename(columns={'Unnamed: 0': 'Rok', 'Unnamed: 1': 'Wiek'}, inplace=True)


# remove NaN and covnerting cols to integers
df['Rok'] = df['Rok'].fillna(0)
df = df.astype({"Rok": "int", "Ogółem": "int",
               "Mężczyźni": "int", "Kobiety": "int"})


# insertion of years
def set_years():
    temp = 0
    for x in range(3876):
        if df['Rok'][x] != 0:
            temp = df['Rok'][x]
        else:
            df.iloc[[x], [0]] = temp


set_years()
print(df)

