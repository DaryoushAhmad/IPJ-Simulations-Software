import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st

# Pfade festlegen
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH_START = BASE_DIR / "data" / "bereinigt" / "dunkelflauten_start.csv"
DATA_PATH_DAUER = BASE_DIR / "data" / "bereinigt" / "dunkelflauten_dauer.csv"
DATA_PATH_P_WEITER = BASE_DIR / "data" / "bereinigt" / "dunkelflauten_p_weiter.csv"


# ---------- Wahrscheinlichkeitsdaten einlesen ----------
@st.cache_data(show_spinner=False)
def ladeWahrscheinlichkeitsDaten():

    df_P_Start = pd.read_csv(DATA_PATH_START)
    df_P_Weiter = pd.read_csv(
        DATA_PATH_P_WEITER,
        sep=";",
        decimal=",",
        encoding="utf-8-sig",
        float_precision="round_trip"
    )

    return df_P_Start, df_P_Weiter


# ---------- P_Weiter berechnen ----------

# def berechnePWeiter(df_P_Weiter):
#     """Berechnet die Exporttabelle aus den Häufigkeiten in dunkelflauten_dauer.csv."""

#     ergebnisse = []

#     for monat in range(1, 13):

#         # Nur Ereignisse des aktuellen Monats auswählen
#         dfMonat = df_P_Weiter[
#             df_P_Weiter["monat"] == monat
#         ]

#         # Maximale Dauer bestimmen
#         maxDauer = int(dfMonat["dauer_viertelstunden"].max())

#         for dauer in range(1, maxDauer + 1):

#             # Ereignisse, die länger als 'dauer' gedauert haben
#             dfLaenger = dfMonat[
#                 dfMonat["dauer_viertelstunden"] > dauer
#             ]
#             anzahlLaenger = dfLaenger["anzahl"].sum()

#             # Ereignisse, die mindestens 'dauer' gedauert haben
#             dfMinLaenger = dfMonat[
#                 dfMonat["dauer_viertelstunden"] >= dauer
#             ]
#             anzahlminLaenger = dfMinLaenger["anzahl"].sum()

#             # Wahrscheinlichkeit berechnen
#             if anzahlminLaenger > 0:
#                 wahrscheinlichkeit = anzahlLaenger / anzahlminLaenger
#             else:
#                 wahrscheinlichkeit = 0

#             ergebnisse.append({
#                 "monat": monat,
#                 "dauer_viertelstunden": dauer,
#                 "p_weiter": wahrscheinlichkeit
#             })

#     dfErgebnis = pd.DataFrame(ergebnisse)

#     return dfErgebnis


# ---------- Dunkelflautenstatus berechnen ----------

def berechneDunkelflautenStatus(dfErzeugung, dfPStart, dfPWeiter, zufallsGenerator):

    # DataFrame kopieren
    dfErzeugung = dfErzeugung.copy()

    # Wahrscheinlichkeiten für schnellen Zugriff vorbereiten
    pStart = dfPStart.set_index("monat")["p_start"].to_dict()

    pWeiter = dfPWeiter.set_index(
        ["monat", "dauer_viertelstunden"]
    )["p_weiter"].to_dict()

    # Listen für die Ergebnisse
    dunkelflautenStatus = []
    wahrscheinlichkeiten = []
    zufallsZahlen = []

    # Anfangszustand
    dunkelflauteAktiv = False
    bisherigeDauer = 0
    startMonat = 0

    # Jede Viertelstunde durchlaufen
    for zeitpunkt in dfErzeugung["Viertelstunde (Beginn)"]:

        # Monat aus dem Datum bestimmen
        # Datumsformat: 01.01. 00:00
        if isinstance(zeitpunkt, str):
            monat = int(zeitpunkt.split(".")[1])
        else:
            monat = zeitpunkt.month

        # Prüfen, ob bereits eine Dunkelflaute vorliegt
        if dunkelflauteAktiv:

            # Fortsetzungswahrscheinlichkeit bestimmen
            wahrscheinlichkeit = pWeiter.get(
                (startMonat, bisherigeDauer), 0 #aus Dictionary auslesen, 0 ist standartwert
            )

            # Zufallszahl erzeugen
            zufallsZahl = zufallsGenerator.random()

            if zufallsZahl < wahrscheinlichkeit:

                # Dunkelflaute wird fortgesetzt
                status = 0
                bisherigeDauer += 1

            else:

                # Dunkelflaute endet
                status = 1
                dunkelflauteAktiv = False
                bisherigeDauer = 0

        else:

            # Startwahrscheinlichkeit bestimmen
            wahrscheinlichkeit = pStart[monat]

            # Zufallszahl erzeugen
            zufallsZahl = zufallsGenerator.random()

            if zufallsZahl < wahrscheinlichkeit:

                # Neue Dunkelflaute beginnt
                status = 0
                dunkelflauteAktiv = True
                bisherigeDauer = 1
                startMonat = monat

            else:

                # Keine Dunkelflaute
                status = 1

        # Ergebnisse speichern
        dunkelflautenStatus.append(status)
        wahrscheinlichkeiten.append(wahrscheinlichkeit)
        zufallsZahlen.append(zufallsZahl)

    # Neue Spalten erstellen
    dfErzeugung["Dunkelflaute"] = dunkelflautenStatus
    dfErzeugung["Verwendete Wahrscheinlichkeit"] = wahrscheinlichkeiten
    dfErzeugung["Zufällige Zahl"] = zufallsZahlen

    return dfErzeugung


