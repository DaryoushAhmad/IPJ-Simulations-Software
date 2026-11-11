import pandas as pd
import streamlit as st

#ergänzt um das pfadproblem zu lösen 
from pathlib import Path

#bestimmt den ordner, indem DatenFunktionen.py liegt und geht einen ordner hoch
#von gemini als debug lösung der streamlit UI
BASE_DIR=Path(__file__).resolve().parent.parent
DATA_PATH_GESAMT=BASE_DIR /"data"/"bereinigt"/"SMARD_Gesamt_Bereinigt.csv"

DATA_PATH_JAHRESSTATISTIK=BASE_DIR /"data"/"bereinigt"/"SMARD_Jahresstatistik.csv"

DATA_PATH_ERZEUGERPROFIL=BASE_DIR /"data"/"bereinigt"/"EE_Jahresprofil_2020-2025.csv"


@st.cache_data  #caching funktion für streamlit
def setUpGesamtcsv():
    dfGesamt = pd.read_csv(
        DATA_PATH_GESAMT,
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
    
    # geändert kai
    dfGesamt["Datum von"] = pd.to_datetime(dfGesamt["Datum von"], format="%d.%m.%Y %H:%M", errors="coerce")   #die spalten in echte pandas datenobjekte umwandeln
    dfGesamt["Datum bis"] = pd.to_datetime(dfGesamt["Datum bis"], format="%d.%m.%Y %H:%M", errors="coerce")
    # end geändert
    
    #dataframe zurückgeben
    return dfGesamt

@st.cache_data  #caching funktion für streamlit
def setUpJahresStatistikcsv():
    dfJahresStatistik = pd.read_csv(
        DATA_PATH_JAHRESSTATISTIK,
        sep=";",    
        decimal=",",    #Pandas erklären das es ein Dezimalzeichen ist
        thousands=".",   #Pandas erklären das es ein 1000 Zeichen
        na_values=["-"]
    )

    return dfJahresStatistik
    
def setUpErzeugerProfil():
    dfErzeugerProfil = pd.read_csv(
        DATA_PATH_ERZEUGERPROFIL,
        sep=";",    
        decimal=",",    #Pandas erklären das es ein Dezimalzeichen ist
        thousands=".",   #Pandas erklären das es ein 1000 Zeichen
        na_values=["-"]
    )
    return dfErzeugerProfil
