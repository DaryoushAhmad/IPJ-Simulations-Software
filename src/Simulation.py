from DataFunktionen import setUpErzeugerProfil
from DunkelflautenSimulation import simuliereDunkelflauten

#app starten: python -m streamlit run src/app.py

def simuliere_ee(leistung_pv, leistung_onshore, leistung_offshore, leistung_biomasse, leistung_wasserkraft,verbrauchsReferenzJahr ,gesamtVerbrauchIn_TWh ):
    """Simuliert MWh je Viertelstunde aus installierten Leistungen in GW."""
    # Profilwerte in Prozent: / 100 * 1000 MW/GW * 0.25 h = Faktor 2.5.

    # Erzeugerprofil einlesen
    dfProfil = setUpErzeugerProfil()

    # Dataframe für Simulation erstellen
    dfSimulation = dfProfil.copy()

    # Photovoltaik Simulieren
    dfSimulation["PV [MWh]"] = (
        dfProfil["PV"]
        * leistung_pv
        * 2.5
    )

    # Wind Onshore Simulieren
    dfSimulation["Wind Onshore [MWh]"] = (
        dfProfil["Wind Onshore"]
        * leistung_onshore
        * 2.5   #1000 * 0.25 / 100 = 2.5
    )
    # Wind Offshore Simulieren
    dfSimulation["Wind Offshore [MWh]"] = (
        dfProfil["Wind Offshore"]
        * leistung_offshore
        * 2.5
    )

    # Biomasse Simulieren
    dfSimulation["Biomasse [MWh]"] = (
        dfProfil["Biomasse"]
        * leistung_biomasse
        * 2.5
    )

    # Wasserkraft Simulieren
    dfSimulation["Wasserkraft [MWh]"] = (
        dfProfil["Wasserkraft"]
        * leistung_wasserkraft
        * 2.5
    )

    # Verbrauch "Simulieren"
    dfSimulation["Verbrauch [MWh]"] = (
        dfProfil[f"Verbrauch {verbrauchsReferenzJahr}"] / 100
        * gesamtVerbrauchIn_TWh * 1000000
    )


    # Gesamte installierte Wind- und PV-Leistung [GW]
    installierteLeistungWindPV = (
        leistung_pv
        + leistung_onshore
        + leistung_offshore
    )

    # Wind und PV zusammenfassen
    dfSimulation["Wind + PV [MWh]"] = (
        dfSimulation["PV [MWh]"]
        + dfSimulation["Wind Onshore [MWh]"]
        + dfSimulation["Wind Offshore [MWh]"]
    ).astype(float)

    dfSimulation["Anteil PV"] = (
        dfSimulation["PV [MWh]"] / dfSimulation["Wind + PV [MWh]"]
    )

    dfSimulation["Anteil Wind Onshore"] = (
        dfSimulation["Wind Onshore [MWh]"] / dfSimulation["Wind + PV [MWh]"]
    )

    dfSimulation["Anteil Wind Offshore"] = (
        dfSimulation["Wind Offshore [MWh]"] / dfSimulation["Wind + PV [MWh]"]
    )


    # Dunkelflauten simulieren
    dfSimulation = simuliereDunkelflauten(
        dfSimulation,
        installierteLeistungWindPV,
        maxAenderung=1.0,
        seed=None
    )
    
    # EE Erzeugung berechnen
    dfSimulation["EE_Erzeugung [MWh]"] = (
        dfSimulation["Wind + PV [MWh]"]
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

    anzahlDunkelflautenViertelstunden = (
        dfSimulation["Dunkelflaute"] == 0
    ).sum()

    anteilDunkelflauten = (
        anzahlDunkelflautenViertelstunden
        / len(dfSimulation)
        * 100
    )

    print("Viertelstunden mit Dunkelflaute:", anzahlDunkelflautenViertelstunden)
    print("Anteil Dunkelflauten [%]:", anteilDunkelflauten)

    anzahlDunkelflauten = (
        (dfSimulation["Dunkelflaute"] == 0)
        & (dfSimulation["Dunkelflaute"].shift(1) != 0)
    ).sum()

    print("Anzahl Dunkelflauten:", anzahlDunkelflauten)

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