# ---------- Erzeugung während Dunkelflauten randomisieren ----------

def randomisiereErzeugung(
    dfErzeugung,
    installierteLeistung,
    zufallsGenerator,
    maxAenderung=1.0
):

    # DataFrame kopieren
    dfErzeugung = dfErzeugung.copy()



    # Variable für die Auslastung
    auslastung = 0
    vorherigeDunkelflaute = False


    # Eingabewerte zum Lesen
    statusArray = dfErzeugung["Dunkelflaute"].to_numpy()
    anteilPV = dfErzeugung["Anteil PV"].to_numpy()
    anteilOnshore = dfErzeugung["Anteil Wind Onshore"].to_numpy()
    anteilOffshore = dfErzeugung["Anteil Wind Offshore"].to_numpy()

    # Kopien der Erzeugungswerte zum Bearbeiten
    pv = dfErzeugung["PV [MWh]"].to_numpy(dtype=float, copy=True)
    onshore = dfErzeugung["Wind Onshore [MWh]"].to_numpy(
        dtype=float, copy=True
    )
    offshore = dfErzeugung["Wind Offshore [MWh]"].to_numpy(
        dtype=float, copy=True
    )
    windPV = dfErzeugung["Wind + PV [MWh]"].to_numpy(
        dtype=float, copy=True
    )

    # Jede Viertelstunde durchlaufen
    for i in range(len(dfErzeugung)):

        # Zeile heraussuchen an stelle [i]
        status = statusArray[i]


        if status == 0:

            # Prüfen, ob eine neue Dunkelflaute beginnt
            if not vorherigeDunkelflaute:

                # Erste Auslastung zwischen 0 und 9 Prozent
                auslastung = zufallsGenerator.uniform(0, 9)

            else:

                # Zufällige Veränderung der Auslastung
                aenderung = zufallsGenerator.uniform(
                    -maxAenderung,
                    maxAenderung
                )

                auslastung += aenderung

                # Auslastung auf 0 bis 9 Prozent begrenzen
                auslastung = np.clip(auslastung, 0, 9)

            # Neue Erzeugung in MWh berechnen
            erzeugungGesamt = (
                auslastung
                * installierteLeistung
                * 2.5
            )

            pv[i] = erzeugungGesamt * anteilPV[i]
            onshore[i] = erzeugungGesamt * anteilOnshore[i]
            offshore[i] = erzeugungGesamt * anteilOffshore[i]
            windPV[i] = erzeugungGesamt

            vorherigeDunkelflaute = True

        else:

            vorherigeDunkelflaute = False

    dfErzeugung["PV [MWh]"] = pv
    dfErzeugung["Wind Onshore [MWh]"] = onshore
    dfErzeugung["Wind Offshore [MWh]"] = offshore
    dfErzeugung["Wind + PV [MWh]"] = windPV


    return dfErzeugung


# ---------- Hauptfunktion Dunkelflautensimulation ----------

def simuliereDunkelflauten(
    dfErzeugung,
    installierteLeistung,
    maxAenderung=1.0,
    seed=42
):

    # Zufallsgenerator erstellen
    zufallsGenerator = np.random.default_rng(seed)

    # Wahrscheinlichkeitsdaten einlesen
    dfPStart, dfPWeiter = ladeWahrscheinlichkeitsDaten()

    # Dunkelflautenstatus für alle Viertelstunden bestimmen
    dfErzeugung = berechneDunkelflautenStatus(
        dfErzeugung,
        dfPStart,
        dfPWeiter,
        zufallsGenerator
    )

    # Erzeugung während Dunkelflauten randomisieren
    dfErzeugung = randomisiereErzeugung(
        dfErzeugung,
        installierteLeistung,
        zufallsGenerator,
        maxAenderung
    )

    return dfErzeugung
