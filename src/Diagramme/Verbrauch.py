import pandas as pd
import plotly.express as px

dfGesamt = pd.read_csv(
    "data/bereinigt/SMARD_Gesamt_Bereinigt.csv",
    sep=";",    
    decimal=",",    #Pandas erklären das es ein Dezimalzeichen ist
    thousands=".",   #Pandas erklären das es ein 1000 Zeichen
    na_values=["-"]
)
dfGesamt["Datum von"] = pd.to_datetime(
dfGesamt["Datum von"],
format="%d.%m.%Y %H:%M"
)

dfGesamt["Datum bis"] = pd.to_datetime(
dfGesamt["Datum bis"],
format="%d.%m.%Y %H:%M"
)   


dfJahresStatistik = pd.read_csv(
    "data/bereinigt/SMARD_Jahresstatistik.csv",
    sep=";",    
    decimal=",",    #Pandas erklären das es ein Dezimalzeichen ist
    thousands=".",   #Pandas erklären das es ein 1000 Zeichen
    na_values=["-"]
)

# Die Jahresstatistik enthält bereits die Summe des Verbrauchs je Jahr.
dfJahresStatistik = dfJahresStatistik.sort_values("Datum von")
dfJahresStatistik["Jahr"] = dfJahresStatistik["Datum von"].astype(str)
dfJahresStatistik["Verbrauch [TWh]"] = (
    dfJahresStatistik["Netzlast [MWh] Originalauflösungen"] / 1000000
)

# Unvollständige Jahre anhand der Anzahl der Viertelstunden kennzeichnen.
jahresbeginn = pd.to_datetime(dfJahresStatistik["Jahr"], format="%Y")
erwarteteViertelstunden = (365 + jahresbeginn.dt.is_leap_year.astype(int)) * 96
dfJahresStatistik["Datenstand"] = "Vollständiges Jahr"
dfJahresStatistik.loc[
    dfJahresStatistik["Anzahl_Viertelstunden"] < erwarteteViertelstunden,
    "Datenstand",
] = "Unvollständiges Jahr"

diagramm = px.bar(
    dfJahresStatistik,
    x="Jahr",
    y="Verbrauch [TWh]",
    color="Datenstand",
    text="Verbrauch [TWh]",
    title="Stromverbrauch je Jahr (Netzlast)",
    color_discrete_map={
        "Vollständiges Jahr": "#2563eb",
        "Unvollständiges Jahr": "#f59e0b",
    },
)
diagramm.update_traces(texttemplate="%{y:.1f}", textposition="outside")
diagramm.update_layout(
    xaxis_type="category",
    template="plotly_white",
    yaxis_rangemode="tozero",
)

# Das interaktive Diagramm im Browser öffnen.
diagramm.show(renderer="browser")
