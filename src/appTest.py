#testsoftware zum UI
#verantwortlich: Kai

# start via: cd IPJ-Simulations-Software
# & "C:\Users\Kai Damerius\AppData\Local\Programs\Python\Python313\python.exe" -m streamlit run src/appTest.py


# bibliotheken ---------------------------------------------------------------------------------------------
import pandas as pd
import plotly.express as px
import streamlit as st
# ----------------------------------------------------------------------------------------------------------

# seitentitel und text
st.title("testtitel")
st.write("hello longus mongus")


# beispieldaten erstellen nur testweise
daten={
    "Jahr":[2020, 2021, 2022, 2023, 2024, 2025, 2026],
    "EE-Testanteil":[34.5, 33, 67, 31, 90, 54.7, 77.2],
    "Netzlast-Testanteil":[440, 450, 312, 900, 567, 123, 676]
    }
df=pd.DataFrame(daten)

# kachel bearbeiten
col1, col2=st.columns(2)
col1.metric(label="durchschnittl. EE-Anteil", value=f"{df['EE-Testanteil'].mean():.1f} %")
col2.metric(label="Aktueller EE-Anteil (2024)", value=f"{df['EE-Testanteil'].iloc[-1]} %", delta="+4.3 %")


# interaktives diagramm mit plotly
st.subheader("Entwicklung ee anteil")
fig=px.line(
    df,
    x="Jahr",
    y="EE-Testanteil",
    markers=True,
    labels={"EE-Testanteil": "EE-Anteil(%)", "Jahr": "Jahr"}
)

st.plotly_chart(fig, use_container_width=True)

# datentabelle anzeigen
st.subheader("Rohdaten")
st.dataframe(df)

