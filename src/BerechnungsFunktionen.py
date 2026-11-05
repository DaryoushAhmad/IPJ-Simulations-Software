import pandas as pd
import plotly.express as px
from DataFunktionen import setUpGesamtcsv, setUpJahresStatistikcsv

def haeufigkeitsverteilung_EE():

    dfGesamt = setUpGesamtcsv()

    ee_intervallgrenzen = list(range(0, 170, 10))

    dfGesamt["EE_Intervall"] = pd.cut(dfGesamt["EE_Anteil"], bins=ee_intervallgrenzen, include_lowest=True)
    dfGesamt["EE_Intervall_Label"]=dfGesamt["EE_Intervall"].apply(lambda interval: f"{int(interval.left)}-{int(interval.right)}")

    #Neu Gruppieren
    kategorien=[f"{l}-{r}" for l, r in zip(ee_intervallgrenzen[:-1],ee_intervallgrenzen[1:])]
    dfGesamt["EE_Intervall_Label"]=pd.Categorical(dfGesamt["EE_Intervall_Label"], categories=kategorien,ordered=True)

    #mit Observed=False wird auch Bereich 0-10 betrachtet
    grouped=dfGesamt.groupby("EE_Intervall_Label", observed=False).size()

    fig = px.bar(
        x=grouped.index.astype(str),
        y=grouped.values
    )

    # Diagramm mit einem Titel und Achsenbeschriftungen versehen
    fig.update_layout(
        title="Häufigkeitsverteilung der EE-Anteile (2020-2026)",
        xaxis_title="Anteil erneuerbarer Energien [%]",
        yaxis_title="Anzahl der Viertelstunden"
    )

    fig.show()