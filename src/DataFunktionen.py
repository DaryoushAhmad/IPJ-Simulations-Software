import pandas as pd

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
    format="%Y-%m-%d %H:%M:%S"
    )

    dfGesamt["Datum bis"] = pd.to_datetime(
    dfGesamt["Datum bis"],
    format="%Y-%m-%d %H:%M:%S"
    )   
    return dfGesamt

def setUpJahresStatistikcsv():
    dfJahresStatistik = pd.read_csv(
        "data/bereinigt/SMARD_Jahresstatistik.csv",
        sep=";",    
        decimal=",",    #Pandas erklären das es ein Dezimalzeichen ist
        thousands=".",   #Pandas erklären das es ein 1000 Zeichen
        na_values=["-"]
    )
    return dfJahresStatistik
    

