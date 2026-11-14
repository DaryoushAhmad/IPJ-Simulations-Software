import pandas as pd
import plotly.express as px
from DataFunktionen import setUpErzeugerProfil 

dfGesamt = setUpErzeugerProfil()


PV_Installiert = 118.111
windOnShore_Installiert = 68.179
windOffShore_Installiert = 9.733

PV_Prognose = 2
windOn_Prognose = 2
windOff_Prognose = 2

# 2,5 da man es wieder in MWh umrechnen muss, da sie vorher in viertelstundenwerte umgerechnet wurden.
dfGesamt["EE_Erzeugung"] = ((dfGesamt["PV"] * PV_Installiert * PV_Prognose) + (dfGesamt["Wind Onshore"] * windOnShore_Installiert * windOn_Prognose) + (dfGesamt["Wind Offshore"] * windOffShore_Installiert * windOff_Prognose)) * 2.5

dfGesamt["EE_Anteil"] = dfGesamt["EE_Erzeugung"]/dfGesamt["Verbrauch 2025 [MWh]"] * 100

#wenn Mittel über 100% ist heißt das nicht das der komplette verbrauch durch EE gedeckt ist
EE_Anteil_Mittel = dfGesamt["EE_Anteil"].mean()
print("EE-Anteil im Mittel: ", EE_Anteil_Mittel)



#Plotten=======================================

ee_intervallgrenzen = list(range(0, 170, 10))

dfGesamt["EE_Intervall"] = pd.cut(dfGesamt["EE_Anteil"], bins=ee_intervallgrenzen, include_lowest=True)

EE_Intervall_Haeufigkeit = dfGesamt["EE_Intervall"].value_counts(sort=False)

fig = px.bar(
    x=EE_Intervall_Haeufigkeit.index.astype(str),
    y=EE_Intervall_Haeufigkeit.values
)

# Diagramm mit einem Titel und Achsenbeschriftungen versehen
fig.update_layout(
    title="Häufigkeitsverteilung der EE-Anteile am Beispiel 2025 mit Simulierten Erzeugungswerten.(4, 4, 4)",
    xaxis_title="Anteil erneuerbarer Energien [%]",
    yaxis_title="Anzahl der Viertelstunden"
)

fig.show()


#dfGesamt.to_csv("profil.csv",sep=";", decimal=",", index=True)