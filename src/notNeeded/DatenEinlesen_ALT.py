# import pandas as pd
# import plotly.express as px

# dfErzeugung = pd.read_csv(
#     "data/raw/Realisierte_Erzeugung.csv",
#     sep=";",    
#     decimal=",",    #Pandas erklären das es ein Dezimalzeichen ist
#     thousands=".",   #Pandas erklären das es ein 1000 Zeichen
#     na_values=["-"]
# )

# dfErzeugung["Datum von"] = pd.to_datetime(
#     dfErzeugung["Datum von"],
#     format="%d.%m.%Y %H:%M" # in 01.01.2020 00:00 Format bringen
# )

# dfErzeugung["Datum bis"] = pd.to_datetime(
#     dfErzeugung["Datum bis"],
#     format="%d.%m.%Y %H:%M" # in 01.01.2020 00:00 Format bringen
# )

# # Stromverbrauchsdaten aus der CSV-Datei einlesen
# dfVerbrauch = pd.read_csv(
#     "data/raw/Realisierter_Stromverbrauch.csv",
#     sep=";",    
#     decimal=",",    #Pandas erklären das es ein Dezimalzeichen ist
#     thousands=".",   #Pandas erklären das es ein 1000 Zeichen
#     na_values=["-"] #not Avalable Values festlegen
# )

# dfVerbrauch["Datum von"] = pd.to_datetime(
#     dfVerbrauch["Datum von"],
#     format="%d.%m.%Y %H:%M" # in 01.01.2020 00:00 Format bringen
# )

# dfVerbrauch["Datum bis"] = pd.to_datetime(
#     dfVerbrauch["Datum bis"],
#     format="%d.%m.%Y %H:%M" # in 01.01.2020 00:00 Format bringen
# )

# kernenergie = "Kernenergie [MWh] Originalauflösungen"

# dfErzeugung[kernenergie] = dfErzeugung[kernenergie].fillna(0) 

# #Liste der EE-Spalten
# ee_spalten = [
#     "Biomasse [MWh] Originalauflösungen",
#     "Wasserkraft [MWh] Originalauflösungen",
#     "Wind Offshore [MWh] Originalauflösungen",
#     "Wind Onshore [MWh] Originalauflösungen",
#     "Photovoltaik [MWh] Originalauflösungen",
#     "Sonstige Erneuerbare [MWh] Originalauflösungen"
# ]


# dfErzeugung["EE_Erzeugung"] = dfErzeugung[ee_spalten].sum(axis=1)    # Erneuerbare Stromerzeugung für jede Viertelstunde berechnen   # axis=1 bedeutet, dass die Werte innerhalb jeder Zeile addiert werden

# #print(dfErzeugung[["Datum von", "EE_Erzeugung"]].head(10))  # Die ersten 10 Ergebnisse mit den zugehörigen Zeitstempeln anzeigen


# #print(df["Datum von"].dt.year)  #Mit .dt können wir auf die einzelnen Bestandteile eines Datums zugreifen.
# #df.isna() #Diese Funktion prüft für jede Zelle, ob ein Wert fehlt.
# #print(dfErzeugung.isna().sum()) #Zählen der fehlenden Spalten
# #dfVerbrauch.info()

# #====================================================================================================================================
# #fehlende_werte = dfErzeugung.groupby(dfErzeugung["Datum von"].dt.year)[kernenergie].apply(
# #    lambda werte: werte.isna().sum()
# #)

# #print(fehlende_werte)
# #====================================================================================================================================



# #====================================================================================================================================
# #fehlende_kernenergie = dfErzeugung.loc[
# #    dfErzeugung[kernenergie].isna(),
# #    ["Datum von", kernenergie]
# #]

# #print(fehlende_kernenergie.head(10))
# #====================================================================================================================================


# # Spalten für die Identifikation eines Zeitintervalls
# zeitspalten = ["Datum von", "Datum bis"]

# # Identische Zeitintervalle in den Erzeugungsdaten durchnummerieren
# dfErzeugung["Vorkommen"] = (
#     dfErzeugung.groupby(zeitspalten, sort=False).cumcount()
# )

# # Identische Zeitintervalle in den Verbrauchsdaten durchnummerieren
# dfVerbrauch["Vorkommen"] = (
#     dfVerbrauch.groupby(zeitspalten, sort=False).cumcount()
# )



# # Erzeugungs- und Verbrauchsdaten anhand der Zeitintervalle
# # und der jeweiligen Vorkommensnummer zusammenführen

# dfGesamt = pd.merge(
#     dfErzeugung,
#     dfVerbrauch,
#     on=["Datum von", "Datum bis", "Vorkommen"],
#     how="inner",
#     validate="one_to_one"
# )

