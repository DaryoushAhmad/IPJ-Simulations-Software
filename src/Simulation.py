from DataFunktionen import setUpErzeugerProfil

#Installierte Leistungen [GW]
PV_Installiert = 118.111
windOnShore_Installiert = 68.179
windOffShore_Installiert = 9.733   


def simuliere_ee(faktor_pv, faktor_onshore, faktor_offshore):
    

    # Erzeugerprofil einlesen
    dfProfil = setUpErzeugerProfil()

    # Dataframe für Simulation erstellen
    dfSimulation = dfProfil.copy()

    # Photovoltaik Simulieren
    dfSimulation["PV [MWh]"] = (
        dfProfil["PV"]
        * PV_Installiert
        * faktor_pv
        * 2.5
    )

    # Photovoltaik Simulieren
    dfSimulation["Wind Onshore [MWh]"] = (
        dfProfil["Wind Onshore"]
        * windOnShore_Installiert
        * faktor_onshore
        * 2.5
    )

    # Photovoltaik Simulieren
    dfSimulation["Wind Offshore [MWh]"] = (
        dfProfil["Wind Offshore"]
        * windOffShore_Installiert
        * faktor_offshore
        * 2.5
    )

    dfSimulation["EE_Erzeugung [MWh]"] = (
        dfSimulation["PV [MWh]"] 
        + dfSimulation["Wind Onshore [MWh]"]
        + dfSimulation["Wind Offshore [MWh]"]
    )

    # Weiter EE Ezeuger berücksichtigen...

    return dfSimulation