from turtle import width
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

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
# print(df)

# sidebar
st.sidebar.header("Filtruj:")
year = st.sidebar.multiselect(
    "Wybierz Rok:", options=df["Rok"].unique(), default=[2025, 2026, 2027])
age = st.sidebar.multiselect(
    "Wybierz Wiek:", options=df["Wiek"].unique(), default=df["Wiek"][30:35])

df_selection = df.query("Rok == @year & Wiek == @age")

# main page
st.title(":bar_chart: Statystyki roczników - GUS")
st.markdown("##")

total = int(df_selection["Ogółem"].sum())
men = int(df_selection["Mężczyźni"].sum())
women = int(df_selection["Kobiety"].sum())

left_col, middle_col, right_col = st.columns(3)
with right_col:
    st.subheader("Ogółem:")
    st.subheader(total)
with left_col:
    st.subheader("Mężczyzn:")
    st.subheader(men)
with middle_col:
    st.subheader("Kobiet:")
    st.subheader(women)

st.markdown("---")

data = ['Mężczyźni', 'Kobiety', 'Ogółem']
mycolors = ["#6aa7d9", "#eb3e3b", "#88f793"]
fig = go.Figure([go.Bar(x=data, y=[men, women, total],
                text=df_selection[data].sum(), marker=dict(color=mycolors))])
st.plotly_chart(fig)

# print(df_selection["Kobiety"].sum())