# # Prüfen, ob alle Datenzeilen erhalten geblieben sind
# #print("Erzeugungsdaten:", len(dfErzeugung))
# #print("Verbrauchsdaten:", len(dfVerbrauch))
# #print("Zusammengeführte Daten:", len(dfGesamt))

# # Sicherstellen, dass beim Merge keine Zeilen verloren gegangen sind
# assert len(dfGesamt) == len(dfErzeugung) == len(dfVerbrauch), \
#     "Achtung: Beim Zusammenführen sind Zeitintervalle verloren gegangen!"

# # Prüfen, ob die Zeitintervalle in beiden Quelldateien
# # ursprünglich in derselben Reihenfolge standen
# assert dfErzeugung[zeitspalten].reset_index(drop=True).equals(
#     dfVerbrauch[zeitspalten].reset_index(drop=True)
# ), "Achtung: Die Reihenfolge der Zeitintervalle unterscheidet sich!"

# #dfGesamt.info()
#=======================Berechnungen===============================


# from DataFunktionen import setUpGesamtcsv, setUpJahresStatistikcsv

# #Berechnung EE Anteil
# dfGesamt = setUpGesamtcsv()
# dfJahresInfos = setUpJahresStatistikcsv()


# EE_Anteil = "EE_Anteil"
# verbrauchAnteil = "Netzlast [MWh] Originalauflösungen"
# EE_Erzeugung = "EE_Erzeugung"

# dfGesamt[EE_Anteil] = dfGesamt["EE_Erzeugung"] / dfGesamt[verbrauchAnteil] * 100

# #print("Anzahl zellen in \"Netzlast [MWh] Originalauflösungen\" die 0 sind: " , dfGesamt[verbraucherAnteil].eq(0).sum())
# #print("Anzahl zellen in \"Netzlast [MWh] Originalauflösungen\" die n.a. sind: ", dfGesamt[verbraucherAnteil].isna().sum())

# EE_Anteil_Mittel = dfGesamt[EE_Anteil].mean()
# #print(round(EE_Anteil_Mittel,2))
# EE_Anteil_Am_Gesamtverbrauch = dfGesamt[EE_Erzeugung].sum()/dfGesamt[verbrauchAnteil].sum() *100
# #print(round(EE_Anteil_Am_Gesamtverbrauch,2))


# #==================Berechnen jährlicher Daten===================================
# dfJahresInfos = dfGesamt.groupby(dfGesamt["Datum von"].dt.year)[EE_Anteil].mean().to_frame()    # to_frame() da es ansonsten eine Series ist

# # Gesamte EE-Erzeugung pro Jahr berechnen
# dfJahresInfos["EE_Erzeugung"] = dfGesamt.groupby(dfGesamt["Datum von"].dt.year)[EE_Erzeugung].sum()

# # Gesamten Stromverbrauch pro Jahr berechnen
# dfJahresInfos["Netzlast [MWh] Originalauflösungen"] = dfGesamt.groupby(dfGesamt["Datum von"].dt.year)[verbrauchAnteil].sum()

# # Energiegewichteten EE-Anteil berechnen
# dfJahresInfos["EE_Anteil_Am_Gesamtverbrauch"] = dfJahresInfos["EE_Erzeugung"] / dfJahresInfos["Netzlast [MWh] Originalauflösungen"] * 100

# # Anzahl viertelstunden berchnen um schaltjahre zu erkennen
# dfJahresInfos["Anzahl_Viertelstunden"] = dfGesamt.groupby(dfGesamt["Datum von"].dt.year).size() #um schaltjahre zu entdecken

# dfJahresInfos["min_EE_Anteil"] = dfGesamt.groupby(dfGesamt["Datum von"].dt.year)[EE_Anteil].min()
# dfJahresInfos["max_EE_Anteil"] = dfGesamt.groupby(dfGesamt["Datum von"].dt.year)[EE_Anteil].max()

# #Standartabweichung berechnen
# dfJahresInfos["EE_Anteil_std"] = dfGesamt.groupby(dfGesamt["Datum von"].dt.year)[EE_Anteil].std(ddof=0)



#print(dfJahresInfos["EE_Anteil_std"])
#=======================================================================



#print("Anzahl der erfassten Viertelstunden: ",EE_Intervall_Haeufigkeit.sum())
#print("Anzahl der DataFrame-Zeilen: ",len(dfGesamt["EE_Intervall"]))



#===================================Plotly Diagramme erstellen=====================================



#====================================================================================================
# Gesamten DataFrame speichern
# dfGesamt.to_csv(
#     "data/bereinigt/SMARD_Gesamt_Bereinigt.csv",
#     sep=";",
#     decimal=",",
#     index=False
# )

# # Jahresstatistiken speichern
# dfJahresInfos.to_csv(
#     "data/bereinigt/SMARD_Jahresstatistik.csv",
#     sep=";",
#     decimal=",",
#     index=True
# )
#====================================================================================================
