from DataFunktionen import setUpErzeugerProfil

#app starten: python -m streamlit run src/app.py

#Installierte Leistungen [GW]
PV_Installiert = 118.111
windOnShore_Installiert = 68.179
windOffShore_Installiert = 9.733   
biomasse_Installiert = 0
wasserkraft_Installiert = 0


def simuliere_ee(leistung_pv, leistung_onshore, leistung_offshore, leistung_biomasse, leistung_wasserkraft,verbrauchsReferenzJahr="2025" ,gesamtVerbrauchIn_TWh=600 ):
    

    # Erzeugerprofil einlesen
    dfProfil = setUpErzeugerProfil()

    # Dataframe für Simulation erstellen
    dfSimulation = dfProfil.copy()

    # Photovoltaik Simulieren
    dfSimulation["PV [MWh]"] = (
        dfProfil["PV"]
        * PV_Installiert
        * leistung_pv
        * 2.5
    )

    # Wind Onshore Simulieren
    dfSimulation["Wind Onshore [MWh]"] = (
        dfProfil["Wind Onshore"]
        * windOnShore_Installiert
        * leistung_onshore
        * 2.5   #1000 * 0.25 / 100 = 2.5
    )
    # Wind Offshore Simulieren
    dfSimulation["Wind Offshore [MWh]"] = (
        dfProfil["Wind Offshore"]
        * windOffShore_Installiert
        * leistung_offshore
        * 2.5
    )

    # Biomasse Simulieren
    dfSimulation["Biomasse [MWh]"] = (
        dfProfil["Biomasse"]
        * biomasse_Installiert
        * leistung_biomasse
        * 2.5
    )

    # Wasserkraft Simulieren
    dfSimulation["Wasserkraft [MWh]"] = (
        dfProfil["Wasserkraft"]
        * wasserkraft_Installiert
        * leistung_wasserkraft
        * 2.5
    )

    # Verbrauch "Simulieren"
    dfSimulation["Verbrauch [MWh]"] = (
        dfProfil[f"Verbrauch {verbrauchsReferenzJahr}"] / 100
        * gesamtVerbrauchIn_TWh * 1000000
    )

    
    # EE Erzeugung berechnen
    dfSimulation["EE_Erzeugung [MWh]"] = (
        dfSimulation["PV [MWh]"] 
        + dfSimulation["Wind Onshore [MWh]"]
        + dfSimulation["Wind Offshore [MWh]"]
        + dfSimulation["Biomasse [MWh]"]
        + dfSimulation["Wasserkraft [MWh]"]
    )


    # Bilanz berechnen
    dfSimulation["Bilanz [MWh]"] = (
        dfSimulation["EE_Erzeugung [MWh]"]
        - dfSimulation["Verbrauch [MWh]"]
    )

    # Überschuss berechnen
    dfSimulation["Ueberschuss [MWh]"] = (
        dfSimulation["Bilanz [MWh]"].clip(lower=0) # clip() bedeutet alle negativen werte mit 0 ersetzen
    )

    # Fehlmenge berechnen
    dfSimulation["Fehlmenge [MWh]"] = (
        (-dfSimulation["Bilanz [MWh]"]).clip(lower=0) # (-) beachten
    )

    dfSimulation["Direkt genutzt [MWh]"] = (
        dfSimulation[
            ["EE_Erzeugung [MWh]", "Verbrauch [MWh]"]
        ].min(axis=1)
    )

    dfSimulation["Erzeugung / Verbrauch [%]"] = (
        dfSimulation["EE_Erzeugung [MWh]"]
        / dfSimulation["Verbrauch [MWh]"]
        * 100
    )

    dfSimulation["Direkte Deckung [%]"] = (
        dfSimulation["Direkt genutzt [MWh]"]
        / dfSimulation["Verbrauch [MWh]"]
        * 100
    )

    dfSimulation["Restlast [GW]"] = (
        dfSimulation["Verbrauch [MWh]"]
        - dfSimulation["EE_Erzeugung [MWh]"]
    ) / 250



    return dfSimulation

#eventuell später auslagern nach BerechnungsFunktionen!
def berechne_kennzahlen(dfSimulation):

    jahreserzeugung = (
        dfSimulation["EE_Erzeugung [MWh]"].sum()
    )

    jahresverbrauch = (
        dfSimulation["Verbrauch [MWh]"].sum()
    )

    direkt_genutzt = (
        dfSimulation["Direkt genutzt [MWh]"].sum()
    )

    jahresanteil = (
        jahreserzeugung / jahresverbrauch * 100
    )

    direkter_deckungsgrad = (
        direkt_genutzt / jahresverbrauch * 100
    )

    return {
        "Jahreserzeugung [TWh]": jahreserzeugung / 1_000_000,
        "Jahresverbrauch [TWh]": jahresverbrauch / 1_000_000,
        "Jahresanteil [%]": jahresanteil,
        "Direkter Deckungsgrad [%]": direkter_deckungsgrad
    }
