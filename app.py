import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Statystyki roczników GUS",
                   page_icon=":chart_with_downwards_trend:", layout="wide")

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

# sidebar
st.sidebar.header("Filtruj:")
year = st.sidebar.multiselect(
    "Wybierz Rok:", options=df["Rok"].unique(), default=[2022])
age = st.sidebar.multiselect(
    "Wybierz Wiek:", options=df["Wiek"].unique(), default=df["Wiek"][21:23])
#slider_range = st.sidebar.slider("Wybierz zakres:", value=[0, 100])
# print(slider)

df_selection = df.query("Rok == @year & Wiek == @age")


# main page
st.title(":bar_chart: Statystyki roczników - GUS")
st.markdown("##")

total = int(df_selection["Ogółem"].sum())
men = int(df_selection["Mężczyźni"].sum())
women = int(df_selection["Kobiety"].sum())

left_col, middle_col, right_col = st.columns(3)
with left_col:
    st.subheader("Ogółem:")
    st.subheader(total)
with middle_col:
    st.subheader("Mężczyźni:")
    st.subheader(men)
with right_col:
    st.subheader("Kobiety:")
    st.subheader(women)

st.markdown("---")

st.dataframe(df_selection)
