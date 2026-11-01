import pandas as pd
import streamlit as st

@st.cache_data  #caching funktion für streamlit
def setUpGesamtcsv():
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
    
    # @dary
    # dfGesamt["Datum von"] = pd.to_datetime(dfGesamt["Datum von"], format="%d.%m.%Y %H:%M", errors="coerce")   #die spalten in echte pandas datenobjekte umwandeln
    # dfGesamt["Datum bis"] = pd.to_datetime(dfGesamt["Datum bis"], format="%d.%m.%Y %H:%M", errors="coerce")
    # @dary kann man das so ändern?S
    
    #dataframe zurückgeben
    return dfGesamt

@st.cache_data  #caching funktion für streamlit
def setUpJahresStatistikcsv():
    dfJahresStatistik = pd.read_csv(
        "data/bereinigt/SMARD_Jahresstatistik.csv",
        sep=";",    
        decimal=",",    #Pandas erklären das es ein Dezimalzeichen ist
        thousands=".",   #Pandas erklären das es ein 1000 Zeichen
        na_values=["-"]
    )

    return dfJahresStatistik
    

