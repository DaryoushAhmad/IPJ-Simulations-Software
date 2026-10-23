import pandas as pd
import plotly.express as px
from DataFunktionen import setUpGesamtcsv, setUpJahresStatistikcsv

def haeufigkeitsverteilung_EE():

    dfGesamt = setUpGesamtcsv()

    ee_intervallgrenzen = list(range(0, 170, 10))

    dfGesamt["EE_Intervall"] = pd.cut(dfGesamt["EE_Anteil"], bins=ee_intervallgrenzen, include_lowest=True)

    EE_Intervall_Haeufigkeit = dfGesamt["EE_Intervall"].value_counts(sort=False)

    fig = px.bar(
        x=EE_Intervall_Haeufigkeit.index.astype(str),
        y=EE_Intervall_Haeufigkeit.values
    )

    # Diagramm mit einem Titel und Achsenbeschriftungen versehen
    fig.update_layout(
        title="Häufigkeitsverteilung der EE-Anteile (2020-2026)",
        xaxis_title="Anteil erneuerbarer Energien [%]",
        yaxis_title="Anzahl der Viertelstunden"
    )

    fig.show()